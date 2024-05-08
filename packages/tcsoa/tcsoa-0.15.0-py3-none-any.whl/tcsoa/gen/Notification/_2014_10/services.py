from __future__ import annotations

from tcsoa.gen.Notification._2014_10.SubscriptionManagement import SubscriptionsResponse, SubscriptionInput, GetSubscriptionsCriteriaInput, FindSubscriptionsCriteriaInput, ModifySubscriptionInput
from typing import List
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):

    @classmethod
    def getSubscriptions(cls, input: GetSubscriptionsCriteriaInput) -> SubscriptionsResponse:
        """
        This operation queries for all Subscriptions that meet the input criteria.  A variety of input parameters are
        allowed, including target, event type, subscriber and handler.  This is intended to return a larger number of
        Subscriptions based on a small set of input criteria.  Most of the parameters can be empty, and will not be
        considered as part of the query.
        
        Use cases:
        The client is searching for all Subscriptions created for a given user against a given object.
        """
        return cls.execute_soa_method(
            method_name='getSubscriptions',
            library='Notification',
            service_date='2014_10',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def modifySubscriptions(cls, inputs: List[ModifySubscriptionInput]) -> SubscriptionsResponse:
        """
        This operation modifies existing ImanSubscriptions.  All values specified in the inputs replace the values on
        the ImanSubscription in the database.  Each modification is verified to insure that a duplicate
        ImanSubscription is not created.
        
        Use cases:
        An existing Subscription needs to have one or more of its values modified.
        """
        return cls.execute_soa_method(
            method_name='modifySubscriptions',
            library='Notification',
            service_date='2014_10',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def createSubscriptions(cls, inputs: List[SubscriptionInput]) -> SubscriptionsResponse:
        """
        This operation creates multiple object or class based Subscriptions based on the provided inputs. A
        Subscription allows a specified piece of functionality to be executed whenever an event occurs on the target
        object. Inputs to this operation will allow the target object to be specified, along with the event to monitor.
        The functionality the execute is specified by an array of ImanActionHandler objects. These handlers will be
        executed in the order they are specified in the Subscription definition. The most common handler would be
        IMAN_Smtp_Mail_Notify, which is used to send an e-mail when the event is triggered. If this handler is
        specified, the notification object should also be included as input.
        
        This operation also creates class based Subscriptions. This is done by passing a type object as the target
        object.  Class based Subscriptions will apply to all objects of the specified type. These can be filtered down
        at execution time by specifying a condition or attribute criteria as input. The Condition or attribute criteria
        will be evaluated against the object on which the event occurred, and the handler will only be executed if the
        Condition evaluates to TRUE.  Conditions and attribute criteria only apply for class based Subscriptions. 
        Attribute criteria are made up of a list of attributes and the values to compare them against off the target
        object.  Each of these comparisons can be logically combined.
        
        
        Use cases:
        Object Based Subscription:
        The client creates an object based Subscription in order to trigger functionality when a specific event occurs
        against the object. An example of this would be subscribing to the "Check Out" event for a given object. Any
        time the object is checked out, the handler functionality will be executed. Most often, this functionality will
        send the given user an e-mail notification.
        
        Class Based Subscription:
        The client creates a class based Subscription in order to trigger functionality when a specific event occurs
        against any object of the given type. An example of this would be subscribing to the "Check Out" event for an
        ItemRevision objects. Any time the object is checked out, the handler functionality will be executed. Most
        often, this functionality will send the given user an e-mail notification.
        
        Class based subscriptions allow a Condition or attribute criteria to be specified as part of the definition.
        This allows the events to be filtered to a smaller level. Any time the event occurs against the given object of
        the specified type, the Condition will be evaluated against the object. If the Condition or attribute criteria
        evaluate to true, the event is posted and the handlers are executed. An example Condition would only evaluate
        to true if the object is part of a specific Project.  Attribute criteria can also be specified and will be
        evaluated when the Subscription is being processed.  If the attribute criteria values do not match, the
        Subscription will be rejected.  Both attribute criteria and a Condition can not be specified at the same time.
        """
        return cls.execute_soa_method(
            method_name='createSubscriptions',
            library='Notification',
            service_date='2014_10',
            service_name='SubscriptionManagement',
            params={'inputs': inputs},
            response_cls=SubscriptionsResponse,
        )

    @classmethod
    def findSubscriptions(cls, input: FindSubscriptionsCriteriaInput) -> SubscriptionsResponse:
        """
        This operation queries for all Subscriptions that meet the input criteria.  A variety of input parameters are
        allowed, including target, event type, subscriber, condition and handlers.
        
        Use cases:
        The client is searching for a previously created Subscription against a given object or type.
        
        Exceptions:
        >When the query operation could not be completed with the given criteria.  This can be caused due to invalid
        input objects.
        
        - 78020:    The operation could not be completed with the given input criteria.
        
        """
        return cls.execute_soa_method(
            method_name='findSubscriptions',
            library='Notification',
            service_date='2014_10',
            service_name='SubscriptionManagement',
            params={'input': input},
            response_cls=SubscriptionsResponse,
        )
