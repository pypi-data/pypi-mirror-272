from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanEventType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetApplicableEventTypesResponse(TcBaseObj):
    """
    The GetApplicableEventTypesResponse structure is used to hold a list of applicable ImanEventType business objects.
    
    :var eventTypes: List of event types applicable for the given input business object or type.
    :var serviceData: ServiceData object associated with the operation, contains business objects of ImanEventType in
    plain list with inflated properties.
    """
    eventTypes: List[ImanEventType] = ()
    serviceData: ServiceData = None


@dataclass
class GetSubscriptionViewResponse(TcBaseObj):
    """
    The GetSubscriptionViewResponse structure is used to hold declarative view and view model as string with the
    ServiceData object.
    
    :var view: Declarative view as HTML string to render create panel for the subscription business object.
    :var viewModel: Declarative view model as JSON string to support rendering of the create panel for the subscription
    business object.
    :var serviceData: ServiceData object associated with the operation, contains partial errors, if any.
    """
    view: str = ''
    viewModel: str = ''
    serviceData: ServiceData = None
