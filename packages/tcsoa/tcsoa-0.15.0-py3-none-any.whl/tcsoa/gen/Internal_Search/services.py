from tcsoa.gen.Internal_Search._2022_12.services import FullTextSearchService as imp0
from tcsoa.gen.Internal_Search._2020_12.services import SearchFolderService as imp1
from tcsoa.gen.Internal_Search._2021_12.services import SearchFolderService as imp2
from tcsoa.gen.Internal_Search._2021_12.services import IndexerService as imp3
from tcsoa.base import TcService


class FullTextSearchService(TcService):
    createFullTextSavedSearch2 = imp0.createFullTextSavedSearch2


class SearchFolderService(TcService):
    createOrEditSearchFolders = imp1.createOrEditSearchFolders
    deleteActiveFolders = imp2.deleteActiveFolders
    exportSearchFolders = imp1.exportSearchFolders
    getSearchFolderAccessors = imp1.getSearchFolderAccessors
    getTranslatedReportSearchRecipe = imp1.getTranslatedReportSearchRecipe
    importSearchFolder = imp1.importSearchFolder


class IndexerService(TcService):
    getDatasetIndexableFilesInfo = imp3.getDatasetIndexableFilesInfo
