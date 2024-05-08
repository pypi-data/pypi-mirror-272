from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from tcsoa.gen.Internal.Cae._2011_06.StructureManagement import ExecuteRuleResponse
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def executeDatamap(cls, rootBOMLine: BOMLine) -> ExecuteRuleResponse:
        """
        This internal operation creates an output BOM structure given the root BOMLine of an input BOM structure loaded
        in a BOMWindow. The output BOM structure is determined by the XSLT-based Data Map rules executed against the
        input BOM structure. Data Map syntax is in compliance with the schema defined in tcsim_xslWithNode.xsd, located
        in TC_DATA.
        
        Data Map rules define the mapping between an input item type and its resulting output item type. Data Map rules
        are defined for an entire site and are stored in the datamapping.xml file located in TC_DATA. The naming of the
        data mapping file is defined by the site preference CAE_dataMapping_file.
        
        The datamapping.xml file can be configured for various domains defined as LOV objects under StructureMap
        Domains in BMIDE. To configure the domains, in the Extensions view in BMIDE, open LOV->StructureMap Domains and
        add additional domain values. This operation assumes the value of the domain as CAE.
        
        To use this operation, a well-defined datamapping.xml is required in TC_DATA.
        
        
        Use cases:
        Use Case 1: Create an output structure given a top BOMLine of the input structure
        
        Given an input BOM structure, the user can apply the Data Map rules to the BOM structure and generate a
        corresponding output BOM structure. The output BOM structure would consist of BOM line occurrences of
        ItemRevision objects as defined in the datamapping.xml file. The user can review the actions executed with the
        process log returned with the BOMViewRevision.
        """
        return cls.execute_soa_method(
            method_name='executeDatamap',
            library='Internal-Cae',
            service_date='2011_06',
            service_name='StructureManagement',
            params={'rootBOMLine': rootBOMLine},
            response_cls=ExecuteRuleResponse,
        )
