from __future__ import annotations

from typing import List
from tcsoa.gen.ProjectManagement._2022_06.ScheduleManagement import LoadBaselineResponse, NotificationRuleInfo, LoadBaselinesInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ScheduleManagementService(TcService):

    @classmethod
    def loadBaselines(cls, loadBaselinesInfo: LoadBaselinesInfo) -> LoadBaselineResponse:
        """
        Loads the information about the baseline tasks of the given ScheduleTask objects based on the source Schedule
        and the baseline Schedule objects.
        """
        return cls.execute_soa_method(
            method_name='loadBaselines',
            library='ProjectManagement',
            service_date='2022_06',
            service_name='ScheduleManagement',
            params={'loadBaselinesInfo': loadBaselinesInfo},
            response_cls=LoadBaselineResponse,
        )

    @classmethod
    def createOrUpdateNotificationRules(cls, notificationRuleInfos: List[NotificationRuleInfo]) -> ServiceData:
        """
        Creates a list of notification rules for Schedule or ScheduleTask objects based on the notification rule info
        structure. The notification rules are used to notify individuals, including yourself, of important events
        associated with selected objects. Notifications utilize Teamcenter mail and the Subscription Manager. To
        receive notifications and subscriptions, a system administrator must set the value of the Mail_server_name
        preference to a name of a valid mail server (this task needs only to be performed once). The e-mail address in
        the Person object for every user that's expected to receive a notification.
        """
        return cls.execute_soa_method(
            method_name='createOrUpdateNotificationRules',
            library='ProjectManagement',
            service_date='2022_06',
            service_name='ScheduleManagement',
            params={'notificationRuleInfos': notificationRuleInfos},
            response_cls=ServiceData,
        )
