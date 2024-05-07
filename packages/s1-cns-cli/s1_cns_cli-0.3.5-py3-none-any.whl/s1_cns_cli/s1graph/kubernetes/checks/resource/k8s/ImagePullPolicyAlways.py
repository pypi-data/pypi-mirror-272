import re
from typing import Any, Dict

from s1_cns_cli.s1graph.common.models.consts import DOCKER_IMAGE_REGEX
from s1_cns_cli.s1graph.common.models.enums import CheckResult
from s1_cns_cli.s1graph.kubernetes.checks.resource.base_container_check import BaseK8sContainerCheck


class ImagePullPolicyAlways(BaseK8sContainerCheck):
    def __init__(self) -> None:
        """
        Image pull policy should be set to always to ensure you get the correct image and imagePullSecrets are correct
        Default is 'IfNotPresent' unless image tag is omitted or :latest
        https://kubernetes.io/docs/concepts/configuration/overview/#container-images

        An admission controller could be used to enforce imagePullPolicy
        """
        name = "Image Pull Policy should be Always"
        id = "CKV_K8S_15"
        # Location: container .imagePullPolicy
        super().__init__(name=name, id=id)

    def scan_container_conf(self, metadata: Dict[str, Any], conf: Dict[str, Any]) -> CheckResult:
        self.evaluated_container_keys = ["image", "imagePullPolicy"]
        if conf.get("image"):
            # Remove the digest, if present
            image_val = conf["image"]
            if not isinstance(image_val, str) or image_val.strip() == "":
                return CheckResult.UNKNOWN
            if "@" in image_val:
                image_val = image_val[0 : image_val.index("@")]
                has_digest = True
            else:
                has_digest = False
            if "imagePullPolicy" not in conf:
                image_tag_match = re.findall(DOCKER_IMAGE_REGEX, image_val)
                if len(image_tag_match) != 1:
                    # If image name is invalid, check result can not be determined
                    return CheckResult.UNKNOWN
                (image, tag) = image_tag_match[0]
                if tag == "latest" or tag == "":
                    # Default imagePullPolicy = Always
                    return CheckResult.PASSED
                elif has_digest:
                    return CheckResult.PASSED
                else:
                    # Default imagePullPolicy = IfNotPresent
                    return CheckResult.FAILED
            else:
                if not has_digest and conf["imagePullPolicy"] != "Always":
                    return CheckResult.FAILED

        else:
            return CheckResult.FAILED
        return CheckResult.PASSED


check = ImagePullPolicyAlways()
