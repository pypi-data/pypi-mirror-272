from tcsoa.gen.Manufacturing._2012_02.services import DataManagementService as imp0
from tcsoa.gen.Manufacturing._2014_06.services import DataManagementService as imp1
from tcsoa.gen.Manufacturing._2008_06.services import TimeManagementService as imp2
from tcsoa.gen.Manufacturing._2012_09.services import DataManagementService as imp3
from tcsoa.gen.Manufacturing._2009_10.services import ModelService as imp4
from tcsoa.gen.Manufacturing._2010_09.services import TimeManagementService as imp5
from tcsoa.gen.Manufacturing._2020_04.services import CoreService as imp6
from tcsoa.gen.Manufacturing._2014_06.services import ResourceManagementService as imp7
from tcsoa.gen.Manufacturing._2013_05.services import IPAManagementService as imp8
from tcsoa.gen.Manufacturing._2009_06.services import StructureManagementService as imp9
from tcsoa.gen.Manufacturing._2011_06.services import DataManagementService as imp10
from tcsoa.gen.Manufacturing._2009_10.services import MFGPropertyCollectorService as imp11
from tcsoa.gen.Manufacturing._2013_12.services import ModelService as imp12
from tcsoa.gen.Manufacturing._2009_10.services import StructureManagementService as imp13
from tcsoa.gen.Manufacturing._2018_11.services import StructureManagementService as imp14
from tcsoa.gen.Manufacturing._2013_05.services import DataManagementService as imp15
from tcsoa.gen.Manufacturing._2015_10.services import StructureManagementService as imp16
from tcsoa.gen.Manufacturing._2009_10.services import DataManagementService as imp17
from tcsoa.gen.Manufacturing._2014_12.services import StructureSearchService as imp18
from tcsoa.gen.Manufacturing._2008_06.services import DataManagementService as imp19
from tcsoa.gen.Manufacturing._2012_02.services import IPAManagementService as imp20
from tcsoa.gen.Manufacturing._2008_12.services import IPAManagementService as imp21
from tcsoa.gen.Manufacturing._2012_09.services import ValidationService as imp22
from tcsoa.gen.Manufacturing._2016_03.services import ImportExportService as imp23
from tcsoa.gen.Manufacturing._2013_05.services import StructureManagementService as imp24
from tcsoa.gen.Manufacturing._2014_12.services import IPAManagementService as imp25
from tcsoa.gen.Manufacturing._2008_06.services import CoreService as imp26
from tcsoa.gen.Manufacturing._2010_09.services import CoreService as imp27
from tcsoa.gen.Manufacturing._2013_05.services import CoreService as imp28
from tcsoa.gen.Manufacturing._2013_05.services import StructureSearchService as imp29
from tcsoa.gen.Manufacturing._2017_05.services import ValidationService as imp30
from tcsoa.gen.Manufacturing._2012_02.services import ModelService as imp31
from tcsoa.gen.Manufacturing._2017_11.services import DataManagementService as imp32
from tcsoa.gen.Manufacturing._2009_10.services import ModelDefinitionsService as imp33
from tcsoa.gen.Manufacturing._2014_12.services import ValidationService as imp34
from tcsoa.gen.Manufacturing._2018_06.services import DataManagementService as imp35
from tcsoa.gen.Manufacturing._2012_02.services import ConstraintsService as imp36
from tcsoa.gen.Manufacturing._2011_06.services import StructureManagementService as imp37
from tcsoa.gen.Manufacturing._2013_12.services import ResourceManagementService as imp38
from tcsoa.gen.Manufacturing._2013_05.services import TimeWayPlanService as imp39
from tcsoa.gen.Manufacturing._2017_05.services import ImportExportService as imp40
from tcsoa.gen.Manufacturing._2013_05.services import ImportExportService as imp41
from tcsoa.gen.Manufacturing._2015_10.services import ImportExportService as imp42
from tcsoa.gen.Manufacturing._2010_09.services import ImportExportService as imp43
from tcsoa.gen.Manufacturing._2015_03.services import StructureManagementService as imp44
from tcsoa.gen.Manufacturing._2009_10.services import StructureSearchService as imp45
from tcsoa.gen.Manufacturing._2019_06.services import DataManagementService as imp46
from tcsoa.gen.Manufacturing._2014_06.services import StructureSearchService as imp47
from tcsoa.gen.Manufacturing._2014_12.services import ModelService as imp48
from tcsoa.base import TcService


class DataManagementService(TcService):
    addAssociatedContexts = imp0.addAssociatedContexts
    addOrRemoveAssociatedContexts = imp1.addOrRemoveAssociatedContexts
    applyConfigObjects = imp3.applyConfigObjects
    associateAndAllocateByPreview = imp0.associateAndAllocateByPreview
    automaticAllocatePreview = imp0.automaticAllocatePreview
    automaticAssociateAndAllocate = imp0.automaticAssociateAndAllocate
    cloneAssemblyAndProcessObjects = imp1.cloneAssemblyAndProcessObjects
    closeContexts = imp10.closeContexts
    closeViews = imp10.closeViews
    connectObjects = imp0.connectObjects
    createAttachments = imp15.createAttachments
    createObjects = imp17.createObjects
    createOrUpdateConfigObjects = imp3.createOrUpdateConfigObjects
    createOrUpdateMEActivityFolders = imp19.createOrUpdateMEActivityFolders
    createOrUpdateMENXObjects = imp19.createOrUpdateMENXObjects
    disconnectFromOrigin = imp0.disconnectFromOrigin
    disconnectObjects = imp17.disconnectObjects
    establishOriginLink = imp1.establishOriginLink
    getAssociatedContexts = imp0.getAssociatedContexts
    getConnectorInfo = imp32.getConnectorInfo
    getOccurrenceKinematicsInformation = imp35.getOccurrenceKinematicsInformation
    getPhysicalAttachmentsInScope = imp32.getPhysicalAttachmentsInScope
    getProcessResourceRelatedInfo = imp1.getProcessResourceRelatedInfo
    openContexts = imp10.openContexts
    openViews = imp10.openViews
    publishSelectionFromStudyToSource = imp46.publishSelectionFromStudyToSource
    removePhysicalAttachementRelation = imp32.removePhysicalAttachementRelation
    setAttributes = imp15.setAttributes
    setConnectorInfo = imp32.setConnectorInfo
    setOccurrenceKinematicsInformation = imp35.setOccurrenceKinematicsInformation
    setPhysicalAttachementsInScope = imp32.setPhysicalAttachementsInScope
    syncSelectionInStudyWithSource = imp46.syncSelectionInStudyWithSource
    syncStudyAndSource = imp15.syncStudyAndSource


class TimeManagementService(TcService):
    allocatedTimeRollUp = imp2.allocatedTimeRollUp
    calculateCriticalPathEx = imp5.calculateCriticalPathEx
    getActivityTimes = imp5.getActivityTimes
    populateAllocatedTimeProperties = imp5.populateAllocatedTimeProperties
    timeAnalysisRollup = imp2.timeAnalysisRollup
    updateTimeManagementProperties = imp5.updateTimeManagementProperties


class ModelService(TcService):
    calculateCriticalPath = imp4.calculateCriticalPath
    computeAppearancePath = imp12.computeAppearancePath
    createFlow = imp4.createFlow
    editLogicalAssignments = imp4.editLogicalAssignments
    getCandidateToolsForToolRequirement = imp31.getCandidateToolsForToolRequirement
    getResolvedNodesFromLA = imp4.getResolvedNodesFromLA
    getToolRequirements = imp31.getToolRequirements
    removeFlow = imp4.removeFlow
    resolveLogicalAssignments = imp4.resolveLogicalAssignments
    resolveToolRequirement = imp31.resolveToolRequirement
    updateFlows = imp31.updateFlows
    validateScopeFlowsConsistency = imp48.validateScopeFlowsConsistency


class CoreService(TcService):
    cancelManufacturingCheckout = imp6.cancelManufacturingCheckout
    findCheckedOutsInStructure = imp26.findCheckedOutsInStructure
    findNodeInContext = imp27.findNodeInContext
    findNodeInContext2 = imp28.findNodeInContext
    getAffectedProperties = imp27.getAffectedProperties
    matchObjectsAgainstVariantRules = imp28.matchObjectsAgainstVariantRules


class ResourceManagementService(TcService):
    checkToolParameters = imp7.checkToolParameters
    getStepP21FileCounts = imp38.getStepP21FileCounts
    getVendorCatalogInfo = imp38.getVendorCatalogInfo
    importStep3DModels = imp38.importStep3DModels
    importStepP21Files = imp38.importStepP21Files
    importVendorCatalogHierarchy = imp38.importVendorCatalogHierarchy
    updateNXToolAssemblies = imp38.updateNXToolAssemblies


class IPAManagementService(TcService):
    cleanIPATree = imp8.cleanIPATree
    deleteFilteredIPA = imp20.deleteFilteredIPA
    deletefilteredIPA = imp21.deletefilteredIPA
    doesIPAExist = imp8.doesIPAExist
    findAndRepopulateDynamicIPAs = imp25.findAndRepopulateDynamicIPAs
    generateIPATree = imp8.generateIPATree
    generateSearchScope = imp21.generateSearchScope
    getFilteredIPA = imp21.getFilteredIPA
    getFilteredIPAType = imp20.getFilteredIPAType
    localUpdateIPATree = imp8.localUpdateIPATree
    repopulateDynamicIPAs = imp25.repopulateDynamicIPAs
    saveSearchResult = imp21.saveSearchResult
    updateIPATree = imp8.updateIPATree


class StructureManagementService(TcService):
    closeAttachmentWindow = imp9.closeAttachmentWindow
    copyEBOPStructure = imp13.copyEBOPStructure
    copyRecursively = imp14.copyRecursively
    createCollabPlanningContext = imp16.createCollabPlanningContext
    createOrUpdateAttachments = imp9.createOrUpdateAttachments
    deleteAttachments = imp9.deleteAttachments
    findAffectedCCs = imp24.findAffectedCCs
    getAttachmentLineChildren = imp9.getAttachmentLineChildren
    getBOMLineActivities = imp9.getBOMLineActivities
    getBOMLineAttachments = imp9.getBOMLineAttachments
    getReferenceContexts = imp37.getReferenceContexts
    getStructureContextActivityLines = imp9.getStructureContextActivityLines
    getStructureContextLines = imp13.getStructureContextLines
    getStructureContextTopLines = imp9.getStructureContextTopLines
    moveAndResequenceNodes = imp44.moveAndResequenceNodes
    pasteDuplicateStructure = imp13.pasteDuplicateStructure
    pasteDuplicateStructure2 = imp14.pasteDuplicateStructure
    setReferenceContexts = imp37.setReferenceContexts


class MFGPropertyCollectorService(TcService):
    collectProperties = imp11.collectProperties


class StructureSearchService(TcService):
    createOrUpdateAssignmentRecipe = imp18.createOrUpdateAssignmentRecipe
    deleteAssignmentRecipes = imp18.deleteAssignmentRecipes
    findStudies = imp29.findStudies
    getAssignmentRecipes = imp18.getAssignmentRecipes
    nextSearch = imp45.nextSearch
    resolveAssignmentRecipe = imp18.resolveAssignmentRecipe
    searchConnectedLines = imp47.searchConnectedLines
    startSearch = imp45.startSearch
    stopSearch = imp45.stopSearch


class ValidationService(TcService):
    executeValidations = imp22.executeValidations
    getAllRegisteredCallbacks = imp30.getAllRegisteredCallbacks
    getAllValidations = imp22.getAllValidations
    getMaturityReport = imp34.getMaturityReport


class ImportExportService(TcService):
    exportToBriefcase = imp23.exportToBriefcase
    importFromBriefcase = imp40.importFromBriefcase
    importManufacturingFeatures = imp41.importManufacturingFeatures
    importManufacturingFeatures2 = imp42.importManufacturingFeatures
    importManufacturingFeatures3 = imp23.importManufacturingFeatures
    importManufaturingFeatures = imp43.importManufaturingFeatures


class ModelDefinitionsService(TcService):
    getManufacturingPropretyDescs = imp33.getManufacturingPropretyDescs
    getValidRelationTypes = imp33.getValidRelationTypes


class ConstraintsService(TcService):
    getPrecedenceConstraintPaths = imp36.getPrecedenceConstraintPaths
    getPrecedenceConstraints = imp36.getPrecedenceConstraints
    validateConstraintConsistency = imp36.validateConstraintConsistency
    validateProcessAreaAssignments = imp36.validateProcessAreaAssignments


class TimeWayPlanService(TcService):
    getTWPInformation = imp39.getTWPInformation
    setProductImage = imp39.setProductImage
