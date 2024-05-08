from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2020_12.DataManagement import ReferencedAssemblyFileInputInfo, ReferencedAssemblyFileResponse
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getReferencedAssemblyFileInfo(cls, input: ReferencedAssemblyFileInputInfo) -> ReferencedAssemblyFileResponse:
        """
        Returns the JTPART named references and transforms for Manufacturing Bill of Material (MBOM) or Bill of Process
        (BOP) assembly lines based on Engineering Bill of Material (EBOM) parent assemblies of their immediate consumed
        or assigned lines. Currently, only the Dataset objects related by IMAN_Rendering relation are considered. The
        referenced EBOM structure is deduced based from the MBOM structure using the IMAN_METarget relation between the
        top lines. In case of BOP structure the MBOM and EBOM are deduced from the open windows in the bom world.
        
        Use cases:
        Use case1 :
        User loads EBOM and MBOM structures in Manufactruing Process Planner application. User selects an assembly in
        MBOM strcuture and opens "3-D Vis" for the selected assembly. The JTPART Dataset objects attached to the item
        revision of the immediate  parent EBOM BOMLine objects of assigned lines are mapped to the parent MBOM assembly
        of assigned BOMLine objects for display.
        
        Use case2 :
        User loads EBOM, MBOM and BOP in Manufactruing Process Planner application. User selects an assembly in BOP
        structure and opens "3-D Vis" for the selected assembly. The JTPART Dataset objects attached to the item
        revision of the immediate  parent EBOM BOMLine objects of assigned lines are mapped to the process or operation
        BOMLine objects for display.
        """
        return cls.execute_soa_method(
            method_name='getReferencedAssemblyFileInfo',
            library='Internal-Manufacturing',
            service_date='2020_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=ReferencedAssemblyFileResponse,
        )
