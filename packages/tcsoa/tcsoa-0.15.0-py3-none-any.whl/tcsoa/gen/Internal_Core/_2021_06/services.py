from __future__ import annotations

from tcsoa.gen.Internal.Core._2021_06.DataManagement import GenerateDsNameInput, GenerateDatasetNameResponse
from tcsoa.gen.Core._2006_03.FileManagement import GetDatasetWriteTicketsInputData, GetDatasetWriteTicketsResponse
from tcsoa.gen.Core._2007_01.FileManagement import GetTransientFileTicketsResponse, TransientFileInfo
from typing import List
from tcsoa.base import TcService


class FileManagementService(TcService):

    @classmethod
    def getTransientTicketsForChunkedUpload(cls, transientFileInfos: List[TransientFileInfo]) -> GetTransientFileTicketsResponse:
        """
        This operation gets the tickets for the desired files to be uploaded to the transient volume, for uploads using
        the FMS chunked upload methods. The 'TransientFileInfo' contains the basic information for a file to be
        uploaded such as file name, file type and whether the file should be deleted after reading. The tickets
        returned by this operation support only the chunked upload methods and are different from the tickets generated
        using 'getTransientFileTicketsForUpload'.
        """
        return cls.execute_soa_method(
            method_name='getTransientTicketsForChunkedUpload',
            library='Internal-Core',
            service_date='2021_06',
            service_name='FileManagement',
            params={'transientFileInfos': transientFileInfos},
            response_cls=GetTransientFileTicketsResponse,
        )

    @classmethod
    def getDatasetTicketsForChunkedUpload(cls, inputs: List[GetDatasetWriteTicketsInputData]) -> GetDatasetWriteTicketsResponse:
        """
        This operation obtains File Management System (FMS) chunked upload tickets and file storage information for a
        set of supplied Dataset objects. The upload tickets are used to transfer files from a local storage to a
        Teamcenter volume using the FMS chunked upload methods, and the file storage information can be used to commit
        Dataset objects referencing those transferred files.
        This operation supports the upload of files representing named references of a Dataset object to a Teamcenter
        volume.
        """
        return cls.execute_soa_method(
            method_name='getDatasetTicketsForChunkedUpload',
            library='Internal-Core',
            service_date='2021_06',
            service_name='FileManagement',
            params={'inputs': inputs},
            response_cls=GetDatasetWriteTicketsResponse,
        )


class DataManagementService(TcService):

    @classmethod
    def generateDatasetName(cls, input: List[GenerateDsNameInput]) -> GenerateDatasetNameResponse:
        """
        This operation generates Dataset names based on file names, relation names and WorkspaceObject object. If the
        "Fnd0GenerateDSNameWithoutExt" business constant for the business object is false, then the Dataset names
        returned will have the file name extensions including the period; otherwise, the Dataset names returned will
        not have the file name extensions. The BusinessObject constant "Fnd0GenerateDSNameWithoutExt" is defined under
        ItemRevision business object.
        
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
            library='Internal-Core',
            service_date='2021_06',
            service_name='DataManagement',
            params={'input': input},
            response_cls=GenerateDatasetNameResponse,
        )
