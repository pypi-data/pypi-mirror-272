from __future__ import annotations

from tcsoa.gen.Core._2021_12.Session import AddPoliciesResponse
from typing import List
from tcsoa.gen.Common import ObjectPropertyPolicy
from tcsoa.base import TcService
from tcsoa.gen.Core._2021_12.LOV import ValidatePropertyValuesForLOVInBulkInputData, ValidatePropertyValuesForLOVInBulkResponse


class LOVService(TcService):

    @classmethod
    def validatePropertyValuesForLOVInBulk(cls, inputs: List[ValidatePropertyValuesForLOVInBulkInputData]) -> ValidatePropertyValuesForLOVInBulkResponse:
        """
        This operation validates the input property against the LOV defination. 
        The validatePropertyValuesForLOVInBulk operation is used to validate input property values before invoking
        service operations like creating objects, save as objects or revise objects etc. All of the input property
        names and their values should be included in PropertyValuesMap.
        
        Use cases:
        CAD Attribute Mapping :
        Define CAD attribute mappings which will resolve to properties with LOV attachment.
        Get the values for mapped properties in CAD application.         
        Validate values using this service operation in bulk.
        
        UI Panel :
        Populate the LOV values with getInitalLOVValues/getNextLOVValues service operation in UI Panel for
        multi-selections.
        User selects the any of the populated the value.
        Valiate selected objects and their values with this service operation.
        """
        return cls.execute_soa_method(
            method_name='validatePropertyValuesForLOVInBulk',
            library='Core',
            service_date='2021_12',
            service_name='LOV',
            params={'inputs': inputs},
            response_cls=ValidatePropertyValuesForLOVInBulkResponse,
        )


class SessionService(TcService):

    @classmethod
    def addObjectPropertyPolicies(cls, clientPolicies: List[ObjectPropertyPolicy], namedPolicies: List[str]) -> AddPoliciesResponse:
        """
        Adds multiple object property policies to the session. Once these policies are added to the session, the client
        application can quickly switch between policies using the appropriate methods on the
        'ObjectPropertyPolicyManager' class in the SOA client framework.
        The business logic of a service operation determines what business objects are returned, while the object
        property policy determines which properties are returned on each business object instance. This allows the
        client application to determine how much or how little data is returned based on how the client application
        uses those returned business objects. The policy is applied uniformly to all service operations.
        By default, all applications use the Default object property policy, defined on the Teamcenter server
        '$TC_DATA/soa/policies/default.xml'. It is this policy that is applied to all service operation responses until
        the client application changes the policy. Siemens PLM Software strongly recommends that all applications
        change the policy to one applicable to the client early in the session.
        """
        return cls.execute_soa_method(
            method_name='addObjectPropertyPolicies',
            library='Core',
            service_date='2021_12',
            service_name='Session',
            params={'clientPolicies': clientPolicies, 'namedPolicies': namedPolicies},
            response_cls=AddPoliciesResponse,
        )
