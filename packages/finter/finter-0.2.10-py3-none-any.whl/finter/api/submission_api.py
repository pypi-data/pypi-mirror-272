# coding: utf-8

"""
    FINTER API

    ## Finter API Document 1. Domain   - production      - https://api.finter.quantit.io/   - staging      - https://staging.api.finter.quantit.io/  2. Authorization <br><br/>(1) 토큰 발급<br/>curl -X POST https://api.finter.quantit.io/login -d {'username': '{finter_user_id}', 'password': '{finter_user_password}'<br> (2) username, password 로그인 (swagger ui 이용 시)<br/>  # noqa: E501

    OpenAPI spec version: 0.298
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import json
import os
import re  # noqa: F401
import shutil
import tempfile
from datetime import datetime, timedelta

# python 2 and python 3 compatibility library
import six

from finter.api_client import ApiClient


class SubmissionApi(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    Ref: https://github.com/swagger-api/swagger-codegen
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

    def submission_create(self, model_info, model_dir, **kwargs):  # noqa: E501
        """submission_create  # noqa: E501

        Finter submission  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.submission_create(model_info, model_dir, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, object) model_info: (required)
        :param str model_dir: (required)
        :return: SubmissionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """
        kwargs['_return_http_data_only'] = True

        with tempfile.TemporaryDirectory() as temp_dir:
            # add metas to model info
            if isinstance(model_info, str):  # convert json to dict
                model_info = json.loads(model_info)
            model_info['submission_time'] = str(datetime.now())
            model_nickname = model_dir.split('/')[-1].split('.zip')[0]
            model_info['nickname'] = model_nickname
            model_info['model_dir'] = model_dir

            # save model meta and zip model files
            json.dump(model_info, open(f'{model_dir}/model_meta.json', 'w'), indent=4)
            shutil.make_archive(os.path.join(temp_dir, model_nickname), "zip", model_dir)
            model_zip_file = os.path.join(temp_dir, f"{model_nickname}.zip")

            # remove unnecessary keys
            del model_info['submission_time']
            del model_info['model_dir']

            # change model_info from dict to json for HTTP POST
            model_info = json.dumps(model_info)

            if kwargs.get('async_req'):
                return self.submission_create_with_http_info(model_info, model_zip_file, **kwargs)  # noqa: E501
            else:
                (data) = self.submission_create_with_http_info(model_info, model_zip_file, **kwargs)  # noqa: E501
                return data

    def submission_create_with_http_info(self, model_info, model_zip_file, **kwargs):  # noqa: E501
        """submission_create  # noqa: E501

        Finter submission  # noqa: E501
        This method makes a synchronous HTTP request by default. To make an
        asynchronous HTTP request, please pass async_req=True
        >>> thread = api.submission_create_with_http_info(model_info, model_zip_file, async_req=True)
        >>> result = thread.get()

        :param async_req bool
        :param dict(str, object) model_info: (required)
        :param str model_zip_file: (required)
        :return: SubmissionResponse
                 If the method is called asynchronously,
                 returns the request thread.
        """

        all_params = ['model_info', 'model_zip_file']  # noqa: E501
        all_params.append('async_req')
        all_params.append('_return_http_data_only')
        all_params.append('_preload_content')
        all_params.append('_request_timeout')

        params = locals()
        for key, val in six.iteritems(params['kwargs']):
            if key not in all_params:
                raise TypeError(
                    "Got an unexpected keyword argument '%s'"
                    " to method submission_create" % key
                )
            params[key] = val
        del params['kwargs']
        # verify the required parameter 'model_info' is set
        if ('model_info' not in params or
                params['model_info'] is None):
            raise ValueError("Missing the required parameter `model_info` when calling `submission_create`")  # noqa: E501
        # verify the required parameter 'model_zip_file' is set
        if ('model_zip_file' not in params or
                params['model_zip_file'] is None):
            raise ValueError("Missing the required parameter `model_zip_file` when calling `submission_create`")  # noqa: E501

        collection_formats = {}

        path_params = {}

        query_params = []

        header_params = {}

        form_params = []
        local_var_files = {}
        if 'model_info' in params:
            form_params.append(('model_info', params['model_info']))  # noqa: E501
        # remove model_zip_file from params and insert it to local_var_files
        local_var_files['model_zip_file'] = params['model_zip_file']
        del params['model_zip_file']

        body_params = None
        # HTTP header `Accept`
        header_params['Accept'] = self.api_client.select_header_accept(
            ['application/json'])  # noqa: E501

        # HTTP header `Content-Type`
        header_params['Content-Type'] = self.api_client.select_header_content_type(  # noqa: E501
            ['multipart/form-data'])  # noqa: E501

        # Authentication setting
        auth_settings = ['basicAuth', 'tokenAuth']  # noqa: E501

        return self.api_client.call_api(
            '/submission', 'POST',
            path_params,
            query_params,
            header_params,
            body=body_params,
            post_params=form_params,
            files=local_var_files,
            response_type='SubmissionResponse',  # noqa: E501
            auth_settings=auth_settings,
            async_req=params.get('async_req'),
            _return_http_data_only=params.get('_return_http_data_only'),
            _preload_content=params.get('_preload_content', True),
            _request_timeout=params.get('_request_timeout'),
            collection_formats=collection_formats)
