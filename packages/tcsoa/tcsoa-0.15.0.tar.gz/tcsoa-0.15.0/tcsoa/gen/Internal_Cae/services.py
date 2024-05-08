from tcsoa.gen.Internal_Cae._2012_09.services import StructureManagementService as imp0
from tcsoa.gen.Internal_Cae._2011_06.services import StructureManagementService as imp1
from tcsoa.gen.Internal_Cae._2013_05.services import StructureManagementService as imp2
from tcsoa.gen.Internal_Cae._2013_12.services import SimulationProcessManagementService as imp3
from tcsoa.gen.Internal_Cae._2014_06.services import StructureManagementService as imp4
from tcsoa.gen.Internal_Cae._2009_10.services import SimulationProcessManagementService as imp5
from tcsoa.gen.Internal_Cae._2013_12.services import StructureManagementService as imp6
from tcsoa.base import TcService


class StructureManagementService(TcService):
    createNewModelByDM = imp0.createNewModelByDM
    executeDatamap = imp1.executeDatamap
    executeMarkUpToDate = imp0.executeMarkUpToDate
    getCAEPropertyComparisonDetails = imp2.getCAEPropertyComparisonDetails
    loadSimulationDataMonitor = imp4.loadSimulationDataMonitor
    propagateCAEModelAttributes = imp6.propagateCAEModelAttributes
    refreshSimulationDataMonitor = imp4.refreshSimulationDataMonitor
    updateModelAttsByDM = imp0.updateModelAttsByDM


class SimulationProcessManagementService(TcService):
    importSimulationObjects2 = imp3.importSimulationObjects2
    notifyUser = imp5.notifyUser
