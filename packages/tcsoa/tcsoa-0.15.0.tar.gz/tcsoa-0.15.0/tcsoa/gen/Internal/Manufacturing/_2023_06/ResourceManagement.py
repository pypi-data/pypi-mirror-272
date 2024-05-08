from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2022_12.ResourceManagement import Import3DModelsInfo, ImportVendorProductsInfo, ImportVendorProductsInput
from typing import List
from tcsoa.gen.Manufacturing._2013_12.ResourceManagement import RMFileTicket
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class ICOToTargetClassMappings(TcBaseObj):
    """
    The object with information about the map ICO.
    
    :var sourceIcoID: The ID of the icm0 Internal Classification Objects (ICO) that should be mapped.
    :var targetItemName: The name of the item that the resource gets mapped to.
    :var targetClassID: The ID of the class where the ICO should be mapped to.
    """
    sourceIcoID: str = ''
    targetItemName: str = ''
    targetClassID: str = ''


@dataclass
class ImportVendorData2In(TcBaseObj):
    """
    The input structure for the importVendorData2 service operation.
    
    :var vendorPackageId: The ID of the vendor package that should be imported.
    This ID can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var vendorPackageDirectory: The vendor package root directory residing on the Teamcenter server.
    This directory can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var doCheckVendorProducts: If true, the operation checks whether products for the given vendor package were
    already imported and/or mapped. In the response object ImportVendorDataResponse2 the number of already imported
    products (importedProductCount) and number of mapped products (mappedProductCount) is returned. If false, nothing
    is checked.
    :var doImportVendorProducts: If true, the operation imports vendor products of the given package into the
    Classification vendor catalog classes inside the Teamcenter database. The system creates icm0 Internal
    Classification Objects (ICOs) in those classes.
    If you call this operation with the input parameters doCheckVendorProducts and doImportVendorProducts set to true
    and the check identifies that products were already imported, then this "import products" operation is not
    performed. If you want to force the product import a second time, set the input parameter doImportVendorProducts to
    true and doCheckVendorProducts to false.
    If false, no products are imported.
    :var doMapToSingleTargetClass: If true, the operation maps the icm0 objects from the vendor catalog classes into
    the Manufacturing Resource Library's (MRL) tool component classes. The vendor catalog classes contain catalog tool
    components. The MRL tool component classes contain those tool components that are actively used in the customer's
    shop floor.
    In the Classification Admin application there are mapping rules (bldb0 Mapping Views) defined that control which
    vendor class is mapped to what MRL class and which vendor attribute is mapped on what MRL attribute.
    During the mapping operation a new Item and a icm0 are created in the MRL sml0 class and the attribute values from
    the source icm0 are transferred to the target icm0. If the source component has a Dataset attached, it is copied to
    the new target component Item. 
    Note: If there are multiple target classes defined for a catalog tool component, the mapping is not performed.
    Corresponding information is written into the log file. The user can map it manually in the desired class.
    The imported products are identified using the vendor package ID in the icm0 attribute values. This allows to call
    the operation once with only input parameter doImportVendorProducts set to true and a second time with only input
    parameter doMapToSingleTargetClass set to true.
    This operation returns information about catalog components with multiple target classes. This information can be
    used to ask the user to select the desired target classes. Later the doMapToMultiTargetClasses operation can be
    called.
    If false, no products are mapped.
    :var doMapToMultiTargetClasses: If true, the operation maps the icm0 objects from the vendor catalog classes into
    the Manufacturing Resource Library's (MRL) tool component classes. The vendor catalog classes contain catalog tool
    components. The MRL tool component classes contain those tool components that are actively used in the customer's
    shop floor.
    In the Classification Admin application there are mapping rules (bldb0 Mapping Views) defined that control which
    vendor class is mapped to what MRL class and which vendor attribute is mapped on what MRL attribute.
    During the mapping operation a new Item and a icm0 are created in the MRL sml0 class and the attribute values from
    the source icm0 are transferred to the target icm0. If the source component has a Dataset attached, it is copied to
    the new target component Item. 
    Note: The mapping is only performed for catalog tool components that have multiple target classes defined.
    Corresponding information is written into the log file. The input parameter MapToMultiTargetClassesInput defines
    the desired target classes. 
    If false, no products are mapped.
    :var doImport3DModels: If true, the operation imports STEP 3D model files for the given vendor package. The STEP
    files are converted to NX part file and to JT file format and imported into Teamcenter. Items are created for the
    icm0 objects. One "UGMaster" Dataset for the NX part file and one "DirectModel" Dataset for the JT file is created
    below the (new) Item.
    The imported products are identified using the vendor package ID in the icm0 attribute values. This allows to call
    the operation once with only input parameter doImportVendorProducts set to true and a second time with only input
    parameter doMapVendorProducts set to true.
    If false, no 3D models are imported.
    :var importVendorProductsInput: This structure contains the import vendor produts information.
    It is used, when input parameter doImportVendorProducts is true.
    :var mapToSingleTargetClassInput: This structure contains the map vendor produts information.
    It is used, when input parameter doMapToSingleTargetClass is true.
    :var mapToMultiTargetClassesInput: This structure contains the map vendor produts information.
    It is used, when input parameter doMapToMultiTargetClasses is true.
    """
    vendorPackageId: str = ''
    vendorPackageDirectory: str = ''
    doCheckVendorProducts: bool = False
    doImportVendorProducts: bool = False
    doMapToSingleTargetClass: bool = False
    doMapToMultiTargetClasses: bool = False
    doImport3DModels: bool = False
    importVendorProductsInput: ImportVendorProductsInput = None
    mapToSingleTargetClassInput: MapToSingleTargetClassInput = None
    mapToMultiTargetClassesInput: MapToMultiTargetClassesInput = None


@dataclass
class ImportVendorData2Response(TcBaseObj):
    """
    The response object of importVendorData2 service operation.
    
    :var serviceData: The service data from the importVendorData2 service operation.
    :var importedProductCount: The number of vendor products that were already imported from the given package.
    :var mappedProductCount: The number of vendor products from the given package that were aleady mapped to
    Manufacturing Resource Library customer classes.
    :var importVendorProductsInfo: The object with information about the import vendor products operation.
    :var mapToSingleTargetClassInfo: The object with information about the map vendor products operation for single
    target classes and information about products having multiple target classes.
    :var mapToMultiTargetClassesInfo: The object with information about the map vendor products operation in cases of
    multiple target classes.
    :var import3DModelsInfo: The object with information about the import 3D models operation.
    """
    serviceData: ServiceData = None
    importedProductCount: int = 0
    mappedProductCount: int = 0
    importVendorProductsInfo: ImportVendorProductsInfo = None
    mapToSingleTargetClassInfo: MapToSingleTargetClassInfo = None
    mapToMultiTargetClassesInfo: MapToMultiTargetClassesInfo = None
    import3DModelsInfo: Import3DModelsInfo = None


@dataclass
class MapToMultiTargetClassesInfo(TcBaseObj):
    """
    The object with information about the map vendor products having multiple target classes.
    
    :var totalProductsCount: The total count of products in the vendor package.
    :var totalMultiMappingCount: The total count of products in the vendor package having multiple target classes.
    :var successMultiMappingCount: The count of successfully imported products having multiple target classes.
    :var logFileInfo: This object contains the name and ticket of the log file for the map products operation.
    """
    totalProductsCount: int = 0
    totalMultiMappingCount: int = 0
    successMultiMappingCount: int = 0
    logFileInfo: RMFileTicket = None


@dataclass
class MapToMultiTargetClassesInput(TcBaseObj):
    """
    This structure contains information for map vendor products.
    It is used, when input parameter doMapToMultiTargetClasses is true.
    
    :var totalProductsCount: The total count of products in the vendor package.
    :var targetItemTypeName: The type of Item to be created when the product is mapped.
    :var icoToTargetClassMappings: This structure contains information for map vendor products.
    :var logFileInfo: This RMFileTicket object contains the name and ticket of the log file generated for the single
    target class map operation.
    """
    totalProductsCount: int = 0
    targetItemTypeName: str = ''
    icoToTargetClassMappings: List[ICOToTargetClassMappings] = ()
    logFileInfo: RMFileTicket = None


@dataclass
class MapToSingleTargetClassInfo(TcBaseObj):
    """
    The object with information about the map vendor products operation for single target class.
    
    :var totalProductsCount: The total count of imported products from the vendor package.
    :var successSingleMappingCount: The count of successfully imported products having single target class.
    :var savedSearch: The saved search for all mapped products.
    :var multiTargetClassesInfo: A list of structure MultiTargetClassesInfo objects.
    Those objects defines the target classes for the catalog components.
    :var logFileInfo: This RMFileTicket object contains the name and ticket of the log file for the map operation.
    """
    totalProductsCount: int = 0
    successSingleMappingCount: int = 0
    savedSearch: WorkspaceObject = None
    multiTargetClassesInfo: List[MultiTargetClassesInfo] = ()
    logFileInfo: RMFileTicket = None


@dataclass
class MapToSingleTargetClassInput(TcBaseObj):
    """
    This structure contains information for map vendor products for single target class.
    It is used, when input parameter doMapToSingleTargetClass is true.
    
    :var targetItemTypeName: The type of Item to be created when the product is mapped.
    """
    targetItemTypeName: str = ''


@dataclass
class MultiTargetClassesInfo(TcBaseObj):
    """
    The object with information about the multiple target classes for map vendor products operation.
    
    :var sourceIcoID: The ID of the icm0 Internal Classification Objects (ICO) that should be mapped.
    :var sourceClassID: The ID of a class in which the ICO is classified.
    :var sourceClassName: The name of a class in which the ICO is classified.
    :var targetItemName: The name of the item that the resource gets mapped to.
    :var targetClasses: A list of TargetClasses structure.
    """
    sourceIcoID: str = ''
    sourceClassID: str = ''
    sourceClassName: str = ''
    targetItemName: str = ''
    targetClasses: List[TargetClasses] = ()


@dataclass
class TargetClasses(TcBaseObj):
    """
    This structure contains the information about target classes.
    
    :var targetClassID: The ID of target class.
    :var targetClassName: The name of target class.
    """
    targetClassID: str = ''
    targetClassName: str = ''
