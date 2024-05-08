from tcsoa.gen.Internal_Core._2018_11.services import LogicalObjectService as imp0
from tcsoa.gen.Internal_Core._2020_04.services import LogicalObjectService as imp1
from tcsoa.gen.Internal_Core._2017_11.services import LogicalObjectService as imp2
from tcsoa.gen.Internal_Core._2018_06.services import LogicalObjectService as imp3
from tcsoa.gen.Internal_Core._2020_01.services import ActiveModelerService as imp4
from tcsoa.gen.Internal_Core._2008_06.services import SessionService as imp5
from tcsoa.gen.Internal_Core._2008_06.services import FileManagementService as imp6
from tcsoa.gen.Internal_Core._2010_09.services import FileManagementService as imp7
from tcsoa.gen.Internal_Core._2008_06.services import DataManagementService as imp8
from tcsoa.gen.Internal_Core._2008_06.services import DispatcherManagementService as imp9
from tcsoa.gen.Internal_Core._2012_10.services import DataManagementService as imp10
from tcsoa.gen.Internal_Core._2008_03.services import SessionService as imp11
from tcsoa.gen.Internal_Core._2021_06.services import DataManagementService as imp12
from tcsoa.gen.Internal_Core._2007_01.services import DataManagementService as imp13
from tcsoa.gen.Internal_Core._2010_09.services import DataManagementService as imp14
from tcsoa.gen.Internal_Core._2021_06.services import FileManagementService as imp15
from tcsoa.gen.Internal_Core._2013_05.services import ProjectLevelSecurityService as imp16
from tcsoa.gen.Internal_Core._2007_06.services import ProjectLevelSecurityService as imp17
from tcsoa.gen.Internal_Core._2013_05.services import LicensingService as imp18
from tcsoa.gen.Internal_Core._2014_10.services import FileManagementService as imp19
from tcsoa.gen.Internal_Core._2017_05.services import FileManagementService as imp20
from tcsoa.gen.Internal_Core._2010_04.services import ProjectLevelSecurityService as imp21
from tcsoa.gen.Internal_Core._2007_12.services import SessionService as imp22
from tcsoa.gen.Internal_Core._2014_11.services import SessionService as imp23
from tcsoa.gen.Internal_Core._2013_05.services import PresentationManagementService as imp24
from tcsoa.gen.Internal_Core._2017_05.services import PresentationManagementService as imp25
from tcsoa.gen.Internal_Core._2017_11.services import TypeService as imp26
from tcsoa.gen.Internal_Core._2010_04.services import DataManagementService as imp27
from tcsoa.gen.Internal_Core._2017_11.services import DataManagementService as imp28
from tcsoa.gen.Internal_Core._2009_10.services import ThumbnailService as imp29
from tcsoa.gen.Internal_Core._2013_05.services import ThumbnailService as imp30
from tcsoa.gen.Internal_Core._2018_11.services import FileManagementService as imp31
from tcsoa.gen.Internal_Core._2012_02.services import DataManagementService as imp32
from tcsoa.gen.Internal_Core._2006_03.services import SessionService as imp33
from tcsoa.gen.Internal_Core._2011_06.services import ICTService as imp34
from tcsoa.gen.Internal_Core._2021_12.services import DataManagementService as imp35
from tcsoa.gen.Internal_Core._2007_05.services import SessionService as imp36
from tcsoa.gen.Internal_Core._2016_10.services import DataManagementService as imp37
from tcsoa.gen.Internal_Core._2012_09.services import EnvelopeService as imp38
from tcsoa.gen.Internal_Core._2014_10.services import LicensingService as imp39
from tcsoa.gen.Internal_Core._2018_12.services import LicensingService as imp40
from tcsoa.gen.Internal_Core._2010_04.services import StructureManagementService as imp41
from tcsoa.gen.Internal_Core._2007_09.services import DataManagementService as imp42
from tcsoa.base import TcService


class LogicalObjectService(TcService):
    addIncludedLogicalObjects = imp0.addIncludedLogicalObjects
    addMemAndPresentedPropsWithWrite = imp1.addMemAndPresentedPropsWithWrite
    addMembersAndPresentedProps = imp2.addMembersAndPresentedProps
    addMembersAndPresentedProps2 = imp3.addMembersAndPresentedProps2
    createLogicalObjectTypes = imp2.createLogicalObjectTypes
    createLogicalObjectTypes2 = imp3.createLogicalObjectTypes2
    deleteLogicalObjectTypes = imp2.deleteLogicalObjectTypes
    deleteMembersAndPresentedProps = imp2.deleteMembersAndPresentedProps
    updateMembers = imp3.updateMembers


class ActiveModelerService(TcService):
    addPropertiesOnTypes = imp4.addPropertiesOnTypes
    createTypes = imp4.createTypes


class SessionService(TcService):
    cancelOperation = imp5.cancelOperation
    disableUserSessionState = imp11.disableUserSessionState
    getProperties = imp22.getProperties
    getSecurityToken = imp23.getSecurityToken
    initTypeByNames = imp33.initTypeByNames
    initTypeByUids = imp33.initTypeByUids
    refreshPOMCachePerRequestDeprecated = imp36.refreshPOMCachePerRequestDeprecated


class FileManagementService(TcService):
    commitRegularFiles = imp6.commitRegularFiles
    commitReplacedFiles = imp7.commitReplacedFiles
    getDatasetTicketsForChunkedUpload = imp15.getDatasetTicketsForChunkedUpload
    getFileTransferTickets = imp6.getFileTransferTickets
    getPlmdFileTicketForDownload = imp19.getPlmdFileTicketForDownload
    getPlmdFileTicketForReplace = imp20.getPlmdFileTicketForReplace
    getPlmdFileTicketForUpload = imp19.getPlmdFileTicketForUpload
    getRegularFileTicketsForUpload = imp6.getRegularFileTicketsForUpload
    getTransientFileTicketsForDownload = imp31.getTransientFileTicketsForDownload
    getTransientTicketsForChunkedUpload = imp15.getTransientTicketsForChunkedUpload
    getWriteTickets = imp6.getWriteTickets
    postCleanUpFileCommits = imp19.postCleanUpFileCommits
    updateImanFileCommits = imp6.updateImanFileCommits


class DataManagementService(TcService):
    createCachedRelations = imp8.createCachedRelations
    createRelateAndSubmitObjects = imp10.createRelateAndSubmitObjects
    generateDatasetName = imp12.generateDatasetName
    getAttributeValues = imp13.getAttributeValues
    getDatasetFiles = imp14.getDatasetFiles
    getOrganizationInformation = imp13.getOrganizationInformation
    getSubscribableTypesAndSubTypes = imp27.getSubscribableTypesAndSubTypes
    getTCSessionAnalyticsInfo = imp28.getTCSessionAnalyticsInfo
    getViewableData = imp32.getViewableData
    multiRelationMultiLevelExpand = imp8.multiRelationMultiLevelExpand
    queryForFileExistence = imp35.queryForFileExistence
    reviseObject = imp8.reviseObject
    reviseObjectsInBulk = imp37.reviseObjectsInBulk
    saveAsNewItemObject = imp8.saveAsNewItemObject
    saveAsObjectsInBulkAndRelate = imp37.saveAsObjectsInBulkAndRelate
    setDefaultProjectForProjectMembers = imp8.setDefaultProjectForProjectMembers
    whereUsedOccGroup = imp42.whereUsedOccGroup


class DispatcherManagementService(TcService):
    createDatasetOfVersion = imp9.createDatasetOfVersion
    insertDatasetVersion = imp9.insertDatasetVersion
    queryDispatcherRequests = imp9.queryDispatcherRequests
    updateDispatcherRequests = imp9.updateDispatcherRequests


class ProjectLevelSecurityService(TcService):
    getFilteredObjectsInProject = imp16.getFilteredObjectsInProject
    getFilteredProjectData = imp17.getFilteredProjectData
    getProjectsSmartFolderHierarchy = imp17.getProjectsSmartFolderHierarchy
    getProjectsSmartFolderHierarchy2 = imp21.getProjectsSmartFolderHierarchy2
    getTopLevelSmartFolderHierarchy = imp17.getTopLevelSmartFolderHierarchy


class LicensingService(TcService):
    getLicenseBundles = imp18.getLicenseBundles
    updateLicenseServer = imp39.updateLicenseServer
    updateLicenseServer2 = imp40.updateLicenseServer2


class PresentationManagementService(TcService):
    getSharedCommonClientFiles = imp24.getSharedCommonClientFiles
    getStylesheet = imp24.getStylesheet
    getStylesheetPerPage = imp25.getStylesheetPerPage


class TypeService(TcService):
    getSubTypeHierarchicalTrees = imp26.getSubTypeHierarchicalTrees


class ThumbnailService(TcService):
    getThumbnailFileTickets = imp29.getThumbnailFileTickets
    getThumbnailFileTickets2 = imp30.getThumbnailFileTickets2
    updateThumbnail = imp29.updateThumbnail


class ICTService(TcService):
    invokeICTMethod = imp34.invokeICTMethod


class EnvelopeService(TcService):
    sendEmail = imp38.sendEmail


class StructureManagementService(TcService):
    validateInStructureAssociations = imp41.validateInStructureAssociations
