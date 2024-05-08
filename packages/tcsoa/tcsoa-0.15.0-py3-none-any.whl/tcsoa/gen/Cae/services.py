from tcsoa.gen.Cae._2012_02.services import StructureManagementService as imp0
from tcsoa.gen.Cae._2013_12.services import SimulationProcessManagementService as imp1
from tcsoa.base import TcService


class StructureManagementService(TcService):
    executeDatamap = imp0.executeDatamap
    executeStructureMap = imp0.executeStructureMap


class SimulationProcessManagementService(TcService):
    launchSimulationTool2 = imp1.launchSimulationTool2
