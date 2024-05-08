from tcsoa.gen.Internal_Security._2021_06.services import AwProjectLevelSecurityService as imp0
from tcsoa.gen.Internal_Security._2017_12.services import AwLicensingService as imp1
from tcsoa.gen.Internal_Security._2021_12.services import AwProjectLevelSecurityService as imp2
from tcsoa.gen.Internal_Security._2022_06.services import AwProjectLevelSecurityService as imp3
from tcsoa.base import TcService


class AwProjectLevelSecurityService(TcService):
    createProjects = imp0.createProjects
    getProjectTeam = imp2.getProjectTeam
    getProjectTeam2 = imp3.getProjectTeam2
    saveAsProject = imp2.saveAsProject


class AwLicensingService(TcService):
    getLicensesWithTypes = imp1.getLicensesWithTypes
