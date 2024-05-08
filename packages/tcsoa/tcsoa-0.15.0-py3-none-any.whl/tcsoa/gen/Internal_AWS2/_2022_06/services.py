from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2016_03.UiConfig import GetOrResetUIColumnConfigInput
from tcsoa.gen.Internal.AWS2._2022_06.UiConfig import GetOrResetUIColumnConfigResponse
from typing import List
from tcsoa.base import TcService


class UiConfigService(TcService):

    @classmethod
    def getOrResetUIColumnConfigs3(cls, getOrResetUiConfigsIn: List[GetOrResetUIColumnConfigInput]) -> GetOrResetUIColumnConfigResponse:
        """
        This operation returns information used by the client to render the table view in Active Workspace. The
        information returned includes column configuration information of the table view. 
        If the resetColumnConfig flag is "True", this operation deletes the column configuration of the input scope and
        then queries the new effective UI column configuration for the login user. This operation clears the login user
        column configurations.
        
        Use cases:
        Request UI Configuration(s) based on the current login user
        Client requests the column information for one or more client scopes using this operation and scope as login
        user.
        
        Request UI Configuration(s) based on a specific Teamcenter scope
        Client requests the column information for one or more client scopes using this operation and scope as Role,
        Site or Group.
        
        Request to reset UI Column Configuration(s) based on the current login user
        If a client needs to reset the column information for login user scope, they can use this operation. The new
        effective UI column configuration will be retrieved for the login user.
        """
        return cls.execute_soa_method(
            method_name='getOrResetUIColumnConfigs3',
            library='Internal-AWS2',
            service_date='2022_06',
            service_name='UiConfig',
            params={'getOrResetUiConfigsIn': getOrResetUiConfigsIn},
            response_cls=GetOrResetUIColumnConfigResponse,
        )
