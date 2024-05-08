from __future__ import annotations

from tcsoa.gen.BusinessObjects import Fnd0StructureContext, BOMWindow
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ContextManagementService(TcService):

    @classmethod
    def applyContextOnBOMWindow(cls, bomWindow: BOMWindow, structureContext: Fnd0StructureContext) -> ServiceData:
        """
        This service operation  applies a Structure Context to an existing BOMWindow. 
        All settings and search filters on the BOMWindow match those on structure context after this operation.
        
        If the structure context is not compatible with BOM Window, Operation gives error in the response. For example:
        Structure Context owned by Snapshot is considered in-compatible if the revision rule from structure context
        does not match with that of the BOM Window.
        
        Use cases:
        1. User searches related Snapshot of the opened product in Active Workspace and calls this service operation
        with Fnd0StructureContext from that Snapshot and opened BOMWindow as input to apply Snapshot on that BOMWindow.
        2. User searches related Snapshot of the opened product in Active Workspace and calls this service operation
        with Fnd0StructureContext from that Snapshot with different revision rule than Window and opened BOMWindow as
        input to apply Snapshot, then expects error to return.
        """
        return cls.execute_soa_method(
            method_name='applyContextOnBOMWindow',
            library='Internal-Rdv',
            service_date='2021_12',
            service_name='ContextManagement',
            params={'bomWindow': bomWindow, 'structureContext': structureContext},
            response_cls=ServiceData,
        )
