# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# pylint: disable=duplicate-code
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring
# pylint: disable=missing-module-docstring
# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-instance-attributes
# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-public-methods
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-statements
# pylint: disable=unused-import

# AccelByte Gaming Services Cloudsave Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from .....core import Operation
from .....core import HeaderStr
from .....core import HttpResponse

from ...models import ModelsBulkGetPlayerRecordResponse
from ...models import ModelsBulkUserIDsRequest
from ...models import ModelsResponseError


class AdminBulkGetPlayerRecordsByUserIDsHandlerV1(Operation):
    """Bulk get player records by multiple user ids (adminBulkGetPlayerRecordsByUserIDsHandlerV1)

    Retrieve player record key and payload in bulk under given namespace.
    Maximum number of user ids per request is 20.

    Properties:
        url: /cloudsave/v1/admin/namespaces/{namespace}/users/records/{key}/bulk

        method: POST

        tags: ["AdminPlayerRecord"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        body: (body) REQUIRED ModelsBulkUserIDsRequest in body

        key: (key) REQUIRED str in path

        namespace: (namespace) REQUIRED str in path

    Responses:
        200: OK - ModelsBulkGetPlayerRecordResponse (OK)

        400: Bad Request - ModelsResponseError (18125: invalid request body | 18126: request record keys list exceed max size [%d])

        401: Unauthorized - ModelsResponseError (20001: unauthorized access)

        403: Forbidden - ModelsResponseError (20013: insufficient permission)

        500: Internal Server Error - ModelsResponseError (18124: unable to get record | 18006: unable to decode record)
    """

    # region fields

    _url: str = "/cloudsave/v1/admin/namespaces/{namespace}/users/records/{key}/bulk"
    _method: str = "POST"
    _consumes: List[str] = ["application/json"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    body: ModelsBulkUserIDsRequest  # REQUIRED in [body]
    key: str  # REQUIRED in [path]
    namespace: str  # REQUIRED in [path]

    # endregion fields

    # region properties

    @property
    def url(self) -> str:
        return self._url

    @property
    def method(self) -> str:
        return self._method

    @property
    def consumes(self) -> List[str]:
        return self._consumes

    @property
    def produces(self) -> List[str]:
        return self._produces

    @property
    def securities(self) -> List[List[str]]:
        return self._securities

    @property
    def location_query(self) -> str:
        return self._location_query

    # endregion properties

    # region get methods

    # endregion get methods

    # region get_x_params methods

    def get_all_params(self) -> dict:
        return {
            "body": self.get_body_params(),
            "path": self.get_path_params(),
        }

    def get_body_params(self) -> Any:
        if not hasattr(self, "body") or self.body is None:
            return None
        return self.body.to_dict()

    def get_path_params(self) -> dict:
        result = {}
        if hasattr(self, "key"):
            result["key"] = self.key
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_body(
        self, value: ModelsBulkUserIDsRequest
    ) -> AdminBulkGetPlayerRecordsByUserIDsHandlerV1:
        self.body = value
        return self

    def with_key(self, value: str) -> AdminBulkGetPlayerRecordsByUserIDsHandlerV1:
        self.key = value
        return self

    def with_namespace(self, value: str) -> AdminBulkGetPlayerRecordsByUserIDsHandlerV1:
        self.namespace = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "body") and self.body:
            result["body"] = self.body.to_dict(include_empty=include_empty)
        elif include_empty:
            result["body"] = ModelsBulkUserIDsRequest()
        if hasattr(self, "key") and self.key:
            result["key"] = str(self.key)
        elif include_empty:
            result["key"] = ""
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[
        Union[None, ModelsBulkGetPlayerRecordResponse],
        Union[None, HttpResponse, ModelsResponseError],
    ]:
        """Parse the given response.

        200: OK - ModelsBulkGetPlayerRecordResponse (OK)

        400: Bad Request - ModelsResponseError (18125: invalid request body | 18126: request record keys list exceed max size [%d])

        401: Unauthorized - ModelsResponseError (20001: unauthorized access)

        403: Forbidden - ModelsResponseError (20013: insufficient permission)

        500: Internal Server Error - ModelsResponseError (18124: unable to get record | 18006: unable to decode record)

        ---: HttpResponse (Undocumented Response)

        ---: HttpResponse (Unexpected Content-Type Error)

        ---: HttpResponse (Unhandled Error)
        """
        pre_processed_response, error = self.pre_process_response(
            code=code, content_type=content_type, content=content
        )
        if error is not None:
            return None, None if error.is_no_content() else error
        code, content_type, content = pre_processed_response

        if code == 200:
            return ModelsBulkGetPlayerRecordResponse.create_from_dict(content), None
        if code == 400:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 401:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 403:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 500:
            return None, ModelsResponseError.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls, body: ModelsBulkUserIDsRequest, key: str, namespace: str, **kwargs
    ) -> AdminBulkGetPlayerRecordsByUserIDsHandlerV1:
        instance = cls()
        instance.body = body
        instance.key = key
        instance.namespace = namespace
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> AdminBulkGetPlayerRecordsByUserIDsHandlerV1:
        instance = cls()
        if "body" in dict_ and dict_["body"] is not None:
            instance.body = ModelsBulkUserIDsRequest.create_from_dict(
                dict_["body"], include_empty=include_empty
            )
        elif include_empty:
            instance.body = ModelsBulkUserIDsRequest()
        if "key" in dict_ and dict_["key"] is not None:
            instance.key = str(dict_["key"])
        elif include_empty:
            instance.key = ""
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "body": "body",
            "key": "key",
            "namespace": "namespace",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "body": True,
            "key": True,
            "namespace": True,
        }

    # endregion static methods
