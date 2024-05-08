from __future__ import annotations

from tcsoa.gen.Internal.StructureManagement._2022_12.Structure import GetOccAttrsObjectsIn, CreateOrUpdateOccAttrObjectsIn, GetOccAttrsObjectsResponse, CreateOrUpdateOccAttrObjectsResp
from typing import List
from tcsoa.base import TcService


class StructureService(TcService):

    @classmethod
    def createOrUpdateOccAttrObjects(cls, inputs: List[CreateOrUpdateOccAttrObjectsIn]) -> CreateOrUpdateOccAttrObjectsResp:
        """
        This operation provides support to create or update the attribute objects for a PSOccurrence. 
        If the PSOccurrence does not have an attribute object, this service operation creates one. If the PSOccurrence
        already has the attribute objects associated, it finds the object to update it.
        Once the Attribute object is created or found, this operation updates the property on this object. 
        And when setting of the property is successful, it also updates the struct last modified date on the BVR, if
        the property is present in the preference: PS_structure_change_condition.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateOccAttrObjects',
            library='Internal-StructureManagement',
            service_date='2022_12',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=CreateOrUpdateOccAttrObjectsResp,
        )

    @classmethod
    def getOccAttrsObjects(cls, inputs: List[GetOccAttrsObjectsIn]) -> GetOccAttrsObjectsResponse:
        """
        This operation provides support to return all the attribute objects that match the types provided in the input
        for given PSOccurrence.
        """
        return cls.execute_soa_method(
            method_name='getOccAttrsObjects',
            library='Internal-StructureManagement',
            service_date='2022_12',
            service_name='Structure',
            params={'inputs': inputs},
            response_cls=GetOccAttrsObjectsResponse,
        )
