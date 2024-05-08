from tcsoa.gen.Internal_AWS2._2018_05.services import GlobalAlternateService as imp0
from tcsoa.gen.Internal_AWS2._2017_06.services import EffectivityManagmentService as imp1
from tcsoa.gen.Internal_AWS2._2015_03.services import FullTextSearchService as imp2
from tcsoa.gen.Internal_AWS2._2012_10.services import DataManagementService as imp3
from tcsoa.gen.Internal_AWS2._2019_06.services import AdvancedSavedSearchService as imp4
from tcsoa.gen.Internal_AWS2._2016_12.services import AdvancedSearchService as imp5
from tcsoa.gen.Internal_AWS2._2017_06.services import RequirementsManagementService as imp6
from tcsoa.gen.Internal_AWS2._2012_10.services import FullTextSearchService as imp7
from tcsoa.gen.Internal_AWS2._2015_10.services import FullTextSearchService as imp8
from tcsoa.gen.Internal_AWS2._2018_05.services import FullTextSearchService as imp9
from tcsoa.gen.Internal_AWS2._2019_12.services import DataManagementService as imp10
from tcsoa.gen.Internal_AWS2._2020_05.services import UiConfigService as imp11
from tcsoa.gen.Internal_AWS2._2023_06.services import UiConfigService as imp12
from tcsoa.gen.Internal_AWS2._2016_12.services import RequirementsManagementService as imp13
from tcsoa.gen.Internal_AWS2._2019_12.services import FinderService as imp14
from tcsoa.gen.Internal_AWS2._2018_12.services import FinderService as imp15
from tcsoa.gen.Internal_AWS2._2012_10.services import RequirementsManagementService as imp16
from tcsoa.gen.Internal_AWS2._2016_03.services import RequirementsManagementService as imp17
from tcsoa.gen.Internal_AWS2._2018_12.services import MultiSiteService as imp18
from tcsoa.gen.Internal_AWS2._2012_10.services import FinderService as imp19
from tcsoa.gen.Internal_AWS2._2017_12.services import DataManagementService as imp20
from tcsoa.gen.Internal_AWS2._2016_03.services import FinderService as imp21
from tcsoa.gen.Internal_AWS2._2018_05.services import DataManagementService as imp22
from tcsoa.gen.Internal_AWS2._2022_12.services import DataManagementService as imp23
from tcsoa.gen.Internal_AWS2._2015_10.services import DataManagementService as imp24
from tcsoa.gen.Internal_AWS2._2016_12.services import DataManagementService as imp25
from tcsoa.gen.Internal_AWS2._2018_05.services import TCXMLService as imp26
from tcsoa.gen.Internal_AWS2._2014_11.services import RequirementsManagementService as imp27
from tcsoa.gen.Internal_AWS2._2020_05.services import FileMgmtService as imp28
from tcsoa.gen.Internal_AWS2._2019_06.services import RequirementsManagementService as imp29
from tcsoa.gen.Internal_AWS2._2012_10.services import OrganizationManagementService as imp30
from tcsoa.gen.Internal_AWS2._2013_12.services import OrganizationManagementService as imp31
from tcsoa.gen.Internal_AWS2._2017_12.services import FullTextSearchService as imp32
from tcsoa.gen.Internal_AWS2._2012_10.services import LOVService as imp33
from tcsoa.gen.Internal_AWS2._2016_04.services import DataManagementService as imp34
from tcsoa.gen.Internal_AWS2._2020_12.services import DataManagementService as imp35
from tcsoa.gen.Internal_AWS2._2016_03.services import UiConfigService as imp36
from tcsoa.gen.Internal_AWS2._2017_06.services import UiConfigService as imp37
from tcsoa.gen.Internal_AWS2._2022_06.services import UiConfigService as imp38
from tcsoa.gen.Internal_AWS2._2012_10.services import StructureSearchService as imp39
from tcsoa.gen.Internal_AWS2._2020_05.services import DataManagementService as imp40
from tcsoa.gen.Internal_AWS2._2020_05.services import FullTextSearchService as imp41
from tcsoa.gen.Internal_AWS2._2016_03.services import DataManagementService as imp42
from tcsoa.gen.Internal_AWS2._2017_06.services import DataManagementService as imp43
from tcsoa.gen.Internal_AWS2._2023_06.services import DataManagementService as imp44
from tcsoa.gen.Internal_AWS2._2012_10.services import WorkflowService as imp45
from tcsoa.gen.Internal_AWS2._2021_12.services import DataManagementService as imp46
from tcsoa.gen.Internal_AWS2._2014_11.services import WorkflowService as imp47
from tcsoa.gen.Internal_AWS2._2018_05.services import WorkflowService as imp48
from tcsoa.gen.Internal_AWS2._2017_06.services import FullTextSearchService as imp49
from tcsoa.gen.Internal_AWS2._2018_05.services import FileMgmtService as imp50
from tcsoa.gen.Internal_AWS2._2019_06.services import DataManagementService as imp51
from tcsoa.gen.Internal_AWS2._2018_05.services import FinderService as imp52
from tcsoa.gen.Internal_AWS2._2016_12.services import FinderService as imp53
from tcsoa.gen.Internal_AWS2._2017_06.services import FinderService as imp54
from tcsoa.gen.Internal_AWS2._2017_12.services import FinderService as imp55
from tcsoa.gen.Internal_AWS2._2019_06.services import FinderService as imp56
from tcsoa.gen.Internal_AWS2._2023_06.services import FinderService as imp57
from tcsoa.gen.Internal_AWS2._2013_12.services import WorkflowService as imp58
from tcsoa.base import TcService


class GlobalAlternateService(TcService):
    addAlternates = imp0.addAlternates
    removeAlternates = imp0.removeAlternates


class EffectivityManagmentService(TcService):
    addOrRemoveRelStatusEffectivities = imp1.addOrRemoveRelStatusEffectivities


class FullTextSearchService(TcService):
    cleanupScratchTable = imp2.cleanupScratchTable
    createFullTextSavedSearch = imp7.createFullTextSavedSearch
    createFullTextSavedSearch2 = imp8.createFullTextSavedSearch
    createFullTextSavedSearch3 = imp9.createFullTextSavedSearch
    deleteFullTextSavedSearch = imp8.deleteFullTextSavedSearch
    deleteIndexedIslands = imp2.deleteIndexedIslands
    deregisterApplicationIDs = imp2.deregisterApplicationIDs
    findFullTextSavedSearches = imp7.findFullTextSavedSearches
    getAMImpactedObjects = imp2.getAMImpactedObjects
    getAddedObjectsToUpdateIndex = imp7.getAddedObjectsToUpdateIndex
    getAddedObjectsToUpdateIndex1 = imp7.getAddedObjectsToUpdateIndex1
    getDatasetIndexableFilesInfo = imp7.getDatasetIndexableFilesInfo
    getDeletedObjectsToUpdateIndex = imp7.getDeletedObjectsToUpdateIndex
    getDeletedObjectsToUpdateIndex1 = imp7.getDeletedObjectsToUpdateIndex1
    getImpactedItemRevsForReIndex = imp7.getImpactedItemRevsForReIndex
    getIndexedObjects = imp2.getIndexedObjects
    getIndexedObjectsAndUpdate = imp32.getIndexedObjectsAndUpdate
    getModifiedObjectsToSync = imp2.getModifiedObjectsToSync
    getObjectsToIndex = imp7.getObjectsToIndex
    getPreFilters = imp7.getPreFilters
    getSearchSettings = imp41.getSearchSettings
    getSuggestions = imp7.getSuggestions
    identifyImpactedObjects = imp49.identifyImpactedObjects
    modifyFullTextSavedSearch = imp8.modifyFullTextSavedSearch
    modifyFullTextSavedSearch2 = imp9.modifyFullTextSavedSearch
    performFullTextSearch = imp7.performFullTextSearch
    queryAndUpdateSyncData = imp32.queryAndUpdateSyncData
    updateIndexIslandStatus = imp2.updateIndexIslandStatus
    updateIndexingStatus = imp7.updateIndexingStatus


class DataManagementService(TcService):
    clearHistory = imp3.clearHistory
    createIdDisplayRules = imp10.createIdDisplayRules
    getAvailableWorkspaces = imp20.getAvailableWorkspaces
    getChildren = imp3.getChildren
    getCurrentUserGateway = imp3.getCurrentUserGateway
    getCurrentUserGateway2 = imp22.getCurrentUserGateway2
    getCurrentUserGateway3 = imp23.getCurrentUserGateway3
    getDatasetTypesWithDefaultRelation = imp24.getDatasetTypesWithDefaultRelation
    getDeclarativeStyleSheets = imp25.getDeclarativeStyleSheets
    getDefaultRelation = imp25.getDefaultRelation
    getHistory = imp3.getHistory
    getIdContexts = imp10.getIdContexts
    getIdentifierTypes = imp10.getIdentifierTypes
    getInitialTableRowData = imp34.getInitialTableRowData
    getLocalizedProperties = imp35.getLocalizedProperties
    getRelatedObjsForConfiguredRevision = imp40.getRelatedObjsForConfiguredRevision
    getStyleSheet = imp34.getStyleSheet
    getStyleSheet2 = imp42.getStyleSheet2
    getStyleSheet3 = imp43.getStyleSheet3
    getTCSessionAnalyticsInfo = imp20.getTCSessionAnalyticsInfo
    getTableViewModelProperties = imp20.getTableViewModelProperties
    getTableViewModelProperties2 = imp44.getTableViewModelProperties2
    getUnprocessedXRT = imp42.getUnprocessedXRT
    getViewModelProperties = imp43.getViewModelProperties
    getViewModelProperties2 = imp20.getViewModelProperties2
    getViewerData = imp43.getViewerData
    getViewerData2 = imp46.getViewerData2
    loadDataForEditing = imp3.loadDataForEditing
    loadDataForEditing2 = imp34.loadDataForEditing
    loadViewModelForEditing = imp43.loadViewModelForEditing
    loadViewModelForEditing2 = imp20.loadViewModelForEditing2
    modifyFavorites = imp51.modifyFavorites
    pinObjects = imp22.pinObjects
    queryForFileExistence = imp46.queryForFileExistence
    saveEditAndSubmitToWorkflow = imp3.saveEditAndSubmitToWorkflow
    saveEditAndSubmitToWorkflow2 = imp34.saveEditAndSubmitToWorkflow
    saveEditAndSubmitToWorkflow3 = imp25.saveEditAndSubmitToWorkflow
    saveViewModelEditAndSubmitWorkflow = imp43.saveViewModelEditAndSubmitWorkflow
    saveViewModelEditAndSubmitWorkflow2 = imp22.saveViewModelEditAndSubmitWorkflow2
    saveXRT = imp42.saveXRT
    setLocalizedProperties = imp35.setLocalizedProperties
    unpinObjects = imp22.unpinObjects
    updateHistory = imp3.updateHistory
    updateTiles = imp22.updateTiles


class AdvancedSavedSearchService(TcService):
    createAdvancedSavedSearch = imp4.createAdvancedSavedSearch
    updateAdvancedSavedSearch = imp4.updateAdvancedSavedSearch


class AdvancedSearchService(TcService):
    createAdvancedSearchInput = imp5.createAdvancedSearchInput
    getSelectedQueryCriteria = imp5.getSelectedQueryCriteria


class RequirementsManagementService(TcService):
    createBaseline = imp6.createBaseline
    createBaselineAsync = imp6.createBaselineAsync
    exportAsync = imp13.exportAsync
    exportAsync2 = imp6.exportAsync2
    exportToApplication = imp16.exportToApplication
    exportToApplication2 = imp17.exportToApplication
    exportToApplication3 = imp13.exportToApplication2
    exportToApplication4 = imp6.exportToApplication3
    getExportTemplates = imp27.getExportTemplates
    getFullTextVersionInfo = imp29.getFullTextVersionInfo
    setRichContent = imp16.setRichContent
    setRichContent2 = imp13.setRichContent2


class UiConfigService(TcService):
    createNamedColumnConfig = imp11.createNamedColumnConfig
    createNamedColumnConfig2 = imp12.createNamedColumnConfig2
    deleteNamedColumnConfig = imp11.deleteNamedColumnConfig
    getNamedColumnConfigs = imp11.getNamedColumnConfigs
    getOrResetUIColumnConfigs = imp36.getOrResetUIColumnConfigs
    getOrResetUIColumnConfigs2 = imp37.getOrResetUIColumnConfigs2
    getOrResetUIColumnConfigs3 = imp38.getOrResetUIColumnConfigs3
    getOrResetUIColumnConfigs4 = imp12.getOrResetUIColumnConfigs4
    getVisibleCommands = imp36.getVisibleCommands
    loadNamedColumnConfig = imp11.loadNamedColumnConfig
    saveNamedColumnConfig = imp11.saveNamedColumnConfig
    saveNamedColumnConfig2 = imp12.saveNamedColumnConfig2
    saveUIColumnConfigs = imp36.saveUIColumnConfigs
    saveUIColumnConfigs2 = imp12.saveUIColumnConfigs2


class FinderService(TcService):
    exportObjectsToFile = imp14.exportObjectsToFile
    exportSearchResults = imp15.exportSearchResults
    findObjectsByClassAndAttributes2 = imp19.findObjectsByClassAndAttributes2
    findUsersTasks = imp19.findUsersTasks
    getClassificationProps = imp21.getClassificationProps
    getFilterValues = imp14.getFilterValues
    performFacetSearch = imp52.performFacetSearch
    performSearch = imp21.performSearch
    performSearch2 = imp53.performSearch2
    performSearchViewModel = imp54.performSearchViewModel
    performSearchViewModel2 = imp55.performSearchViewModel2
    performSearchViewModel3 = imp52.performSearchViewModel3
    performSearchViewModel4 = imp56.performSearchViewModel4
    performSearchViewModel5 = imp57.performSearchViewModel5


class MultiSiteService(TcService):
    fetchODSRecords = imp18.fetchODSRecords


class TCXMLService(TcService):
    getDiagnosticInfoForAcctTables = imp26.getDiagnosticInfoForAcctTables
    installDBTriggersForDataSync = imp26.installDBTriggersForDataSync
    removeDBTriggersForDataSync = imp26.removeDBTriggersForDataSync


class FileMgmtService(TcService):
    getFileNamesWithTicketInfo = imp28.getFileNamesWithTicketInfo
    loadPlmdTicketForReplace = imp50.loadPlmdTicketForReplace


class OrganizationManagementService(TcService):
    getGroupMembership = imp30.getGroupMembership
    getGroupMembership2 = imp31.getGroupMembership2


class LOVService(TcService):
    getInitialLOVValues = imp33.getInitialLOVValues
    getNextLOVValues = imp33.getNextLOVValues
    validateLOVValueSelections = imp33.validateLOVValueSelections


class StructureSearchService(TcService):
    getParentsWhereUsed = imp39.getParentsWhereUsed
    getProductsWhereUsed = imp39.getProductsWhereUsed


class WorkflowService(TcService):
    getTaskResults = imp45.getTaskResults
    getWorkflowGraph = imp47.getWorkflowGraph
    getWorkflowGraphLegend = imp47.getWorkflowGraphLegend
    getWorkflowTaskViewModel = imp48.getWorkflowTaskViewModel
    performTaskSearch = imp58.performTaskSearch
