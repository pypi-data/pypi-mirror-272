from __future__ import annotations

from tcsoa.gen.StructureManagement._2022_06.RevisionRuleAdministration import GetAPSValidRevisionRulesResponse
from tcsoa.base import TcService
from tcsoa.gen.BusinessObjects import WorkspaceObject


class RevisionRuleAdministrationService(TcService):

    @classmethod
    def getAPSValidRevisionRules(cls, inputObject: WorkspaceObject) -> GetAPSValidRevisionRulesResponse:
        """
        Retrieves the Advanced PLM Services (APS) non-suppressed revision rules (RevisionRule) valid for the input
        WorkspaceObject.
        Common uses for RevisionRule include configuration of product structure, Collaborative Design, Product
        Configurator, Search. Examples of Rule Entries are: Latest Entry, Working Entry, Status Entry, and Override
        Entry.
        
        Use cases:
        Input: 
            {
                inputObject = { Cfg0ProductItem }
            }
            
        Output:
        The output of the operation returns valid RevisionRule objects for the given configurator context input which
        can be used to configure the configurator data objects.
        """
        return cls.execute_soa_method(
            method_name='getAPSValidRevisionRules',
            library='StructureManagement',
            service_date='2022_06',
            service_name='RevisionRuleAdministration',
            params={'inputObject': inputObject},
            response_cls=GetAPSValidRevisionRulesResponse,
        )
