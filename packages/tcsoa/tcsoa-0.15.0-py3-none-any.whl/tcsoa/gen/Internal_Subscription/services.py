from tcsoa.gen.Internal_Subscription._2018_12.services import SubscriptionManagementService as imp0
from tcsoa.gen.Internal_Subscription._2018_05.services import SubscriptionManagementService as imp1
from tcsoa.base import TcService


class SubscriptionManagementService(TcService):
    getAllSubscribableEventTypes = imp0.getAllSubscribableEventTypes
    getApplicableCommonEventTypes = imp0.getApplicableCommonEventTypes
    getApplicableConfiguredEvents = imp0.getApplicableConfiguredEvents
    getApplicableEventTypes = imp1.getApplicableEventTypes
    getSubscriptionCreationView = imp1.getSubscriptionCreationView
    getSubscriptionViewAndViewModel = imp0.getSubscriptionViewAndViewModel
    validateSubscribableTypes = imp0.validateSubscribableTypes
