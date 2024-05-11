from typing import Any

import joblib
from xgboost.core import XGBoostError

from kozmoml_xgboost.xgboost import _load_sklearn_interface as load_xgb_model
from kozmoml.errors import InvalidModelURI
from kozmoml_supervisor_explain.explainers.white_box_runtime import (
    SupervisorExplainWhiteBoxRuntime,
)


class SKLearnRuntime(SupervisorExplainWhiteBoxRuntime):
    """
    Runtime for white-box explainers that require access to a tree-based model matching
    the SKLearn API, such as a sklearn, XGBoost, or LightGBM model. Example explainers
    include TreeShap and TreePartialDependence.
    """

    async def _get_inference_model(self) -> Any:
        inference_model_path = self.supervisor_explain_settings.infer_uri
        # Attempt to load model.
        try:
            # Try to load as joblib model first
            model = joblib.load(inference_model_path)
        except (IndexError, KeyError, IOError):
            try:
                # Try to load as XGBoost model
                model = load_xgb_model(inference_model_path)
            except XGBoostError:
                raise InvalidModelURI(self.name, inference_model_path)
        return model
