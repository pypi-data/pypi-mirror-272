from __future__ import annotations

from tcsoa.gen.Internal.Manufacturing._2023_06.ResourceManagement import ImportVendorData2In, ImportVendorData2Response
from tcsoa.base import TcService


class ResourceManagementService(TcService):

    @classmethod
    def importVendorData2(cls, importVendorData2In: ImportVendorData2In) -> ImportVendorData2Response:
        """
        This operation imports products from vendor packages. Generic Tool Catalog (GTC) and Deutsches Institut
        f&uuml;r Normung (DIN) packages are supported. The five "do" options (see below) in the input object
        ImportVendorData2In control what sub-operations are executed. It is possible to trigger all together in one
        call or to call them one by one in multiple sequential calls.
        
        This operation also checks whether products for a given vendor package were already imported, maps the imported
        products from the vendor classes to the tool component classes and imports 3D models.
        
        Use cases:
        For check vendor products:
        A typical use case is checking if products were already imported from this vendor package. With this
        information you can ask the user, if the products should be really imported or mapped once more.
        
        For import vendor products:
        A typical use case is importing product data from vendor packages into the Classification vendor catalog
        classes inside the Teamcenter database. It creates icm0 objects in those classes.
        
        For map vendor products:
        A typical use case is the mapping of icm0 objects from the vendor catalog classes into the MRL tool component
        classes. The vendor classes contain catalog tool components. In the MRL tool component classes are those tool
        components that are actively used in the customer's shopfloor.
        In the Classification Admin application, mapping rules (Mapping Views) are defined that control which vendor
        class is mapped on which MRL class and which vendor attribute is mapped on what MRL attribute.
        During the mapping operation a new Item and a icm0 are created in the MRL class and the attribute values from
        the source icm0 are transferred into the target icm0. If the source component has a Dataset attached, it is
        copied to the new target component.
        
        For import 3D models:
        There are two different use cases:
        A) The relevant icm0 is classified in a vendor catalog class
        (the icm0 has an attribute -159003 "3D Model file name")
        B) The relevant  icm0 is classified in a MRL Tool Components class
        (the icm0 does not have an attribute -159003 "3D Model file name")
        
        In use case A, this operation retrieves the 3D model file name directly from vendor attribute -159003 
        "3D Model file name".
        (Another attribute ID instead of -159003 can be defined in the MRMGTC3DModelAttributeID preference.)
        
        In use case B, the operation checks if there is an MRL attribute -40930 "Vendor Reference Object ID" in the
        relevant icm0. This attribute is used to store the reference from the MRL Tool Components icm0 to the vendor
        catalog icm0. If this attribute exists in the icm0 object&rsquo;s class and has a valid icm0 ID as value, the
        3D model file name is retrieved from the referenced icm0. (see use case A)
        (Another attribute ID instead of -40930 can be defined in the MRMGTCReferenceObjectAttributeID preference.)
        
        If there is a problem during importing one of the 3D models, the operation continues importing the 3D models of
        the following icm0 objects and writes information to log file.
        
        Note: The Graphics Builder has to be configured properly for this operation to work.
        """
        return cls.execute_soa_method(
            method_name='importVendorData2',
            library='Internal-Manufacturing',
            service_date='2023_06',
            service_name='ResourceManagement',
            params={'importVendorData2In': importVendorData2In},
            response_cls=ImportVendorData2Response,
        )
