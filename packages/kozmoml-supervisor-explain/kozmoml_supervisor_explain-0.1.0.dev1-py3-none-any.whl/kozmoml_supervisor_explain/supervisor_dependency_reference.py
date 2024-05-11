from dataclasses import dataclass
from enum import Enum
from typing import Union, Dict


@dataclass
class ExplainerDependencyReference:
    """Class for keeping track of dependencies required to Supervisor runtime."""

    explainer_name: str
    supervisor_class: str
    runtime_class: str


_ANCHOR_IMAGE_TAG = "anchor_image"
_ANCHOR_TEXT_TAG = "anchor_text"
_ANCHOR_TABULAR_TAG = "anchor_tabular"
_KERNEL_SHAP_TAG = "kernel_shap"
_INTEGRATED_GRADIENTS_TAG = "integrated_gradients"
_TREE_SHAP_TAG = "tree_shap"
_TREE_PARTIAL_DEPENDENCE_TAG = "tree_partial_dependence"
_TREE_PARTIAL_DEPENDENCE_VARIANCE_TAG = "tree_partial_dependence_variance"


# NOTE: to add new explainers populate the below dict with a new
# ExplainerDependencyReference, referencing the specific runtime class in kozmoml
# and the specific supervisor explain class.
# this can be simplified when supervisor moves to a config based init.

# Steps:
#  update _TAG_TO_RT_IMPL
#  update ExplainerEnum

_BLACKBOX_MODULE = "kozmoml_supervisor_explain.explainers.black_box_runtime"
_INTEGRATED_GRADIENTS_MODULE = "kozmoml_supervisor_explain.explainers.integrated_gradients"
_WHITEBOX_SKLEARN_MODULE = "kozmoml_supervisor_explain.explainers.sklearn_api_runtime"

_TAG_TO_RT_IMPL: Dict[str, ExplainerDependencyReference] = {
    _ANCHOR_IMAGE_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_IMAGE_TAG,
        runtime_class=f"{_BLACKBOX_MODULE}.SupervisorExplainBlackBoxRuntime",
        supervisor_class="supervisor.explainers.AnchorImage",
    ),
    _ANCHOR_TABULAR_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_TABULAR_TAG,
        runtime_class=f"{_BLACKBOX_MODULE}.SupervisorExplainBlackBoxRuntime",
        supervisor_class="supervisor.explainers.AnchorTabular",
    ),
    _ANCHOR_TEXT_TAG: ExplainerDependencyReference(
        explainer_name=_ANCHOR_TEXT_TAG,
        runtime_class=f"{_BLACKBOX_MODULE}.SupervisorExplainBlackBoxRuntime",
        supervisor_class="supervisor.explainers.AnchorText",
    ),
    _KERNEL_SHAP_TAG: ExplainerDependencyReference(
        explainer_name=_KERNEL_SHAP_TAG,
        runtime_class=f"{_BLACKBOX_MODULE}.SupervisorExplainBlackBoxRuntime",
        supervisor_class="supervisor.explainers.KernelShap",
    ),
    _INTEGRATED_GRADIENTS_TAG: ExplainerDependencyReference(
        explainer_name=_INTEGRATED_GRADIENTS_TAG,
        runtime_class=f"{_INTEGRATED_GRADIENTS_MODULE}.IntegratedGradientsWrapper",
        supervisor_class="supervisor.explainers.IntegratedGradients",
    ),
    _TREE_SHAP_TAG: ExplainerDependencyReference(
        explainer_name=_TREE_SHAP_TAG,
        runtime_class=f"{_WHITEBOX_SKLEARN_MODULE}.SKLearnRuntime",
        supervisor_class="supervisor.explainers.TreeShap",
    ),
    _TREE_PARTIAL_DEPENDENCE_TAG: ExplainerDependencyReference(
        explainer_name=_TREE_PARTIAL_DEPENDENCE_TAG,
        runtime_class=f"{_WHITEBOX_SKLEARN_MODULE}.SKLearnRuntime",
        supervisor_class="supervisor.explainers.TreePartialDependence",
    ),
    _TREE_PARTIAL_DEPENDENCE_VARIANCE_TAG: ExplainerDependencyReference(
        explainer_name=_TREE_PARTIAL_DEPENDENCE_VARIANCE_TAG,
        runtime_class=f"{_WHITEBOX_SKLEARN_MODULE}.SKLearnRuntime",
        supervisor_class="supervisor.explainers.PartialDependenceVariance",
    ),
}


class ExplainerEnum(str, Enum):
    anchor_image = _ANCHOR_IMAGE_TAG
    anchor_text = _ANCHOR_TEXT_TAG
    anchor_tabular = _ANCHOR_TABULAR_TAG
    kernel_shap = _KERNEL_SHAP_TAG
    integrated_gradients = _INTEGRATED_GRADIENTS_TAG
    tree_shap = _TREE_SHAP_TAG
    tree_partial_dependence = _TREE_PARTIAL_DEPENDENCE_TAG
    tree_partial_dependence_variance = _TREE_PARTIAL_DEPENDENCE_VARIANCE_TAG


def get_mlmodel_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].runtime_class


def get_supervisor_class_as_str(tag: Union[ExplainerEnum, str]) -> str:
    if isinstance(tag, ExplainerEnum):
        tag = tag.value
    return _TAG_TO_RT_IMPL[tag].supervisor_class
