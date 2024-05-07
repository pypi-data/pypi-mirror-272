from s1_cns_cli.s1graph.common.models.enums import CheckResult, CheckCategories
from s1_cns_cli.s1graph.terraform.checks.resource.base_resource_check import BaseResourceCheck


class ECSClusterContainerInsights(BaseResourceCheck):
    def __init__(self):
        name = "Ensure container insights are enabled on ECS cluster"
        id = "CKV_AWS_65"
        supported_resources = ['aws_ecs_cluster']
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        if 'setting' in conf.keys():
            for idx, setting in enumerate(conf['setting']):
                if isinstance(setting, dict) and setting['name'] == ['containerInsights'] \
                        and setting['value'] == ['enabled']:
                    self.evaluated_keys = [f'setting/[{idx}]/name', f'setting/[{idx}]/value']
                    return CheckResult.PASSED
        return CheckResult.FAILED


check = ECSClusterContainerInsights()
