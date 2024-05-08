from __future__ import annotations

from tcsoa.gen.Internal.Security._2021_06.AwProjectLevelSecurity import CreateProjectInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class AwProjectLevelSecurityService(TcService):

    @classmethod
    def createProjects(cls, createInfo: List[CreateProjectInfo]) -> ServiceData:
        """
        This operation creates TC_Project business objects using the given input. The newly created project will be
        active and visible with the current login user as Project Administrator and Project Team Administrator.
        """
        return cls.execute_soa_method(
            method_name='createProjects',
            library='Internal-Security',
            service_date='2021_06',
            service_name='AwProjectLevelSecurity',
            params={'createInfo': createInfo},
            response_cls=ServiceData,
        )
