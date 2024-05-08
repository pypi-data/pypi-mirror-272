from __future__ import annotations

from tcsoa.gen.Internal.Subscription._2018_12.SubscriptionManagement import ValidateSubscribableTypesResponse, GetApplCommonEventTypesResponse, GetSubscriptionViewAndModelResponse
from tcsoa.gen.BusinessObjects import POM_object, ImanEventType
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):

    @classmethod
    def getAllSubscribableEventTypes(cls) -> ServiceData:
        """
        This operation returns all the subscribable event types in the system.
        Event type and its mapping is configured through BMIDE from the Extensions section, by navigating to "Audit
        Manager" and "Event Type Mappings".
        Each event type, of business object type ImanEventType, represents the possible event on the business objects
        e.g. Checkout, Delete, Cancel Checkout etc.
        
        The event type is mapped to a business object type by defining the event type mapping. The event type mapping
        are of business object type EventTypeMapping in the Teamcenter database.
        
        Subscribable flag is a property on the EventTypeMapping, can be configured through BMIDE. Which defines whether
        user can create a subscription for this EventTypeMapping (business object type and event type combination).
        """
        return cls.execute_soa_method(
            method_name='getAllSubscribableEventTypes',
            library='Internal-Subscription',
            service_date='2018_12',
            service_name='SubscriptionManagement',
            params={},
            response_cls=ServiceData,
        )

    @classmethod
    def getApplicableCommonEventTypes(cls, objectsOrTypes: List[POM_object]) -> GetApplCommonEventTypesResponse:
        """
        This operation returns common event types for the input business objects or the business object types. The
        event type and its mapping to the business object type is defined through BMIDE.
        
        Each event type, of business object type ImanEventType, represents the possible event on the business objects
        e.g. Checkout, Delete, Cancel Checkout etc.
        
        The event type is mapped to a business object type by defining the event type mapping. The event type mapping
        are of business object type EventTypeMapping in the Teamcenter database.
        
        The event type is used to define the subscriptions for a business object or type and system notifies the
        followers when the subscribed event occurs.
        
        This operation filters the already subscribed event types. This filtering of event types is only applicable,
        - To business objects, not to types.
        - When there is only single object input for objectsOrTypes.
        
        """
        return cls.execute_soa_method(
            method_name='getApplicableCommonEventTypes',
            library='Internal-Subscription',
            service_date='2018_12',
            service_name='SubscriptionManagement',
            params={'objectsOrTypes': objectsOrTypes},
            response_cls=GetApplCommonEventTypesResponse,
        )

    @classmethod
    def getApplicableConfiguredEvents(cls, inObject: POM_object) -> ServiceData:
        """
        This operation returns list of event types which is subset of,
        &bull;    User configured list of event types applicable for a given input object type.
        &bull;    Filters out already subscribed event types for the input object.
        &bull;    If the input object is null, it would return all the event types configured by the logged in user.
        
        This filtered list of event types is used for subscribing object to multiple events in Active Workspace.
        
        Each user can configure his/her favorite list of event types which internally is stored in a user preference,
        AWC_followMultiEventConfiguredEventTypes.
        
        Event type and its mapping is configured through BMIDE. Subscribable flag is defined on event type mapping in
        BMIDE.
        """
        return cls.execute_soa_method(
            method_name='getApplicableConfiguredEvents',
            library='Internal-Subscription',
            service_date='2018_12',
            service_name='SubscriptionManagement',
            params={'inObject': inObject},
            response_cls=ServiceData,
        )

    @classmethod
    def getSubscriptionViewAndViewModel(cls, objectsOrTypes: List[POM_object], eventTypes: List[ImanEventType]) -> GetSubscriptionViewAndModelResponse:
        """
        This operation returns the declarative view and view model, as string, to render the create panel of the
        subscription business object. The declarative view is custom tag based, underlying framework agnostic, Active
        Worksapce html format whereas declarative view model is JSON format based configuration to support the
        rendering, actions and localization for the view.
        
        The input attributes on the create panel of the subscription business object is governed by the the business
        object or business object type and the selected event type.
        
        In case of multiple objects or events types are passed as an input paramater it renders the view and view model
        accrodingly.
        
        While creating the subscription business object, the selected event type of business object type ImanEventType
        is the major driver for the create panel. Event type could be standard event type e.g. Delete, Cancel Checkout
        or assigning status to the business object or relating some other business object or when new revisions are
        created for the Item business object types.
        
        This operation is invoked from the Active Worksapce client after user makes a selection of the object or a
        business object type, called follow type and the event type.
        """
        return cls.execute_soa_method(
            method_name='getSubscriptionViewAndViewModel',
            library='Internal-Subscription',
            service_date='2018_12',
            service_name='SubscriptionManagement',
            params={'objectsOrTypes': objectsOrTypes, 'eventTypes': eventTypes},
            response_cls=GetSubscriptionViewAndModelResponse,
        )

    @classmethod
    def validateSubscribableTypes(cls, objectsOrTypes: List[POM_object]) -> ValidateSubscribableTypesResponse:
        """
        This operation identifies the list of input objects which can be subscribed for event notification. A filtered
        list of subscribable and non subscribable objects are returned.
        
        Subscribable flag is defined on event type mapping in BMIDE.
        """
        return cls.execute_soa_method(
            method_name='validateSubscribableTypes',
            library='Internal-Subscription',
            service_date='2018_12',
            service_name='SubscriptionManagement',
            params={'objectsOrTypes': objectsOrTypes},
            response_cls=ValidateSubscribableTypesResponse,
        )
