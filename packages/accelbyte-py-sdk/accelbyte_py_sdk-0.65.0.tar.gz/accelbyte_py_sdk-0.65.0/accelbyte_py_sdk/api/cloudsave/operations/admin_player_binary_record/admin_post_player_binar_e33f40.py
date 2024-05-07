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

from ...models import ModelsPlayerBinaryRecordCreate
from ...models import ModelsResponseError
from ...models import ModelsUploadBinaryRecordResponse


class AdminPostPlayerBinaryRecordV1(Operation):
    """Create player binary record (adminPostPlayerBinaryRecordV1)

    Create a player binary record.

    Other detail info:

    `key` should follow these rules:
    1. support uppercase and lowercase letters, numbers, and separators **"-"**, **"_"**, **"."** are allowed
    2. begin and end with letters or numbers
    3. spaces are not allowed
    4. separators must not appears twice in a row


    Supported file types: jpeg, jpg, png, bmp, gif, mp3, webp, and bin.

    Properties:
        url: /cloudsave/v1/admin/namespaces/{namespace}/users/{userId}/binaries

        method: POST

        tags: ["AdminPlayerBinaryRecord"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        body: (body) REQUIRED ModelsPlayerBinaryRecordCreate in body

        namespace: (namespace) REQUIRED str in path

        user_id: (userId) REQUIRED str in path

    Responses:
        201: Created - ModelsUploadBinaryRecordResponse (Record in user-level created)

        400: Bad Request - ModelsResponseError (18327: invalid request body)

        401: Unauthorized - ModelsResponseError (20001: unauthorized access)

        403: Forbidden - ModelsResponseError (20013: insufficient permission)

        409: Conflict - ModelsResponseError (18330: key already exists)

        500: Internal Server Error - ModelsResponseError (18323: unable to get record | 18328: unable to save record | 18331: unable to get presigned URL)
    """

    # region fields

    _url: str = "/cloudsave/v1/admin/namespaces/{namespace}/users/{userId}/binaries"
    _method: str = "POST"
    _consumes: List[str] = ["application/json"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    body: ModelsPlayerBinaryRecordCreate  # REQUIRED in [body]
    namespace: str  # REQUIRED in [path]
    user_id: str  # REQUIRED in [path]

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
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        if hasattr(self, "user_id"):
            result["userId"] = self.user_id
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_body(
        self, value: ModelsPlayerBinaryRecordCreate
    ) -> AdminPostPlayerBinaryRecordV1:
        self.body = value
        return self

    def with_namespace(self, value: str) -> AdminPostPlayerBinaryRecordV1:
        self.namespace = value
        return self

    def with_user_id(self, value: str) -> AdminPostPlayerBinaryRecordV1:
        self.user_id = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "body") and self.body:
            result["body"] = self.body.to_dict(include_empty=include_empty)
        elif include_empty:
            result["body"] = ModelsPlayerBinaryRecordCreate()
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "user_id") and self.user_id:
            result["userId"] = str(self.user_id)
        elif include_empty:
            result["userId"] = ""
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[
        Union[None, ModelsUploadBinaryRecordResponse],
        Union[None, HttpResponse, ModelsResponseError],
    ]:
        """Parse the given response.

        201: Created - ModelsUploadBinaryRecordResponse (Record in user-level created)

        400: Bad Request - ModelsResponseError (18327: invalid request body)

        401: Unauthorized - ModelsResponseError (20001: unauthorized access)

        403: Forbidden - ModelsResponseError (20013: insufficient permission)

        409: Conflict - ModelsResponseError (18330: key already exists)

        500: Internal Server Error - ModelsResponseError (18323: unable to get record | 18328: unable to save record | 18331: unable to get presigned URL)

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

        if code == 201:
            return ModelsUploadBinaryRecordResponse.create_from_dict(content), None
        if code == 400:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 401:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 403:
            return None, ModelsResponseError.create_from_dict(content)
        if code == 409:
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
        cls,
        body: ModelsPlayerBinaryRecordCreate,
        namespace: str,
        user_id: str,
        **kwargs,
    ) -> AdminPostPlayerBinaryRecordV1:
        instance = cls()
        instance.body = body
        instance.namespace = namespace
        instance.user_id = user_id
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> AdminPostPlayerBinaryRecordV1:
        instance = cls()
        if "body" in dict_ and dict_["body"] is not None:
            instance.body = ModelsPlayerBinaryRecordCreate.create_from_dict(
                dict_["body"], include_empty=include_empty
            )
        elif include_empty:
            instance.body = ModelsPlayerBinaryRecordCreate()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "userId" in dict_ and dict_["userId"] is not None:
            instance.user_id = str(dict_["userId"])
        elif include_empty:
            instance.user_id = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "body": "body",
            "namespace": "namespace",
            "userId": "user_id",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "body": True,
            "namespace": True,
            "userId": True,
        }

    # endregion static methods
