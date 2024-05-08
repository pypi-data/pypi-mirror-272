from tcsoa.gen.ProjectManagement._2007_01.services import ScheduleManagementService as imp0
from tcsoa.gen.ProjectManagement._2008_06.services import ScheduleManagementService as imp1
from tcsoa.gen.ProjectManagement._2012_02.services import ScheduleManagementService as imp2
from tcsoa.gen.ProjectManagement._2012_09.services import ScheduleManagementService as imp3
from tcsoa.gen.ProjectManagement._2015_07.services import ScheduleManagementService as imp4
from tcsoa.gen.ProjectManagement._2007_06.services import ScheduleManagementService as imp5
from tcsoa.gen.ProjectManagement._2011_06.services import ScheduleManagementService as imp6
from tcsoa.gen.ProjectManagement._2011_12.services import ScheduleManagementService as imp7
from tcsoa.gen.ProjectManagement._2016_04.services import ScheduleManagementService as imp8
from tcsoa.gen.ProjectManagement._2022_06.services import ScheduleManagementService as imp9
from tcsoa.gen.ProjectManagement._2014_10.services import ScheduleManagementService as imp10
from tcsoa.gen.ProjectManagement._2014_06.services import ScheduleManagementService as imp11
from tcsoa.gen.ProjectManagement._2007_12.services import ScheduleManagementService as imp12
from tcsoa.gen.ProjectManagement._2009_10.services import ScheduleManagementService as imp13
from tcsoa.gen.ProjectManagement._2011_02.services import ScheduleManagementService as imp14
from tcsoa.gen.ProjectManagement._2018_11.services import ScheduleManagementService as imp15
from tcsoa.gen.ProjectManagement._2017_11.services import ScheduleManagementService as imp16
from tcsoa.base import TcService


class ScheduleManagementService(TcService):
    addMemberships = imp0.addMemberships
    addMemberships2 = imp1.addMemberships
    assignResources = imp2.assignResources
    assignResources2 = imp3.assignResources
    assignResources3 = imp4.assignResources
    baselineTasks = imp0.baselineTasks
    claimAssignment = imp3.claimAssignment
    copySchedules = imp0.copySchedules
    copySchedules2 = imp5.copySchedules
    copySchedules3 = imp1.copySchedules
    copySchedules4 = imp6.copySchedules
    copySchedulesAsync = imp6.copySchedulesAsync
    copySchedulesAsyncClient = imp6.copySchedulesAsyncClient
    createBillRates = imp1.createBillRates
    createDependencies = imp7.createDependencies
    createDependencies2 = imp2.createDependencies
    createNewBaselines = imp0.createNewBaselines
    createNewBaselines2 = imp8.createNewBaselines
    createNewBaselinesAsync = imp8.createNewBaselinesAsync
    createOrUpdateNotificationRules = imp5.createOrUpdateNotificationRules
    createOrUpdateNotificationRules2 = imp9.createOrUpdateNotificationRules
    createPhaseGateTask = imp10.createPhaseGateTask
    createProxyTasks = imp6.createProxyTasks
    createSchedule = imp0.createSchedule
    createSchedule2 = imp1.createSchedule
    createScheduleDeliverableTemplates = imp0.createScheduleDeliverableTemplates
    createScheduleDeliverableTemplates2 = imp1.createScheduleDeliverableTemplates
    createTaskDeliverableTemplates = imp0.createTaskDeliverableTemplates
    createTaskDeliverableTemplates2 = imp5.createTaskDeliverableTemplates
    createTasks = imp2.createTasks
    deleteAssignments = imp2.deleteAssignments
    deleteDependencies = imp2.deleteDependencies
    deleteNotificationRules = imp5.deleteNotificationRules
    deleteScheduleAsync = imp6.deleteScheduleAsync
    deleteScheduleAsyncClient = imp6.deleteScheduleAsyncClient
    deleteSchedulingObjects = imp0.deleteSchedulingObjects
    deleteTasks = imp2.deleteTasks
    detachSchedule = imp10.detachSchedule
    filterUsers = imp11.filterUsers
    findCriticalPathTasks = imp2.findCriticalPathTasks
    getCostRollupData = imp10.getCostRollupData
    getDemandProfile = imp12.getDemandProfile
    getEVMResults = imp10.getEVMResults
    getNotificationRules = imp5.getNotificationRules
    getResourceGraphData = imp10.getResourceGraphData
    insertSchedule = imp10.insertSchedule
    launchScheduledWorkflow = imp2.launchScheduledWorkflow
    loadBaselines = imp9.loadBaselines
    loadSchedules = imp6.loadSchedules
    manageScheduleLocks = imp6.manageScheduleLocks
    modifySchedules = imp13.modifySchedules
    moveTasks = imp2.moveTasks
    recalculateScheduleNonInteractive = imp2.recalculateScheduleNonInteractive
    refreshScheduleObject = imp6.refreshScheduleObject
    replaceAssignment = imp10.replaceAssignment
    scaleScheduleNonInteractive = imp2.scaleScheduleNonInteractive
    shiftSchedule = imp4.shiftSchedule
    shiftScheduleAsync = imp4.shiftScheduleAsync
    shiftScheduleNonInteractive = imp2.shiftScheduleNonInteractive
    specialPasteScheduleTasks = imp14.specialPasteScheduleTasks
    submitTimesheetEntries = imp15.submitTimesheetEntries
    submitTimesheetEntriesAsync = imp15.submitTimesheetEntriesAsync
    updateAssignments = imp2.updateAssignments
    updateDependencies = imp2.updateDependencies
    updateSchedules = imp2.updateSchedules
    updateTaskCostData = imp1.updateTaskCostData
    updateTaskExecution = imp6.updateTaskExecution
    updateTasks = imp13.updateTasks
    updateTasks2 = imp2.updateTasks
    verifySchedule = imp10.verifySchedule
    whatIfAnalysis = imp16.whatIfAnalysis
