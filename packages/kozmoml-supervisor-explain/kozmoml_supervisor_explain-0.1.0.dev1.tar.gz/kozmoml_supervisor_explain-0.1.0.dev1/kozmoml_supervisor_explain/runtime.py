import asyncio
import functools
import json
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Optional, Dict

import numpy as np
import pandas as pd
from supervisor.api.interfaces import Explanation, Explainer
from supervisor.saving import load_explainer

from kozmoml.codecs import (
    NumpyRequestCodec,
    StringCodec,
)
from kozmoml.errors import ModelParametersMissing
from kozmoml.handlers import custom_handler
from kozmoml.model import MLModel
from kozmoml.rest.responses import Response
from kozmoml.settings import ModelSettings, ModelParameters
from kozmoml.types import (
    InferenceRequest,
    InferenceResponse,
    Parameters,
    ResponseOutput,
)
from kozmoml.utils import get_model_uri
from kozmoml_supervisor_explain.supervisor_dependency_reference import (
    get_mlmodel_class_as_str,
    get_supervisor_class_as_str,
)
from kozmoml_supervisor_explain.common import (
    SupervisorExplainSettings,
    import_and_get_class,
    EXPLAIN_PARAMETERS_TAG,
    EXPLAINER_TYPE_TAG,
)
from kozmoml_supervisor_explain.errors import InvalidExplanationShape


class SupervisorExplainRuntimeBase(MLModel):
    """
    Base class for Supervisor-Explain models
    """

    def __init__(
        self, settings: ModelSettings, explainer_settings: SupervisorExplainSettings
    ):
        self.supervisor_explain_settings = explainer_settings
        self._executor = ThreadPoolExecutor()
        super().__init__(settings)

    @custom_handler(rest_path="/explain")
    async def explain_v1_output(self, request: InferenceRequest) -> Response:
        """
        A custom endpoint to return explanation results in plain json format (no v2
        encoding) to keep backward compatibility of legacy downstream users.

        This does not work with multi-model serving as no reference to the model exists
        in the endpoint.
        """
        v2_response = await self.predict(request)

        if len(v2_response.outputs) != 1:
            raise InvalidExplanationShape(len(v2_response.outputs))

        output = v2_response.outputs[0]

        if output.shape not in ([1], [1, 1]):
            raise InvalidExplanationShape(output.shape)

        explanation = json.loads(output.data[0])

        return Response(content=explanation, media_type="application/json")

    async def predict(self, payload: InferenceRequest) -> InferenceResponse:
        """
        This is actually a call to explain as we are treating
        an explainer model as MLModel
        """

        # TODO: convert and validate?
        input_data = self.decode_request(payload, default_codec=NumpyRequestCodec)
        if isinstance(input_data, pd.DataFrame):
            input_data = np.array(input_data)
        output_data = await self._async_explain_impl(input_data, payload.parameters)

        return InferenceResponse(
            model_name=self.name,
            model_version=self.version,
            outputs=[output_data],
            parameters=Parameters(
                headers={
                    "x-kozmo-supervisor-type": "explanation",
                    "x-kozmo-supervisor-method": self.get_supervisor_method(),
                }
            ),
        )

    def get_supervisor_method(self) -> str:
        module: str = type(self._model).__module__  # type: ignore
        return module.split(".")[-1]

    async def _async_explain_impl(
        self, input_data: Any, settings: Optional[Parameters]
    ) -> ResponseOutput:
        explain_parameters = dict()
        if settings is not None:
            settings_dict = settings.dict()
            if EXPLAIN_PARAMETERS_TAG in settings_dict:
                explain_parameters = settings_dict[EXPLAIN_PARAMETERS_TAG]

        loop = asyncio.get_running_loop()
        explain_call = functools.partial(
            self._explain_impl,
            input_data=input_data,
            explain_parameters=explain_parameters,
        )
        explanation = await loop.run_in_executor(self._executor, explain_call)
        # TODO: Convert supervisor-explain output to v2 protocol, for now we use to_json
        return StringCodec.encode_output(
            payload=[explanation.to_json()], name="explanation"
        )

    async def _load_from_uri(self, predictor: Any) -> Explainer:
        """Load the explainer from disk, and pass the predictor"""
        model_parameters: Optional[ModelParameters] = self.settings.parameters
        if model_parameters is None:
            raise ModelParametersMissing(self.name)
        absolute_uri = await get_model_uri(self.settings)
        return await self._load_explainer(path=absolute_uri, predictor=predictor)

    async def _load_explainer(self, path: str, predictor: Any) -> Explainer:
        loop = asyncio.get_running_loop()
        load_call = functools.partial(load_explainer, path=path, predictor=predictor)
        return await loop.run_in_executor(self._executor, load_call)

    def _explain_impl(self, input_data: Any, explain_parameters: Dict) -> Explanation:
        """Actual explain to be implemented by subclasses"""
        raise NotImplementedError


class SupervisorExplainRuntime:
    """Wrapper / Factory class for specific supervisor explain runtimes"""

    def __new__(cls, settings: ModelSettings):
        # TODO: we probably want to validate the enum more sanely here
        # we do not want to construct a specific supervisor settings here because
        # it might be dependent on type
        # although at the moment we only have one `SupervisorExplainSettings`
        assert settings.parameters is not None
        assert EXPLAINER_TYPE_TAG in settings.parameters.extra  # type: ignore

        explainer_type = settings.parameters.extra[EXPLAINER_TYPE_TAG]  # type: ignore

        rt_class = import_and_get_class(get_mlmodel_class_as_str(explainer_type))

        supervisor_class = import_and_get_class(get_supervisor_class_as_str(explainer_type))

        return rt_class(settings, supervisor_class)
