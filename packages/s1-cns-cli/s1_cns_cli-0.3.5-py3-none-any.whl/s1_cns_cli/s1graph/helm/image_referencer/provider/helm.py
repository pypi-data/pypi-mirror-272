from __future__ import annotations

from typing import TYPE_CHECKING

from s1_cns_cli.s1graph.helm.image_referencer.base_provider import BaseHelmProvider
from s1_cns_cli.s1graph.kubernetes.image_referencer.provider.k8s import SUPPORTED_K8S_IMAGE_RESOURCE_TYPES

if TYPE_CHECKING:
    from networkx import DiGraph


class HelmProvider(BaseHelmProvider):
    def __init__(self, graph_connector: DiGraph, original_root_dir: str, temp_root_dir: str):
        super().__init__(
            graph_connector=graph_connector,
            supported_resource_types=SUPPORTED_K8S_IMAGE_RESOURCE_TYPES,
            original_root_dir=original_root_dir,
            temp_root_dir=temp_root_dir
        )
