from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2022_12.DataManagement import GetCurrentUserGateway3Response
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getCurrentUserGateway3(cls) -> GetCurrentUserGateway3Response:
        """
        The operation looks for the Awp0TileCollection with current logged in user as scope and returns information
        about the Awp0Tile objects associated to it.
        
        Use cases:
        This operation is suited to display the Awp0Tile objects on the Active Workspace client gateway page through
        the Tile2 objects. The Tile2 objects that are returned by this operation are the ones which are configured for
        the logged in user based on current group, role, and project.
        
        Display the user specific Awp0Tile objects during startup
        1. User logs into Active Workspace.
        2. Active Workspace invokes getCurrentUserGateway3 operation.
        3. Displays the groups of Tile2 objects that are configured for the logged in user.
        
        Display the user specific Awp0Tile objects during context change
        1. User changes the group/role/project in Active Workspace.
        2. Active Workspace invokes getCurrentUserGateway3 operation.
        3. Displays the groups of Tile2 objects that are configured for the logged in user based on current group,
        role, and project.
        """
        return cls.execute_soa_method(
            method_name='getCurrentUserGateway3',
            library='Internal-AWS2',
            service_date='2022_12',
            service_name='DataManagement',
            params={},
            response_cls=GetCurrentUserGateway3Response,
        )
