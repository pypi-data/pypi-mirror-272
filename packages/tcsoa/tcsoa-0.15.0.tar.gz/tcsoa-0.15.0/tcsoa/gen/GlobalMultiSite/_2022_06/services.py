from __future__ import annotations

from tcsoa.gen.GlobalMultiSite._2022_06.ImportExport import ExportFilesOfflineInput
from tcsoa.gen.GlobalMultiSite._2021_06.ImportExport import ExportFilesOfflineResponse
from typing import List
from tcsoa.gen.GlobalMultiSite._2007_06.ImportExport import NamesAndValue
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def exportFilesOffline2(cls, input: List[ExportFilesOfflineInput], options: List[NamesAndValue]) -> ExportFilesOfflineResponse:
        """
        This operation exports ImanFile associated with Dataset  from Teamcenter to an offline or local repository. NX
        part files are converted to native format. If option tcxml_export is given, a TCXML file is genereated which
        contains all the processed objects. All files can be downloaded using the returned FMS file tickets.
        """
        return cls.execute_soa_method(
            method_name='exportFilesOffline2',
            library='GlobalMultiSite',
            service_date='2022_06',
            service_name='ImportExport',
            params={'input': input, 'options': options},
            response_cls=ExportFilesOfflineResponse,
        )
