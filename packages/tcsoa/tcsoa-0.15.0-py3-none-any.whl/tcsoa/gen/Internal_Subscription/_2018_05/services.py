from __future__ import annotations

from tcsoa.gen.Internal.Subscription._2018_05.SubscriptionManagement import GetSubscriptionViewResponse, GetApplicableEventTypesResponse
from tcsoa.gen.BusinessObjects import POM_object, ImanEventType, ImanSubscription
from typing import List
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):

    @classmethod
    def getApplicableEventTypes(cls, objectOrType: POM_object, subscriptionsToFilter: List[ImanSubscription]) -> GetApplicableEventTypesResponse:
        """
        This operation returns all the mapped event types for the input business object or the business object type.
        The event type and its mapping to the business object type is defined through BMIDE.
        
        Each event type, of business object type ImanEventType, represents the possible event on the business objects
        e.g. Checkout, Delete, Cancel Checkout etc.
        
        The event type is mapped to a business object type by defining the event type mapping. The event type mapping
        are of business object type EventTypeMapping in the Teamcenter database.
        
        The event type is used to define the subscriptions for a business object or type and system notifies the
        followers when the subscribed event occurs.
        
        This operation optionally takes existing subscription business objects of type ImanSubscription to find which
        event types are already subscribed and client is requesting to filter the already subscribed event types.
        """
        return cls.execute_soa_method(
            method_name='getApplicableEventTypes',
            library='Internal-Subscription',
            service_date='2018_05',
            service_name='SubscriptionManagement',
            params={'objectOrType': objectOrType, 'subscriptionsToFilter': subscriptionsToFilter},
            response_cls=GetApplicableEventTypesResponse,
        )

    @classmethod
    def getSubscriptionCreationView(cls, objectOrType: POM_object, eventType: ImanEventType) -> GetSubscriptionViewResponse:
        """
        This operation returns the declarative view and view model, as string, to render the create panel of the
        subscription business object. The declarative view is custom HTML tag based, underlying framework agnostic,
        Active Worksapce format whereas declarative view model is JSON format based configuration to support the
        rendering, actions and localization for the view.
        
        The input attributes on the create panel of the subscription business object is governed by the the business
        object or business object type and the selected event type.
        
        While creating the subscription business object, the selected event type of business object type ImanEventType
        is the major driver for the create panel. Event type could be standard event type e.g. Delete, Cancel Checkout
        or assigning status to the business object or relating some other business object or when new revisions are
        created for the Item object types.
        
        This operation is invoked from the Active Worksapce client after user makes a selection of the object or a
        business object type, called follow type and the event type.
        """
        return cls.execute_soa_method(
            method_name='getSubscriptionCreationView',
            library='Internal-Subscription',
            service_date='2018_05',
            service_name='SubscriptionManagement',
            params={'objectOrType': objectOrType, 'eventType': eventType},
            response_cls=GetSubscriptionViewResponse,
        )
