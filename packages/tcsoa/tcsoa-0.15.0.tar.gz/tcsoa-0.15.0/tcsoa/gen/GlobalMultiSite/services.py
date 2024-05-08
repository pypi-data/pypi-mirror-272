from tcsoa.gen.GlobalMultiSite._2007_06.services import SiteReservationService as imp0
from tcsoa.gen.GlobalMultiSite._2011_06.services import ImportExportService as imp1
from tcsoa.gen.GlobalMultiSite._2007_06.services import ImportExportService as imp2
from tcsoa.gen.GlobalMultiSite._2021_06.services import ImportExportService as imp3
from tcsoa.gen.GlobalMultiSite._2022_06.services import ImportExportService as imp4
from tcsoa.gen.GlobalMultiSite._2008_06.services import ImportExportService as imp5
from tcsoa.gen.GlobalMultiSite._2010_04.services import ImportExportService as imp6
from tcsoa.gen.GlobalMultiSite._2007_12.services import ImportExportService as imp7
from tcsoa.gen.GlobalMultiSite._2020_04.services import ImportExportService as imp8
from tcsoa.base import TcService


class SiteReservationService(TcService):
    cancelSiteCheckOut = imp0.cancelSiteCheckOut
    siteCheckIn = imp0.siteCheckIn
    siteCheckOut = imp0.siteCheckOut


class ImportExportService(TcService):
    createGSIdentities = imp1.createGSIdentities
    createOrUpdateActionRules = imp2.createOrUpdateActionRules
    createOrUpdateClosureRules = imp2.createOrUpdateClosureRules
    createOrUpdateFilterRules = imp2.createOrUpdateFilterRules
    createOrUpdatePropertySets = imp2.createOrUpdatePropertySets
    createOrUpdateTransferModes = imp2.createOrUpdateTransferModes
    createOrUpdateTransferOptionSets = imp2.createOrUpdateTransferOptionSets
    exportFilesOffline = imp3.exportFilesOffline
    exportFilesOffline2 = imp4.exportFilesOffline2
    exportObjectsToOfflinePackage = imp5.exportObjectsToOfflinePackage
    exportObjectsToPLMXML = imp6.exportObjectsToPLMXML
    getActionRules = imp2.getActionRules
    getAllTransferOptionSets = imp2.getAllTransferOptionSets
    getAvailableTransferOptionSets = imp2.getAvailableTransferOptionSets
    getClosureRules = imp2.getClosureRules
    getFilterRules = imp2.getFilterRules
    getHashedUID = imp1.getHashedUID
    getPropertySets = imp2.getPropertySets
    getRemoteSites = imp7.getRemoteSites
    getTransferModes = imp2.getTransferModes
    importNXFiles = imp3.importNXFiles
    importObjectsFromOfflinePackage = imp5.importObjectsFromOfflinePackage
    importObjectsFromPLMXML = imp6.importObjectsFromPLMXML
    importObjectsFromPLMXMLWithDSM = imp8.importObjectsFromPLMXMLWithDSM
    requestExportToRemoteSites = imp7.requestExportToRemoteSites
    requestImportFromOfflinePackage = imp2.requestImportFromOfflinePackage
    requestImportFromRemoteSites = imp7.requestImportFromRemoteSites
