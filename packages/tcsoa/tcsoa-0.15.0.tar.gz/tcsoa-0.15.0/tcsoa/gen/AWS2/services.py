from tcsoa.gen.AWS2._2018_12.services import RequirementsManagementService as imp0
from tcsoa.gen.AWS2._2017_06.services import UiConfigService as imp1
from tcsoa.base import TcService


class RequirementsManagementService(TcService):
    createTracelinks = imp0.createTracelinks


class UiConfigService(TcService):
    getUIConfigs3 = imp1.getUIConfigs3
