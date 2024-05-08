from __future__ import annotations

from tcsoa.gen.Internal.Core._2021_12.DataManagement import DatasetsForFileResponse, DatasetsForFileInput
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def queryForFileExistence(cls, input: List[DatasetsForFileInput]) -> DatasetsForFileResponse:
        """
        This operation takes one or more file names as input and searches Teamcenter to determine if the file already
        exists. The search is limited to the Dataset objects related with any relation to the passed in
        WorkspaceObject. If the file is found, the Dataset to which it is attached is returned to the caller. If the
        file is not found, the output structure will be empty. This operation is designed to use by the Active
        Workspace client to assist when a user attaches a file to a WorkspaceObject. The operation allows the Active
        Workspace client to prompt for whether the file should create or replace the existing file if it exists.
        """
        return cls.execute_soa_method(
            method_name='queryForFileExistence',
            library='Internal-Core',
            service_date='2021_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=DatasetsForFileResponse,
        )
