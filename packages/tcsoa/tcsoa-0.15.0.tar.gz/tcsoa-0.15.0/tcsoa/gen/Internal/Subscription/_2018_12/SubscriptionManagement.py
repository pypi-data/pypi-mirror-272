from __future__ import annotations

from tcsoa.gen.BusinessObjects import POM_object, ImanEventType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetApplCommonEventTypesResponse(TcBaseObj):
    """
    The GetApplCommonEventTypesResponse structure is to hold a list of applicable common ImanEventType business objects.
    
    :var commonEventTypes: List of common event types applicable for the given input business objects or types.
    :var serviceData: ServiceData object associated with the operation, contains business objects of ImanEventType in
    plain list with inflated properties.
    """
    commonEventTypes: List[ImanEventType] = ()
    serviceData: ServiceData = None


@dataclass
class GetSubscriptionViewAndModelResponse(TcBaseObj):
    """
    The GetSubscriptionViewAndModelResponse structure is used to hold declarative view and view model as string with
    the ServiceData object.
    
    :var view: Declarative view as string to render create panel for the subscription business object.
    :var viewModel: Declarative view model as string to support rendering of the create panel for the subscription
    business object.
    :var serviceData: ServiceData object associated with the operation, contains partial errors, if any.
    """
    view: str = ''
    viewModel: str = ''
    serviceData: ServiceData = None


@dataclass
class ValidateSubscribableTypesResponse(TcBaseObj):
    """
    The ValidateSubscribableTypesResponse structure is used to hold two separate list of subscribable and non
    subscribable objects or types.
    
    :var subscribableObjects: List of subscribable objects or Types.
    :var nonSubscribableObjects: List of non subscribable objects or types.
    :var serviceData: ServiceData object associated with the operation, contains business objects in plain list with
    inflated properties.
    """
    subscribableObjects: List[POM_object] = ()
    nonSubscribableObjects: List[POM_object] = ()
    serviceData: ServiceData = None
