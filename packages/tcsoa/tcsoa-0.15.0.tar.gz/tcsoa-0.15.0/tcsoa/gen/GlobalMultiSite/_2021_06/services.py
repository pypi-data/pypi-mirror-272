from __future__ import annotations

from tcsoa.gen.GlobalMultiSite._2021_06.ImportExport import ExportFilesOfflineResponse, ImportNXFileInfo
from typing import List
from tcsoa.gen.GlobalMultiSite._2007_06.ImportExport import NamesAndValue
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class ImportExportService(TcService):

    @classmethod
    def importNXFiles(cls, inputs: List[ImportNXFileInfo]) -> ServiceData:
        """
        Import NX native files into Teamcenter NX Dataset objects such as UGMASTER and UGPART by calling NX clone
        utility. NX clone utility edits the NX part file first and then create a new Dataset version with updated file.
        The NX files must be upldated to the transient volume using FMS prior to calling this operation. The operation
        will check if the Dataset is a NX Dataset, if not, no update will happen. If user doesn&rsquo;t have write
        privilege to the Dataset or the Dataset is checked out by soemone else, then the import operation will fail.
        Multiple files can be imported together and NX clone will be executed once for all.
        """
        return cls.execute_soa_method(
            method_name='importNXFiles',
            library='GlobalMultiSite',
            service_date='2021_06',
            service_name='ImportExport',
            params={'inputs': inputs},
            response_cls=ServiceData,
        )

    @classmethod
    def exportFilesOffline(cls, uids: List[str], options: List[NamesAndValue]) -> ExportFilesOfflineResponse:
        """
        Export DataSet ImanFile from Teamcenter to offline or local repository. For NX part files, the operation will
        convert them to native format. If option tcxml_export is given, a TCXML file will be genereated which contains
        all the processed objects. User can download all the files using the returned FMS file tickets.
        """
        return cls.execute_soa_method(
            method_name='exportFilesOffline',
            library='GlobalMultiSite',
            service_date='2021_06',
            service_name='ImportExport',
            params={'uids': uids, 'options': options},
            response_cls=ExportFilesOfflineResponse,
        )
