from __future__ import annotations

from tcsoa.gen.Internal.Bom._2021_12.StructureManagement import GetAlignDesignsInput, GetAlignedPartsCsidChainResp, GetAlignedPartsInput, GetAlignedDesignsResp
from tcsoa.base import TcService


class StructureManagementService(TcService):

    @classmethod
    def getAlignedDesigns(cls, input: GetAlignDesignsInput) -> GetAlignedDesignsResp:
        """
        This operaton finds the aligned design lines (BOMLine) and design product from input part lines and returns the
        aligned design line (BOMLine) objects, their clone stable ID chains,  and the design product (ItemRevision) in
        response.
        """
        return cls.execute_soa_method(
            method_name='getAlignedDesigns',
            library='Internal-Bom',
            service_date='2021_12',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=GetAlignedDesignsResp,
        )

    @classmethod
    def getAlignedPartsCsidChain(cls, input: GetAlignedPartsInput) -> GetAlignedPartsCsidChainResp:
        """
        This operaton find the aligned part lines (BOMLine) from the input design csid chains and returns the aligned
        part line (BOMLine) objects and their csid chains in response.
        """
        return cls.execute_soa_method(
            method_name='getAlignedPartsCsidChain',
            library='Internal-Bom',
            service_date='2021_12',
            service_name='StructureManagement',
            params={'input': input},
            response_cls=GetAlignedPartsCsidChainResp,
        )
