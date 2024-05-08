from __future__ import annotations

from tcsoa.gen.Internal.ReqMgmt._2023_06.ExcelImportExport import MappingGroupResponse, ImportExcelData, ImportExcelResponse, MappingGroupInput
from typing import List
from tcsoa.base import TcService


class ExcelImportExportService(TcService):

    @classmethod
    def getMappingGroupInfo(cls, inputs: List[MappingGroupInput]) -> MappingGroupResponse:
        """
        Returns all the mapping group information which includes the names of all mapping groups as well as the mapping
        information of each group. The input Excel file contains a level column to indicate the level of the object in
        the structure. "Level" and "Object Type" columns are mandatory in the input Excel sheet. The column headers of
        the excel file are mapped to their respective properties which are saved into a mapping group. The user can
        create, update or delete the mapping group. The input Excel file is parsed to import the data to create
        Requirement structure in Teamcenter.
        """
        return cls.execute_soa_method(
            method_name='getMappingGroupInfo',
            library='Internal-ReqMgmt',
            service_date='2023_06',
            service_name='ExcelImportExport',
            params={'inputs': inputs},
            response_cls=MappingGroupResponse,
        )

    @classmethod
    def importExcelAndUpdateMappingGrp(cls, importExcelData: List[ImportExcelData]) -> ImportExcelResponse:
        """
        Imports an Excel file into Teamcenter and creates the Requirement structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure. "Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create Requirement structure in Teamcenter. This operation
        supports the creation of objects only. Update and Delete are not supported. The column headers in excel are
        mapped to their respective properties which are saved as a mapping group on "import". This operation support
        create and update of mapping groups.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrp',
            library='Internal-ReqMgmt',
            service_date='2023_06',
            service_name='ExcelImportExport',
            params={'importExcelData': importExcelData},
            response_cls=ImportExcelResponse,
        )

    @classmethod
    def importExcelAndUpdateMappingGrpAsync(cls, importExcelData: List[ImportExcelData]) -> None:
        """
        Imports an Excel file into Teamcenter and creates the Requirement structure and sets the properties on objects
        based on the values given in Excel file. The input Excel file contains a level column to indicate the level of
        the object in the structure." Level" and "Object Type" columns are mandatory in the input Excel sheet. The
        input Excel file is parsed to import the data to create Requirement structure in Teamcenter. This operation
        supports the creation of objects only. Update and Delete are not supported. The column headers in excel are
        mapped to their respective properties which are saved as a mapping group on "import". This operation support
        create and update of mapping groups.
        """
        return cls.execute_soa_method(
            method_name='importExcelAndUpdateMappingGrpAsync',
            library='Internal-ReqMgmt',
            service_date='2023_06',
            service_name='ExcelImportExport',
            params={'importExcelData': importExcelData},
            response_cls=None,
        )
