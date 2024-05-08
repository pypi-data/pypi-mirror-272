from tcsoa.gen.Core._2014_10.services import DataManagementService as imp0
from tcsoa.gen.Core._2021_06.services import DataManagementService as imp1
from tcsoa.gen.Core._2021_12.services import SessionService as imp2
from tcsoa.gen.Core._2020_01.services import ProjectLevelSecurityService as imp3
from tcsoa.gen.Core._2008_06.services import DataManagementService as imp4
from tcsoa.gen.Core._2014_06.services import DigitalSignatureService as imp5
from tcsoa.gen.Core._2007_09.services import ProjectLevelSecurityService as imp6
from tcsoa.gen.Core._2017_05.services import ProjectLevelSecurityService as imp7
from tcsoa.gen.Core._2014_06.services import ReservationService as imp8
from tcsoa.gen.Core._2012_02.services import DataManagementService as imp9
from tcsoa.gen.Core._2006_03.services import ReservationService as imp10
from tcsoa.gen.Core._2006_03.services import DataManagementService as imp11
from tcsoa.gen.Core._2018_11.services import ProjectLevelSecurityService as imp12
from tcsoa.gen.Core._2006_03.services import FileManagementService as imp13
from tcsoa.gen.Core._2017_05.services import FileManagementService as imp14
from tcsoa.gen.Core._2008_03.services import SessionService as imp15
from tcsoa.gen.Core._2012_09.services import ProjectLevelSecurityService as imp16
from tcsoa.gen.Core._2007_12.services import DataManagementService as imp17
from tcsoa.gen.Core._2016_09.services import DataManagementService as imp18
from tcsoa.gen.Core._2010_04.services import DataManagementService as imp19
from tcsoa.gen.Core._2008_06.services import DispatcherManagementService as imp20
from tcsoa.gen.Core._2020_01.services import DataManagementService as imp21
from tcsoa.gen.Core._2008_06.services import StructureManagementService as imp22
from tcsoa.gen.Core._2018_06.services import DataManagementService as imp23
from tcsoa.gen.Core._2007_01.services import DataManagementService as imp24
from tcsoa.gen.Core._2010_09.services import DataManagementService as imp25
from tcsoa.gen.Core._2015_07.services import DataManagementService as imp26
from tcsoa.gen.Core._2007_01.services import ManagedRelationsService as imp27
from tcsoa.gen.Core._2007_06.services import DataManagementService as imp28
from tcsoa.gen.Core._2007_09.services import DataManagementService as imp29
from tcsoa.gen.Core._2016_05.services import DataManagementService as imp30
from tcsoa.gen.Core._2020_04.services import DataManagementService as imp31
from tcsoa.gen.Core._2013_05.services import DataManagementService as imp32
from tcsoa.gen.Core._2010_04.services import LanguageInformationService as imp33
from tcsoa.gen.Core._2007_06.services import LOVService as imp34
from tcsoa.gen.Core._2007_06.services import PropDescriptorService as imp35
from tcsoa.gen.Core._2011_06.services import PropDescriptorService as imp36
from tcsoa.gen.Core._2006_03.services import SessionService as imp37
from tcsoa.gen.Core._2011_06.services import SessionService as imp38
from tcsoa.gen.Core._2008_06.services import PropDescriptorService as imp39
from tcsoa.gen.Core._2012_10.services import DataManagementService as imp40
from tcsoa.gen.Core._2012_02.services import OperationDescriptorService as imp41
from tcsoa.gen.Core._2016_10.services import ProjectLevelSecurityService as imp42
from tcsoa.gen.Core._2015_10.services import FileManagementService as imp43
from tcsoa.gen.Core._2008_06.services import SessionService as imp44
from tcsoa.gen.Core._2013_05.services import LOVService as imp45
from tcsoa.gen.Core._2009_10.services import DataManagementService as imp46
from tcsoa.gen.Core._2011_06.services import LOVService as imp47
from tcsoa.gen.Core._2017_11.services import LogicalObjectService as imp48
from tcsoa.gen.Core._2018_06.services import LogicalObjectService as imp49
from tcsoa.gen.Core._2018_11.services import LogicalObjectService as imp50
from tcsoa.gen.Core._2008_06.services import ManagedRelationsService as imp51
from tcsoa.gen.Core._2007_01.services import SessionService as imp52
from tcsoa.gen.Core._2010_04.services import SessionService as imp53
from tcsoa.gen.Core._2011_06.services import OperationDescriptorService as imp54
from tcsoa.gen.Core._2011_06.services import DataManagementService as imp55
from tcsoa.gen.Core._2014_06.services import DataManagementService as imp56
from tcsoa.gen.Core._2007_01.services import FileManagementService as imp57
from tcsoa.gen.Core._2015_10.services import SessionService as imp58
from tcsoa.gen.Core._2009_10.services import ProjectLevelSecurityService as imp59
from tcsoa.gen.Core._2019_06.services import SessionService as imp60
from tcsoa.gen.Core._2009_04.services import ProjectLevelSecurityService as imp61
from tcsoa.gen.Core._2011_06.services import ReservationService as imp62
from tcsoa.gen.Core._2014_10.services import ProjectLevelSecurityService as imp63
from tcsoa.gen.Core._2015_10.services import DataManagementService as imp64
from tcsoa.gen.Core._2007_06.services import SessionService as imp65
from tcsoa.gen.Core._2012_02.services import SessionService as imp66
from tcsoa.gen.Core._2012_09.services import DataManagementService as imp67
from tcsoa.gen.Core._2011_06.services import EnvelopeService as imp68
from tcsoa.gen.Core._2007_12.services import SessionService as imp69
from tcsoa.gen.Core._2009_04.services import SessionService as imp70
from tcsoa.gen.Core._2022_12.services import SessionService as imp71
from tcsoa.gen.Core._2008_06.services import ReservationService as imp72
from tcsoa.gen.Core._2019_06.services import DataManagementService as imp73
from tcsoa.gen.Core._2008_05.services import DataManagementService as imp74
from tcsoa.gen.Core._2021_12.services import LOVService as imp75
from tcsoa.base import TcService


class DataManagementService(TcService):
    addChildren = imp0.addChildren
    addNamedReferenceToDatasets = imp1.addNamedReferenceToDatasets
    addParticipants = imp4.addParticipants
    bulkCreateObjects = imp9.bulkCreateObjects
    changeOwnership = imp11.changeOwnership
    createAlternateIdentifiers = imp17.createAlternateIdentifiers
    createAttachAndSubmitObjects = imp18.createAttachAndSubmitObjects
    createConnections = imp4.createConnections
    createDatasets = imp11.createDatasets
    createDatasets2 = imp19.createDatasets
    createDatasets3 = imp4.createDatasets2
    createFolders = imp11.createFolders
    createIdDisplayRules = imp21.createIdDisplayRules
    createItems = imp11.createItems
    createObjects = imp4.createObjects
    createObjectsInBulkAndRelate = imp23.createObjectsInBulkAndRelate
    createOrUpdateForms = imp24.createOrUpdateForms
    createOrUpdateGDELinks = imp4.createOrUpdateGDELinks
    createOrUpdateItemElements = imp4.createOrUpdateItemElements
    createOrUpdateRelations = imp4.createOrUpdateRelations
    createOrUpdateStaticTableData = imp25.createOrUpdateStaticTableData
    createRelateAndSubmitObjects2 = imp26.createRelateAndSubmitObjects2
    createRelations = imp11.createRelations
    deleteObjects = imp11.deleteObjects
    deleteRelations = imp11.deleteRelations
    expandGRMRelationsForPrimary = imp28.expandGRMRelationsForPrimary
    expandGRMRelationsForPrimary2 = imp29.expandGRMRelationsForPrimary
    expandGRMRelationsForSecondary = imp28.expandGRMRelationsForSecondary
    expandGRMRelationsForSecondary2 = imp29.expandGRMRelationsForSecondary
    findDisplayableSubBusinessObjects = imp4.findDisplayableSubBusinessObjects
    findDisplayableSubBusinessObjectsWithDisplayNames = imp19.findDisplayableSubBusinessObjectsWithDisplayNames
    generateContextSpecificIDs = imp30.generateContextSpecificIDs
    generateContextSpecificIDs2 = imp31.generateContextSpecificIDs2
    generateIdsUsingIDGenerationRules = imp0.generateIdsUsingIDGenerationRules
    generateItemIdsAndInitialRevisionIds = imp11.generateItemIdsAndInitialRevisionIds
    generateNextValues = imp32.generateNextValues
    generateNextValuesForProperties = imp26.generateNextValuesForProperties
    generateRevisionIds = imp11.generateRevisionIds
    generateUID = imp24.generateUID
    getAvailableTypes = imp28.getAvailableTypes
    getAvailableTypesWithDisplayNames = imp19.getAvailableTypesWithDisplayNames
    getChildren = imp32.getChildren
    getContextsAndIdentifierTypes = imp17.getContextsAndIdentifierTypes
    getCreatbleSubBuisnessObjectNames = imp26.getCreatbleSubBuisnessObjectNames
    getDatasetCreationRelatedInfo = imp24.getDatasetCreationRelatedInfo
    getDatasetCreationRelatedInfo2 = imp19.getDatasetCreationRelatedInfo2
    getDatasetTypeInfo = imp28.getDatasetTypeInfo
    getDatasetTypesWithFileExtension = imp40.getDatasetTypesWithFileExtension
    getDeepCopyData = imp0.getDeepCopyData
    getDeepCopyData2 = imp26.getDeepCopyData
    getDomainOfObjectOrType = imp26.getDomainOfObjectOrType
    getEventTypes = imp25.getEventTypes
    getIdContexts = imp21.getIdContexts
    getIdentifierTypes = imp21.getIdentifierTypes
    getItemAndRelatedObjects = imp4.getItemAndRelatedObjects
    getItemCreationRelatedInfo = imp24.getItemCreationRelatedInfo
    getItemFromAttribute = imp46.getItemFromAttribute
    getItemFromId = imp24.getItemFromId
    getLocalizedProperties = imp19.getLocalizedProperties
    getLocalizedProperties2 = imp26.getLocalizedProperties2
    getNRPatternsWithCounters = imp4.getNRPatternsWithCounters
    getNextIds = imp4.getNextIds
    getPasteRelations = imp32.getPasteRelations
    getPasteRelations2 = imp0.getPasteRelations2
    getProperties = imp11.getProperties
    getRevNRAttachDetails = imp4.getRevNRAttachDetails
    getStaticTableData = imp25.getStaticTableData
    getSubTypeNames = imp32.getSubTypeNames
    getTableProperties = imp46.getTableProperties
    getTraceReport = imp55.getTraceReport
    getTraceReport2 = imp40.getTraceReport
    getTraceReport3 = imp56.getTraceReport2
    getTraceReportLegacy = imp56.getTraceReportLegacy
    isPropertyLocalizable = imp19.isPropertyLocalizable
    listAlternateIdDisplayRules = imp17.listAlternateIdDisplayRules
    loadObjects = imp29.loadObjects
    moveToNewFolder = imp24.moveToNewFolder
    postEvent = imp25.postEvent
    pruneNamedReferences = imp0.pruneNamedReferences
    purgeSequences = imp28.purgeSequences
    reassignParticipants = imp64.reassignParticipants
    refreshObjects = imp24.refreshObjects
    refreshObjects2 = imp40.refreshObjects2
    removeChildren = imp0.removeChildren
    removeNamedReferenceFromDataset = imp29.removeNamedReferenceFromDataset
    removeNamedReferenceFromDataset2 = imp1.removeNamedReferenceFromDataset2
    removeParticipants = imp4.removeParticipants
    resetContextID = imp30.resetContextID
    revise = imp11.revise
    revise2 = imp4.revise2
    reviseObjects = imp32.reviseObjects
    saveAsNewItem = imp24.saveAsNewItem
    saveAsNewItem2 = imp4.saveAsNewItem2
    saveAsObjectAndRelate = imp67.saveAsObjectAndRelate
    saveAsObjects = imp55.saveAsObjects
    saveAsObjectsAndRelate = imp0.saveAsObjectsAndRelate
    setDisplayProperties = imp11.setDisplayProperties
    setLocalizedProperties = imp19.setLocalizedProperties
    setLocalizedPropertyValues = imp19.setLocalizedPropertyValues
    setOrRemoveImmunity = imp28.setOrRemoveImmunity
    setProperties = imp24.setProperties
    setProperties2 = imp25.setProperties
    setPropertiesAndDetectOverwrite = imp30.setPropertiesAndDetectOverwrite
    setTableProperties = imp46.setTableProperties
    unlinkAndDeleteObjects = imp73.unlinkAndDeleteObjects
    unloadObjects = imp74.unloadObjects
    validateAlternateIds = imp17.validateAlternateIds
    validateIdValue = imp9.validateIdValue
    validateItemIdsAndRevIds = imp28.validateItemIdsAndRevIds
    validateRevIds = imp55.validateRevIds
    validateValues = imp32.validateValues
    verifyExtension = imp25.verifyExtension
    whereReferenced = imp24.whereReferenced
    whereReferencedByRelationName = imp28.whereReferencedByRelationName
    whereUsed = imp24.whereUsed
    whereUsed2 = imp9.whereUsed


class SessionService(TcService):
    addObjectPropertyPolicies = imp2.addObjectPropertyPolicies
    connect = imp15.connect
    getAvailableServices = imp37.getAvailableServices
    getClientCacheData = imp38.getClientCacheData
    getDisplayStrings = imp44.getDisplayStrings
    getFavorites = imp15.getFavorites
    getGroupMembership = imp37.getGroupMembership
    getPreferences = imp37.getPreferences
    getPreferences2 = imp52.getPreferences
    getPreferences3 = imp53.getPreferences2
    getSessionGroupMember = imp37.getSessionGroupMember
    getShortcuts = imp53.getShortcuts
    getTCSessionInfo = imp52.getTCSessionInfo
    getTypeDescriptions = imp38.getTypeDescriptions
    getTypeDescriptions2 = imp58.getTypeDescriptions2
    licenseAdmin = imp60.licenseAdmin
    login = imp37.login
    login2 = imp44.login
    login3 = imp38.login
    loginSSO = imp37.loginSSO
    loginSSO2 = imp44.loginSSO
    loginSSO3 = imp38.loginSSO
    logout = imp37.logout
    refreshPOMCachePerRequest = imp65.refreshPOMCachePerRequest
    registerState = imp66.registerState
    setAndEvaluateIdDisplayRule = imp69.setAndEvaluateIdDisplayRule
    setFavorites = imp15.setFavorites
    setObjectPropertyPolicy = imp52.setObjectPropertyPolicy
    setObjectPropertyPolicy2 = imp44.setObjectPropertyPolicy
    setObjectPropertyPolicy3 = imp66.setObjectPropertyPolicy
    setPreferences = imp37.setPreferences
    setSessionGroupMember = imp37.setSessionGroupMember
    setUserSessionState = imp69.setUserSessionState
    setUserSessionStateAndUpdateDefaults = imp58.setUserSessionStateAndUpdateDefaults
    sponsoredLogin = imp58.sponsoredLogin
    sponsoredLoginSSO = imp58.sponsoredLoginSSO
    startOperation = imp70.startOperation
    stopOperation = imp70.stopOperation
    tcServerSleep = imp71.tcServerSleep
    unregisterState = imp66.unregisterState
    updateObjectPropertyPolicy = imp38.updateObjectPropertyPolicy


class ProjectLevelSecurityService(TcService):
    addOrRemoveProjectMembers = imp3.addOrRemoveProjectMembers
    assignOrRemoveObjects = imp6.assignOrRemoveObjects
    assignOrRemoveObjectsFromProjects = imp7.assignOrRemoveObjectsFromProjects
    changeOwningProgram = imp12.changeOwningProgram
    copyProjects = imp16.copyProjects
    copyProjects2 = imp7.copyProjects2
    createProjects = imp16.createProjects
    createProjects2 = imp7.createProjects2
    getDefaultProject = imp42.getDefaultProject
    getFirstLevelProjectTeamStructure = imp3.getFirstLevelProjectTeamStructure
    getModifiableProjects = imp3.getModifiableProjects
    getPrivilegeInProjects = imp3.getPrivilegeInProjects
    getProjectTeamChildNodes = imp3.getProjectTeamChildNodes
    getProjectTeams = imp16.getProjectTeams
    getProjectsForAssignOrRemove = imp7.getProjectsForAssignOrRemove
    getUserProjects = imp59.getUserProjects
    getUserProjects2 = imp12.getUserProjects2
    loadProjectDataForUser = imp61.loadProjectDataForUser
    modifyProjects = imp16.modifyProjects
    modifyProjects2 = imp7.modifyProjects2
    propagateData = imp63.propagateData
    setPropagationEnabledProperties = imp7.setPropagationEnabledProperties
    setUserPrivilege = imp3.setUserPrivilege


class DigitalSignatureService(TcService):
    applySignatures = imp5.applySignatures
    getSignatureMessages = imp5.getSignatureMessages
    voidSignatures = imp5.voidSignatures


class ReservationService(TcService):
    bulkCancelCheckout = imp8.bulkCancelCheckout
    bulkCheckin = imp8.bulkCheckin
    bulkCheckout = imp8.bulkCheckout
    cancelCheckout = imp10.cancelCheckout
    checkin = imp10.checkin
    checkout = imp10.checkout
    getReservationHistory = imp10.getReservationHistory
    okToCheckout = imp62.okToCheckout
    transferCheckout = imp72.transferCheckout


class FileManagementService(TcService):
    commitDatasetFiles = imp13.commitDatasetFiles
    commitDatasetFilesInBulk = imp14.commitDatasetFilesInBulk
    getDatasetWriteTickets = imp13.getDatasetWriteTickets
    getDigestInfoForDatasets = imp43.getDigestInfoForDatasets
    getDigestInfoForFiles = imp43.getDigestInfoForFiles
    getFileReadTickets = imp13.getFileReadTickets
    getTransientFileTicketsForUpload = imp57.getTransientFileTicketsForUpload
    replaceFiles = imp14.replaceFiles


class DispatcherManagementService(TcService):
    createDispatcherRequest = imp20.createDispatcherRequest


class StructureManagementService(TcService):
    createInStructureAssociations = imp22.createInStructureAssociations
    getPrimariesOfInStructureAssociation = imp22.getPrimariesOfInStructureAssociation
    getSecondariesOfInStructureAssociation = imp22.getSecondariesOfInStructureAssociation
    removeInStructureAssociations = imp22.removeInStructureAssociations


class ManagedRelationsService(TcService):
    createRelation = imp27.createRelation
    getManagedRelations = imp51.getManagedRelations
    getTraceReport = imp27.getTraceReport
    modifyRelation = imp27.modifyRelation


class LanguageInformationService(TcService):
    getAllTranslationStatuses = imp33.getAllTranslationStatuses
    getLanguagesList = imp33.getLanguagesList


class LOVService(TcService):
    getAttachedLOVs = imp34.getAttachedLOVs
    getInitialLOVValues = imp45.getInitialLOVValues
    getLOVAttachments = imp47.getLOVAttachments
    getNextLOVValues = imp45.getNextLOVValues
    validateLOVValueSelections = imp45.validateLOVValueSelections
    validatePropertyValuesForLOVInBulk = imp75.validatePropertyValuesForLOVInBulk


class PropDescriptorService(TcService):
    getAttachedPropDescs = imp35.getAttachedPropDescs
    getAttachedPropDescs2 = imp36.getAttachedPropDescs2
    getCreateDesc = imp39.getCreateDesc


class OperationDescriptorService(TcService):
    getDeepCopyData = imp41.getDeepCopyData
    getSaveAsDesc = imp54.getSaveAsDesc


class LogicalObjectService(TcService):
    getLogicalObjects = imp48.getLogicalObjects
    getLogicalObjects2 = imp49.getLogicalObjects2
    getLogicalObjectsWithContext = imp50.getLogicalObjectsWithContext


class EnvelopeService(TcService):
    sendAndDeleteEnvelopes = imp68.sendAndDeleteEnvelopes
