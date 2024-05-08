from tcsoa.gen.Internal_ReqMgmt._2023_06.services import ExcelImportExportService as imp0
from tcsoa.base import TcService


class ExcelImportExportService(TcService):
    getMappingGroupInfo = imp0.getMappingGroupInfo
    importExcelAndUpdateMappingGrp = imp0.importExcelAndUpdateMappingGrp
    importExcelAndUpdateMappingGrpAsync = imp0.importExcelAndUpdateMappingGrpAsync
