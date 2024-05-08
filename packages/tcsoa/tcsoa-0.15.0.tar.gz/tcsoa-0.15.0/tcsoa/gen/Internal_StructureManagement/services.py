from tcsoa.gen.Internal_StructureManagement._2007_06.services import GlobalAlternateService as imp0
from tcsoa.gen.Internal_StructureManagement._2016_03.services import StructureVerificationService as imp1
from tcsoa.gen.Internal_StructureManagement._2010_04.services import BOMMarkupService as imp2
from tcsoa.gen.Internal_StructureManagement._2019_06.services import VariantManagementService as imp3
from tcsoa.gen.Internal_StructureManagement._2015_10.services import VariantManagementService as imp4
from tcsoa.gen.Internal_StructureManagement._2008_06.services import StructureService as imp5
from tcsoa.gen.Internal_StructureManagement._2007_06.services import PublishByLinkService as imp6
from tcsoa.gen.Internal_StructureManagement._2011_06.services import StructureService as imp7
from tcsoa.gen.Internal_StructureManagement._2021_12.services import EffectivitiesManagementService as imp8
from tcsoa.gen.Internal_StructureManagement._2009_10.services import EffectivitiesManagementService as imp9
from tcsoa.gen.Internal_StructureManagement._2022_12.services import StructureService as imp10
from tcsoa.gen.Internal_StructureManagement._2014_12.services import StructureVerificationService as imp11
from tcsoa.gen.Internal_StructureManagement._2020_05.services import RevisionRuleAdministrationService as imp12
from tcsoa.gen.Internal_StructureManagement._2023_06.services import RevisionRuleAdministrationService as imp13
from tcsoa.gen.Internal_StructureManagement._2016_10.services import EffectivityService as imp14
from tcsoa.gen.Internal_StructureManagement._2013_05.services import StructureExpansionLiteService as imp15
from tcsoa.gen.Internal_StructureManagement._2013_12.services import StructureExpansionLiteService as imp16
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureExpansionLiteService as imp17
from tcsoa.gen.Internal_StructureManagement._2012_02.services import StructureVerificationService as imp18
from tcsoa.gen.Internal_StructureManagement._2011_06.services import IncrementalChangeService as imp19
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureVerificationService as imp20
from tcsoa.gen.Internal_StructureManagement._2011_06.services import VariantManagementService as imp21
from tcsoa.gen.Internal_StructureManagement._2014_12.services import BrokenLinksService as imp22
from tcsoa.gen.Internal_StructureManagement._2007_12.services import BrokenLinksService as imp23
from tcsoa.gen.Internal_StructureManagement._2018_11.services import StructureVerificationService as imp24
from tcsoa.gen.Internal_StructureManagement._2012_09.services import StructureVerificationService as imp25
from tcsoa.gen.Internal_StructureManagement._2018_11.services import MassUpdateService as imp26
from tcsoa.gen.Internal_StructureManagement._2007_06.services import RestructureService as imp27
from tcsoa.gen.Internal_StructureManagement._2017_05.services import StructureLiteConversionService as imp28
from tcsoa.gen.Internal_StructureManagement._2008_05.services import RestructureService as imp29
from tcsoa.gen.Internal_StructureManagement._2014_12.services import RestructureService as imp30
from tcsoa.gen.Internal_StructureManagement._2008_03.services import StructureService as imp31
from tcsoa.gen.Internal_StructureManagement._2010_09.services import StructureService as imp32
from tcsoa.gen.Internal_StructureManagement._2007_06.services import RedliningService as imp33
from tcsoa.gen.Internal_StructureManagement._2008_05.services import StructureService as imp34
from tcsoa.base import TcService


class GlobalAlternateService(TcService):
    addRelatedGlobalAlternates = imp0.addRelatedGlobalAlternates
    listGlobalAlternates = imp0.listGlobalAlternates
    removeRelatedGlobalAlternates = imp0.removeRelatedGlobalAlternates
    setPreferredGlobalAlternate = imp0.setPreferredGlobalAlternate


class StructureVerificationService(TcService):
    alignMatchedCandidates = imp1.alignMatchedCandidates
    createOrUpdatePropagationDetails = imp11.createOrUpdatePropagationDetails
    createOrUpdateReviewStatus = imp11.createOrUpdateReviewStatus
    findMatchingCandidates = imp1.findMatchingCandidates
    findReviewStatus = imp11.findReviewStatus
    getActivitiesComparisonDetails = imp18.getActivitiesComparisonDetails
    getAttachmentComparisonDetails = imp20.getAttachmentComparisonDetails
    getMountAttachComparisonDetails = imp24.getMountAttachComparisonDetails
    getPropertyPropagationStatusDetails = imp11.getPropertyPropagationStatusDetails
    getStructureChangeDetails = imp11.getStructureChangeDetails
    getStructureChangeImpactedLines = imp11.getStructureChangeImpactedLines
    getToolRequirementComparisonDetails = imp18.getToolRequirementComparisonDetails
    getValidCriteria = imp25.getValidCriteria


class BOMMarkupService(TcService):
    applyBOMMarkup = imp2.applyBOMMarkup
    createBOMMarkup = imp2.createBOMMarkup
    savePendingEditsAsMarkup = imp2.savePendingEditsAsMarkup


class VariantManagementService(TcService):
    applyRollupVariantConfiguration = imp3.applyRollupVariantConfiguration
    applyVariantConfiguration = imp4.applyVariantConfiguration
    getBOMVariantConfigOptions = imp21.getBOMVariantConfigOptions
    getModularOptionsForBom = imp21.getModularOptionsForBom


class StructureService(TcService):
    copyRecursively = imp5.copyRecursively
    createOrSavePSBOMViewRevision = imp7.createOrSavePSBOMViewRevision
    createOrUpdateOccAttrObjects = imp10.createOrUpdateOccAttrObjects
    findHighestFindNumberInExpand = imp5.findHighestFindNumberInExpand
    getAvailableViewTypes = imp7.getAvailableViewTypes
    getOccAttrsObjects = imp10.getOccAttrsObjects
    resequence = imp31.resequence
    resequence2 = imp32.resequence
    syncAlignedOccurrences = imp34.syncAlignedOccurrences


class PublishByLinkService(TcService):
    createIDCWindowForDesignAsm = imp6.createIDCWindowForDesignAsm


class EffectivitiesManagementService(TcService):
    createOrUpdateDateEffectivities = imp8.createOrUpdateDateEffectivities
    createOrUpdateEffectivites = imp9.createOrUpdateEffectivites
    getEffectivityGrpRevList = imp9.getEffectivityGrpRevList
    setEndItemEffectivityGroups = imp9.setEndItemEffectivityGroups


class RevisionRuleAdministrationService(TcService):
    createOrUpdateRevisionRule = imp12.createOrUpdateRevisionRule
    createOrUpdateRevisionRule2 = imp13.createOrUpdateRevisionRule2
    getRevisionRuleInfo = imp12.getRevisionRuleInfo
    getRevisionRuleInfo2 = imp13.getRevisionRuleInfo2


class EffectivityService(TcService):
    cutbackUnitOccurrenceEffectivity = imp14.cutbackUnitOccurrenceEffectivity
    getUnitNetOccurrenceEffectivity = imp14.getUnitNetOccurrenceEffectivity


class StructureExpansionLiteService(TcService):
    expandBasedOnOccurrenceList = imp15.expandBasedOnOccurrenceList
    expandBasedOnOccurrenceList2 = imp16.expandBasedOnOccurrenceList2
    expandNext = imp15.expandNext
    expandNext2 = imp16.expandNext2
    expandNext3 = imp17.expandNext3
    getUndelivered = imp15.getUndelivered
    getUndelivered2 = imp16.getUndelivered2
    getUndelivered3 = imp17.getUndelivered3
    unloadBelow = imp15.unloadBelow
    unloadBelow2 = imp16.unloadBelow2


class IncrementalChangeService(TcService):
    getAttachmentChanges = imp19.getAttachmentChanges
    getAttributeChanges = imp19.getAttributeChanges
    getParentAndChildComponents = imp19.getParentAndChildComponents
    getPredecessorChanges = imp19.getPredecessorChanges
    getStructureChanges = imp19.getStructureChanges


class BrokenLinksService(TcService):
    getBrokenLinkAndReplacements = imp22.getBrokenLinkAndReplacements
    getBrokenLinkInfoWithFixOpt = imp23.getBrokenLinkInfoWithFixOpt
    repairBrokenLinks = imp23.repairBrokenLinks


class MassUpdateService(TcService):
    hasActiveMarkupAssociated = imp26.hasActiveMarkupAssociated
    saveImpactedAssemblies = imp26.saveImpactedAssemblies


class RestructureService(TcService):
    insertLevel = imp27.insertLevel
    moveNode = imp27.moveNode
    removeLevel = imp27.removeLevel
    replaceInContext = imp29.replaceInContext
    replaceItems = imp30.replaceItems
    splitOccurrence = imp27.splitOccurrence


class StructureLiteConversionService(TcService):
    liteBOMLinesToBOMLines = imp28.liteBOMLinesToBOMLines


class RedliningService(TcService):
    revertAllPendingEdits = imp33.revertAllPendingEdits
    revertPendingEdits = imp33.revertPendingEdits
