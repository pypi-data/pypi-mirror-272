import dataclasses
import io
import json
import logging
import os.path
import sys
from enum import Enum
from typing import List, Dict, Iterable

import requests

from datetime import datetime

from tcsoa.config import TcSoaConfig
from tcsoa.exceptions import InvalidCredentialsException, InternalServerException, ServiceException, Severity, \
    InnerException
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBoClass


class RestBackend:
    def __init__(self, host: str):
        """
        Initializes the REST Backend. Should be useable for all Teamcenter Backends which have AWC installed.

        @param host: The address to your web server - for example: http://webserver:7001/tc
        """
        self.host = host
        self.base_url = f'{self.host}/RestServices'
        self.policy = {
            "useRefCount": False,
            "types": list()
        }
        self.state = {
            "stateless": True,
            "unloadObjects": True,
            "enableServerStateHeaders": True,
            "formatProperties": True,
            "clientID": "TcSoaClient"
        }
        self.session = requests.session()
        self.session.trust_env = False
        self.session.proxies = {
            "http": None,
            "https": None,
        }

    def _get_object_load_policy_for_bo(self, bo_name):
        types_list = self.policy['types']
        matching_type = list(t for t in types_list if t['name'] == bo_name)
        if matching_type:
            object_policy = matching_type[0]
        else:
            object_policy = {
                'name': bo_name
            }
            types_list.append(object_policy)
        return object_policy

    def set_object_load_policy(self, bo_name, properties: List[str]):
        object_policy = self._get_object_load_policy_for_bo(bo_name)
        object_policy['properties'] = [{'name': p} for p in properties]

    def add_object_load_policy(self, bo_name, properties: List[str]):
        object_policy = self._get_object_load_policy_for_bo(bo_name)
        objs_props = object_policy.setdefault('properties', [])
        for prop in properties:
            if not any(p for p in objs_props if p['name'] == prop):
                objs_props.append({'name': prop})

    def clear_object_load_policy(self, bo_name):
        self.policy['types'] = list(t for t in self.policy['types'] if t['name'] != bo_name)

    def clear_all_object_load_policies(self):
        self.policy['types'] = list()

    def input_obj_to_json(self, input_obj):
        if input_obj is None:
            return ''
        if type(input_obj) in (str, int, float, bool):
            return input_obj
        if isinstance(input_obj, TcBoClass):
            return {k: self.input_obj_to_json(v) for k, v in input_obj.__dict__.items() if k != 'props'}
        if dataclasses.is_dataclass(input_obj):
            return {k[:-1] if k.endswith('_') else k: self.input_obj_to_json(v) for k, v in input_obj.__dict__.items()}
        if isinstance(input_obj, datetime):
            return input_obj.strftime(TcSoaConfig.date_format)
        if isinstance(input_obj, Enum):
            return input_obj.value
        if isinstance(input_obj, dict):
            return {k: self.input_obj_to_json(v) for k, v in input_obj.items()}
        if type(input_obj) in (list, set, tuple) or isinstance(input_obj, Iterable):
            return [self.input_obj_to_json(o) for o in input_obj]
        raise NotImplementedError()

    def response_to_output_obj(self, response_cls, response):
        try:
            response_data: Dict[str: any] = response.json()
            qname = response_data.pop('.QName')
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.InvalidCredentialsException':
                raise InvalidCredentialsException(**self._data_to_exception(response_data))
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.ServiceException':
                raise ServiceException(**self._data_to_exception(response_data))
            if qname == 'http://teamcenter.com/Schemas/Soa/2006-03/Exceptions.InternalServerException':
                raise InternalServerException(**self._data_to_exception(response_data))

            if response_cls:
                response_data = self.dataclass_from_dict(response_cls, response_data)
            return response_data
        except ValueError:
            # note to self: when XML is returned, you dont have a valid cookie
            return response.content  # todo: handle this better

    def _data_to_exception(self, data):
        messages = data.get('messages', None)
        inner_exs = ()
        if messages:
            data = messages[0]
            inner_exs = [InnerException(**self._data_to_exception(m)) for m in messages[1:]]
        return dict(message=data['message'], code=data['code'], level=Severity(data['level']), inner_exceptions=inner_exs)

    @staticmethod
    def eval_str_type(cls, field):
        """ Black Magic - Evaluates the type annotation in context of the class """
        return eval(field, globals(), sys.modules[cls.__module__].__dict__)

    @staticmethod
    def dataclass_from_dict(cls, from_dict):
        try:
            fieldtypes = cls.__annotations__
        except AttributeError:
            if dataclasses.is_dataclass(cls):
                fieldtypes = dict()     # __annotations__ is only set to data classes with attributes
            elif getattr(cls, '__origin__', None) == dict and isinstance(from_dict, list):
                # special case: from_dict is a tuple, containing 2 lists, where the first list contains keys, and
                # the second list contains the values
                return {
                    RestBackend.dataclass_from_dict(cls.__args__[0], key):
                        RestBackend.dataclass_from_dict(cls.__args__[1], from_dict[1][idx])
                    for idx, key in enumerate(from_dict[0])}
            elif isinstance(from_dict, (tuple, list)):
                return [RestBackend.dataclass_from_dict(cls.__args__[0], f) for f in from_dict]
            elif isinstance(from_dict, dict):
                try:
                    return {
                        RestBackend.dataclass_from_dict(cls.__args__[0], k):
                            RestBackend.dataclass_from_dict(cls.__args__[1], v)
                        for k, v in from_dict.items()
                    }
                except AttributeError:
                    # special case - the definition says is should produce a native object type, but if returns a dict
                    if len(from_dict) == 1 and 'out' in from_dict:
                        return from_dict['out']
                    return from_dict
            else:
                # logging.warning(f'Warning! Expected attribute class {str(cls)} but received {from_dict} !')
                return from_dict

        if issubclass(cls, Enum):
            instance = cls(from_dict)
        else:
            instance = cls()
            # if isinstance(from_dict, list) and len(from_dict) == 1 and isinstance(from_dict[0], dict):
            #     from_dict = from_dict[0]    # HACK! can't believe I have to do this! mainly for class `FileTicketsResponse`
            for f in from_dict:
                dest_f = f
                if f == 'ServiceData' and 'serviceData' in fieldtypes:
                    dest_f = 'serviceData'

                if dest_f in fieldtypes:
                    field = fieldtypes[dest_f]
                else:
                    logging.debug(f'Warning! unregistered attribute "{f}" is tried to be set on class "{cls.__name__}"!')
                    setattr(instance, dest_f, from_dict[f])
                    continue

                if isinstance(field, str):  # black magic incoming
                    field = RestBackend.eval_str_type(cls, field)
                setattr(instance, dest_f, RestBackend.dataclass_from_dict(field, from_dict[f]))
        if TcSoaConfig.global_obj_cache_enabled:
            if isinstance(instance, ServiceData):
                TcSoaConfig.internal_handle_sd(instance)
        return instance

    def _headers(self, method_name: str) -> Dict[str, str]:
        return {
            'Operation-Name': method_name,
            'App-Xml': 'application/json',
            'Content-Type': 'application/json',
        }

    def execute(self, service_id, method_name, input_obj, response_cls):
        json_body = dict(
            header=dict(
                state=self.state,
                policy=self.policy,
            ),
            body=self.input_obj_to_json(input_obj)
        )
        url = f'{self.base_url}/{service_id}/{method_name}'
        data = json.dumps(json_body, ensure_ascii=False).encode('utf8')
        response = self.session.post(url, data=data, headers=self._headers(method_name))
        response.encoding = "utf-8"
        response_obj = self.response_to_output_obj(response_cls, response)
        return response_obj

    def fms_download(self, ticket: str, *, path: str = None, file_stream: io.IOBase = None):
        raise NotImplementedError('For this backend, please use tcsoa.fcc.file_management_utility.FileManagementUtility class to download files.')


class JsonRestBackend(RestBackend):
    """
    A backend which directly communicates with AWC instead of using the REST backend directly.
    This has the advantage of beeing able to use the AWC microservices, such as the file service.

    @param host: The address of AWC - for example: https://awc.my-company.com
    """

    def __init__(self, host: str):
        super(JsonRestBackend, self).__init__(host)
        self.base_url = f'{self.host}/tc/JsonRestServices'
        self._fms_initialized = False

    def _headers(self, method_name: str = None) -> Dict[str, str]:
        if 'XSRF-TOKEN' not in self.session.cookies:
            self.session.get(f'{self.host}/getSessionVars')
        return {
            'Content-Type': 'application/json',
            'X-Xsrf-Token': self.session.cookies['XSRF-TOKEN'],
        }

    def _ensure_fms_init(self):
        """
        Okay explanation time:
        When executing a login in Teamcenter, your session is not really registered in AWC.
        To achieve a "real" login in AWC to be able to use microservices like file-repo-service, your need to call
        the tcsoa.gen.Internal_AWS2.services.DataManagementService#getTCSessionAnalyticsInfo method, where the loading
        policy inclused the 'user_id' attribute for the 'UserSession' object.
        After doing this, your session is registered for the AWC micro services and you can call them without
        getting a http 401 error.
        """
        if self._fms_initialized is False:
            self._fms_initialized = True
            self.add_object_load_policy('UserSession', ['user_id'])
            from tcsoa.gen.Internal_AWS2.services import DataManagementService
            DataManagementService.getTCSessionAnalyticsInfo([])

    def fms_download(self, ticket: str, *, path: str = None, file_stream: io.IOBase = None):
        self._ensure_fms_init()

        if path is None:
            file_name = 'my_file'
        else:
            file_name = os.path.basename(path)
        url = f'{self.host}/fms/fmsdownload/{file_name}'

        response = self.session.get(url, params={'ticket': ticket})
        response.encoding = "utf-8"
        if 200 <= response.status_code < 300:
            if file_stream is not None:
                file_stream.write(response.content)
            elif path is not None:
                with open(path, 'wb') as f:
                    f.write(response.content)
            else:
                raise ValueError('pass either "path" or "file_stream" parameter.')
        else:
            response.raise_for_status()

    def fms_upload(self, ticket: str, *, file_path: str, mime_type: str):
        self._ensure_fms_init()

        file_name = os.path.basename(file_path)
        mp_encoder = MultipartEncoder(
            fields={
                'fmsTicket': ticket,
                'fmsFile': (file_name, open(file_path, 'rb'), mime_type),
            }
        )
        url = f'{self.host}/fms/fmsupload'
        response = self.session.post(url, data=mp_encoder, headers={
            'Content-Type': mp_encoder.content_type,
            'X-Xsrf-Token': self.session.cookies['XSRF-TOKEN'],
        })
        if response.status_code >= 400:
            response.raise_for_status()
