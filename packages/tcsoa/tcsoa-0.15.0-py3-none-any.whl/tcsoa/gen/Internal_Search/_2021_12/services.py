from __future__ import annotations

from tcsoa.gen.Internal.Search._2021_12.Indexer import GetDatasetIndexableFilesInfoResp
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SearchFolderService(TcService):

    @classmethod
    def deleteActiveFolders(cls, activeFolders: List[str]) -> ServiceData:
        """
        This operation deletes a list of Active Folders provided in the input parameter.
        
        Use cases:
        Active Folders can be deleted in bulk. In order to do so, a user selects a group of Active Folders and follows
        that up with a call to this operation.
        """
        return cls.execute_soa_method(
            method_name='deleteActiveFolders',
            library='Internal-Search',
            service_date='2021_12',
            service_name='SearchFolder',
            params={'activeFolders': activeFolders},
            response_cls=ServiceData,
        )


class IndexerService(TcService):

    @classmethod
    def getDatasetIndexableFilesInfo(cls, datasetUIDs: List[str], referenceNames: List[str]) -> GetDatasetIndexableFilesInfoResp:
        """
        This operation finds files associated with a given list of Datasets and filters out those which are not
        supported for indexing. Optionally, reference names can be specified to further restrict the returned files.
        Finally, returns a map of Dataset UIDs and information on supported files including UID and FMS ticket for file
        download.
        
        Use cases:
        Get information on all indexable files for given Datasets.
        Get information on indexable files for given Datasets and associated with the reference names, MSWord and
        MSWordX.
        """
        return cls.execute_soa_method(
            method_name='getDatasetIndexableFilesInfo',
            library='Internal-Search',
            service_date='2021_12',
            service_name='Indexer',
            params={'datasetUIDs': datasetUIDs, 'referenceNames': referenceNames},
            response_cls=GetDatasetIndexableFilesInfoResp,
        )
