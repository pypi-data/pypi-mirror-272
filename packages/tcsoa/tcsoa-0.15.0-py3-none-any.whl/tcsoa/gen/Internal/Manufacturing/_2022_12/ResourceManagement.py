from __future__ import annotations

from tcsoa.gen.Manufacturing._2013_12.ResourceManagement import RMFileTicket
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from tcsoa.gen.BusinessObjects import WorkspaceObject
from dataclasses import dataclass


@dataclass
class Import3DModelsInfo(TcBaseObj):
    """
    The object with information about the import 3D models operation.
    
    :var totalCount: The total count of imported products from the vendor package.
    :var successCount: The count of successfully imported 3D models.
    :var logFileInfo: This RMFileTicket object contains the name and ticket of the log file for the import 3D models
    operation.
    """
    totalCount: int = 0
    successCount: int = 0
    logFileInfo: RMFileTicket = None


@dataclass
class ImportVendorDataIn(TcBaseObj):
    """
    The input object of importVendorData service operation.
    
    :var vendorPackageId: The ID of the vendor package that should be imported. 
    This ID can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var vendorPackageDirectory: The vendor package root directory residing on the Teamcenter server. 
    This directory can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var doCheckVendorProducts: If true, the operation checks whether products for the given vendor package were
    already imported and/or mapped. In the response object ImportVendorDataResponse the number of   already imported
    products (importedProductCount) and number of mapped products (mappedProductCount) is returned. If false, nothing
    is checked.
    :var doImportVendorProducts: If true, the operation imports vendor products of the given package into the
    Classification vendor catalog classes inside the Teamcenter database. The system creates icm0 Internal
    Classification Objects (ICOs) in those classes.
    If you call this operation with the input parameters  doCheckVendorProducts and doImportVendorProducts set to true
    and the check identifies that products were already imported, then this "import products" operation is not
    performed. If you want to force the product import a second time, set the input parameter  doImportVendorProducts
    to true and doCheckVendorProducts to false.
    If false, no products are imported.
    :var doMapVendorProducts: If true, the operation maps the icm0 objects from the vendor catalog classes into the
    Manufacturing Resource Library's (MRL) tool component classes. The vendor catalog classes contain catalog tool
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
    parameter doMapVendorProducts set to true.
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
    :var mapVendorProductsInput: This structure contains information for map vendor products. 
    It is used, when input parameter doMapVendorProducts is true.
    """
    vendorPackageId: str = ''
    vendorPackageDirectory: str = ''
    doCheckVendorProducts: bool = False
    doImportVendorProducts: bool = False
    doMapVendorProducts: bool = False
    doImport3DModels: bool = False
    importVendorProductsInput: ImportVendorProductsInput = None
    mapVendorProductsInput: MapVendorProductsInput = None


@dataclass
class ImportVendorDataResponse(TcBaseObj):
    """
    The response object of importVendorData service operation.
    
    :var serviceData: The service data from the importVendorData service operation.
    :var importedProductCount: The number of vendor products that were already imported from the given package.
    :var mappedProductCount: The number of vendor products from the given package that were aleady mapped to
    Manufacturing Resource Library customer classes.
    :var importVendorProductsInfo: The object with information about the import vendor products operation.
    :var mapVendorProductsInfo: The object with information about the map vendor products operation.
    :var import3DModelsInfo: The object with information about the import 3D models operation.
    """
    serviceData: ServiceData = None
    importedProductCount: int = 0
    mappedProductCount: int = 0
    importVendorProductsInfo: ImportVendorProductsInfo = None
    mapVendorProductsInfo: MapVendorProductsInfo = None
    import3DModelsInfo: Import3DModelsInfo = None


@dataclass
class ImportVendorProductsInfo(TcBaseObj):
    """
    The object with information about the import vendor products operation.
    
    :var totalCount: The total count of products in the vendor package.
    :var successCount: The count of successfully imported products.
    :var savedSearch: The saved search for all imported products.
    :var logFileInfo: This RMFileTicket object contains the name and ticket of the log file for the import operation.
    """
    totalCount: int = 0
    successCount: int = 0
    savedSearch: WorkspaceObject = None
    logFileInfo: RMFileTicket = None


@dataclass
class ImportVendorProductsInput(TcBaseObj):
    """
    This structure contains the import vendor produts information. 
    It is used, when input parameter doImportVendorProducts is true.
    
    :var classId: The Classification root class ID of the vendor catalog. 
    This ID can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var productCount: The count of products in the given vendor package. 
    This count can be retrieved with operation
    Internal::Manufacturing::_2016_09::ResourceManagement::getVendorCatalogInfo3().
    :var importOption: The import option allows to specify that existing data
    (0) should not be overwritten,
    (1) should be overwritten
    (2) should only be overwritten with newer tool data.
    """
    classId: str = ''
    productCount: int = 0
    importOption: int = 0


@dataclass
class MapVendorProductsInfo(TcBaseObj):
    """
    The object with information about the map vendor products operation.
    
    :var totalCount: The total count of imported products from the vendor package.
    :var successCount: The count of successfully mapped products.
    :var savedSearch: The saved search for all mapped products.
    :var logFileInfo: This object contains the name and ticket of the log file for the map operation.
    """
    totalCount: int = 0
    successCount: int = 0
    savedSearch: WorkspaceObject = None
    logFileInfo: RMFileTicket = None


@dataclass
class MapVendorProductsInput(TcBaseObj):
    """
    This structure contains information for map vendor products. 
    It is used, when input parameter doMapVendorProducts is true.
    
    :var targetItemTypeName: The type of Item to be created when the product is mapped.
    """
    targetItemTypeName: str = ''
