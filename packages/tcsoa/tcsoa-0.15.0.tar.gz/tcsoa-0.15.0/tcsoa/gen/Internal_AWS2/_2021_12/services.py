from __future__ import annotations

from tcsoa.gen.Internal.AWS2._2021_12.DataManagement import GetViewerDataResponse, DatasetsForFileResponse, GetViewerDataIn, DatasetsForFileInput
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def getViewerData2(cls, inputs: GetViewerDataIn) -> GetViewerDataResponse:
        """
        This operation returns the Dataset, file and relevant viewer data for given combination of input object,
        Dataset, named reference and direction by processing the viewer preference set by Teamcenter Administrator. 
        
        Dataset objects associated with the input object are retrieved and sorted based on the values of viewer
        preference. Thereafter, appropriate subsequent Dataset is identified using direction and the current input
        Dataset displayed on the viewer. The corresponding file and viewer information along with Dataset is returned
        in the response. 
        
        Supported viewer configuration for given a Dataset type is configured by "AWC_defaultViewerConfig.VIEWERCONFIG"
        preference.
        
        Use cases:
        &bull;    Display default viewer when object is selected or opened in Active Workspace.
        &bull;    Navigate to next named reference if Dataset has multiple references else navigate to next dataset in
        Active Workspace Viewer Gallery.
        &bull;    Navigate to previous named reference if Dataset has multiple references else navigate to previous
        Named reference in Active Workspace Viewer Gallery.
        """
        return cls.execute_soa_method(
            method_name='getViewerData2',
            library='Internal-AWS2',
            service_date='2021_12',
            service_name='DataManagement',
            params={'inputs': inputs},
            response_cls=GetViewerDataResponse,
        )

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
            library='Internal-AWS2',
            service_date='2021_12',
            service_name='DataManagement',
            params={'input': input},
            response_cls=DatasetsForFileResponse,
        )
