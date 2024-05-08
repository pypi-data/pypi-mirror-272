from __future__ import annotations

from tcsoa.gen.Internal.DocMgmt._2022_06.DataManagement import GenerateDsNameInput, GenerateDatasetNameResponse
from typing import List
from tcsoa.base import TcService


class DataManagementService(TcService):

    @classmethod
    def generateDatasetName(cls, input: List[GenerateDsNameInput]) -> GenerateDatasetNameResponse:
        """
        This operation generates a Dataset name using the specified file name and the WorkspaceObject constant
        Fnd0GenerateDSNameWithoutExt. This operation accepts a list of GenerateDsNameInput structures and returns a
        list of GenerateDatasetNameOutput structures which maps the generated Dataset names to the input
        WorkspaceObject objects.
        
        Use cases:
        &bull;    Add a new file to existing DocumentRevision business object. 
        In Active Workspace Client, when opening a DocumentRevison business object in the Overview tab, under the
        "FILES" section, there is an "Add to" button the user can click to add a new file to the DocumentRevision
        object. For example, if the "Fnd0GenerateDSNameWithoutExt" business constant for DocumentRevision is false,
        then the Dataset name will be looked like "test.docx".
        
        &bull;    Drag and drop a file to an existing DocumentRevision business object.
        In Active Workspace Client, when opening a DocumentRevison business object in the Overview tab, under the
        "FILES" section, user can drag and drop a file into the section, that will add a new file to the
        DocumentRevision object. For example, if the "Fnd0GenerateDSNameWithoutExt" business constant for
        DocumentRevision is true, then the Dataset name will be looked like "test".
        """
        return cls.execute_soa_method(
            method_name='generateDatasetName',
            library='Internal-DocMgmt',
            service_date='2022_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GenerateDatasetNameResponse,
        )
