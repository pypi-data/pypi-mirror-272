from abc import abstractmethod

from s1_cns_cli.s1graph.common.checks.base_check import BaseCheck
from s1_cns_cli.s1graph.serverless.checks.custom.registry import custom_registry


class BaseCustomCheck(BaseCheck):
    def __init__(self, name, id, categories, supported_entities, guideline=None):
        super().__init__(name=name, id=id, categories=categories, supported_entities=supported_entities,
                         block_type="serverless", guideline=guideline)
        custom_registry.register(self)

    def scan_entity_conf(self, conf, entity_type):
        return self.scan_custom_conf(conf)

    @abstractmethod
    def scan_custom_conf(self, conf):
        raise NotImplementedError()
