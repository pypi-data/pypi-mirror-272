from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ScheduleTask, Schedule
from typing import List, Dict
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LoadBaselineResponse(TcBaseObj):
    """
    Response of the load baseline operation, containing information about the loaded baseline tasks.
    
    :var baselineTasksInfo: Map (string, BaselineTaskInfo) of original ScheduleTask UID and its baseline task
    information.
    :var serviceData: The ServiceData.
    """
    baselineTasksInfo: TaskUidToBaselineTaskInfoMap = None
    serviceData: ServiceData = None


@dataclass
class LoadBaselinesInfo(TcBaseObj):
    """
    Information required to load the baseline tasks of a Schedule baseline based on a source Schedule and load options
    
    :var sourceSchedule: The Schedule for which the baseline needs to be loaded.
    :var baselineSchedules: A list of baseline Schedule objects to load.
    :var scheduleTasks: A list of ScheduleTask objects, in the source Schedule, for which the respective baseline tasks
    are to be returned.
    :var loadOptions: A map (string, string) of options for loading Schedule Baseline. Valid options (key : value) are:
    loadBaselineTasks : true/false (Set true to return the baseline tasks; false otherwise)
    loadCompleteBaseline : true/false (Set true to return information of all the baseline tasks in the schedule
    baseline; Set false or do not specify this option to return the baseline task information of only the input
    ScheduleTask objects.)
    """
    sourceSchedule: Schedule = None
    baselineSchedules: List[Schedule] = ()
    scheduleTasks: List[ScheduleTask] = ()
    loadOptions: PropertyValueMap = None


@dataclass
class NotificationRuleInfo(TcBaseObj):
    """
    The information needed for the creation of a single Notification or subscription rule.
    
    :var name: The name of the rule.
    :var target: The Schedule or ScheduleTask.
    :var subscriber: The subscriber for this notification. It is same as target object in case of notification or a
    User object in the case of subscription.
    :var recipient: A list of UID of User, Resource Pool, Discipline, or Schedule Member to be notified.
    :var ruleType: The type of rule to create. Valid values are: "__Add_Task", "__Delete_Task", "__Near_Due",
    "__Overdue", "__Start_Date_Change", "__Finish_Date_Change", "__Status_Change", " __Status_ChangeTo","
    __Priority_Change", "__Priority_ChangeTo", "__Work_Estimate_Change", "__Work_Complete_Change", "__Work_Ready",
    "__User_Assigned".
    :var status: If true, notification will be sent when event is triggered; otherwise, notification will not be sent.
    :var update: If true, the update on the existing notification rule is performed; otherwise, a new notification rule
    is created.
    :var listOfAdditionalProperties: A collection of AdditionalProperties structures. Each AdditionalProperties
    structure holds property name and value for notification rules.
    """
    name: str = ''
    target: BusinessObject = None
    subscriber: BusinessObject = None
    recipient: List[BusinessObject] = ()
    ruleType: str = ''
    status: bool = False
    update: bool = False
    listOfAdditionalProperties: List[AdditionalProperties] = ()


@dataclass
class BaselineTaskInfo(TcBaseObj):
    """
    Contains information about the baselineTask.
    
    :var baselineTask: The baseline ScheduleTask object.
    :var properties: Map (string, string) of baseline task property names and their values.
    """
    baselineTask: ScheduleTask = None
    properties: PropertyValueMap = None


@dataclass
class AdditionalProperties(TcBaseObj):
    """
    The structure containing information of additional properties. 
    Valid properties are: 
    email_subject: Subject of email address which needed to be sent. 
    email_message: Text of email address which needed to be sent. 
    email_recipients: External email address who also needs to be notified.
    condition: Additional rule condition like how many days before user should be notified.
    
    :var name: The name of additional property.
    :var values: A list of values for the property.
    """
    name: str = ''
    values: List[str] = ()


"""
Map (string, string) containing a key value pair of string type.
"""
PropertyValueMap = Dict[str, str]


"""
Map (string, BaselineTaskInfo) of original ScheduleTask UID and various baseline task information.
"""
TaskUidToBaselineTaskInfoMap = Dict[str, List[BaselineTaskInfo]]
