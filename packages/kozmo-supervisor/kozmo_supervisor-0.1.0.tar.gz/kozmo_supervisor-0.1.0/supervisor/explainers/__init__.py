"""
The 'supervisor.explainers' module includes feature importance, counterfactual and anchor-based explainers.
"""

from supervisor.utils.missing_optional_dependency import import_optional
from supervisor.explainers.ale import ALE, plot_ale
from supervisor.explainers.anchors.anchor_text import AnchorText
from supervisor.explainers.anchors.anchor_tabular import AnchorTabular
from supervisor.explainers.anchors.anchor_image import AnchorImage
from supervisor.explainers.cfrl_base import CounterfactualRL
from supervisor.explainers.cfrl_tabular import CounterfactualRLTabular
from supervisor.explainers.partial_dependence import PartialDependence, TreePartialDependence, plot_pd
from supervisor.explainers.pd_variance import PartialDependenceVariance, plot_pd_variance
from supervisor.explainers.permutation_importance import PermutationImportance, plot_permutation_importance
from supervisor.explainers.similarity.grad import GradientSimilarity


DistributedAnchorTabular = import_optional(
    'supervisor.explainers.anchors.anchor_tabular_distributed',
    names=['DistributedAnchorTabular'])

CEM = import_optional(
    'supervisor.explainers.cem',
    names=['CEM'])

CounterfactualProto, CounterFactualProto = import_optional(
    'supervisor.explainers.cfproto',
    names=['CounterfactualProto', 'CounterFactualProto'])  # TODO: remove in an upcoming release

Counterfactual, CounterFactual = import_optional(
    'supervisor.explainers.counterfactual',
    names=['Counterfactual', 'CounterFactual'])  # TODO: remove in an upcoming release

IntegratedGradients = import_optional(
    'supervisor.explainers.integrated_gradients',
    names=['IntegratedGradients'])

KernelShap, TreeShap = import_optional(
    'supervisor.explainers.shap_wrappers',
    names=['KernelShap', 'TreeShap'])

__all__ = [
    "ALE",
    "AnchorTabular",
    "DistributedAnchorTabular",
    "AnchorText",
    "AnchorImage",
    "CEM",
    "Counterfactual",
    "CounterfactualProto",
    "CounterfactualRL",
    "CounterfactualRLTabular",
    "plot_ale",
    "PartialDependence",
    "TreePartialDependence",
    "PartialDependenceVariance",
    "PermutationImportance",
    "plot_pd",
    "plot_pd_variance",
    "plot_permutation_importance",
    "IntegratedGradients",
    "KernelShap",
    "TreeShap",
    "GradientSimilarity"
]
