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

# AccelByte Gaming Services Lobby Server

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from .....core import Operation
from .....core import HeaderStr
from .....core import HttpResponse

from ...models import ModelGetFriendsResponse
from ...models import RestapiErrorResponseBody


class GetListOfFriends(Operation):
    """get list of friends (get list of friends)

    Get list of friends in a namespace.

    Properties:
        url: /lobby/v1/admin/friend/namespaces/{namespace}/users/{userId}

        method: GET

        tags: ["friends"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        namespace: (namespace) REQUIRED str in path

        user_id: (userId) REQUIRED str in path

        friend_id: (friendId) OPTIONAL str in query

        friend_ids: (friendIds) OPTIONAL List[str] in query

        limit: (limit) OPTIONAL int in query

        offset: (offset) OPTIONAL int in query

    Responses:
        200: OK - ModelGetFriendsResponse

        400: Bad Request - RestapiErrorResponseBody (Bad Request)

        401: Unauthorized - RestapiErrorResponseBody (Unauthorized)

        403: Forbidden - RestapiErrorResponseBody (Forbidden)

        500: Internal Server Error - RestapiErrorResponseBody (Internal Server Error)
    """

    # region fields

    _url: str = "/lobby/v1/admin/friend/namespaces/{namespace}/users/{userId}"
    _method: str = "GET"
    _consumes: List[str] = ["application/json"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    namespace: str  # REQUIRED in [path]
    user_id: str  # REQUIRED in [path]
    friend_id: str  # OPTIONAL in [query]
    friend_ids: List[str]  # OPTIONAL in [query]
    limit: int  # OPTIONAL in [query]
    offset: int  # OPTIONAL in [query]

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
            "path": self.get_path_params(),
            "query": self.get_query_params(),
        }

    def get_path_params(self) -> dict:
        result = {}
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        if hasattr(self, "user_id"):
            result["userId"] = self.user_id
        return result

    def get_query_params(self) -> dict:
        result = {}
        if hasattr(self, "friend_id"):
            result["friendId"] = self.friend_id
        if hasattr(self, "friend_ids"):
            result["friendIds"] = self.friend_ids
        if hasattr(self, "limit"):
            result["limit"] = self.limit
        if hasattr(self, "offset"):
            result["offset"] = self.offset
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_namespace(self, value: str) -> GetListOfFriends:
        self.namespace = value
        return self

    def with_user_id(self, value: str) -> GetListOfFriends:
        self.user_id = value
        return self

    def with_friend_id(self, value: str) -> GetListOfFriends:
        self.friend_id = value
        return self

    def with_friend_ids(self, value: List[str]) -> GetListOfFriends:
        self.friend_ids = value
        return self

    def with_limit(self, value: int) -> GetListOfFriends:
        self.limit = value
        return self

    def with_offset(self, value: int) -> GetListOfFriends:
        self.offset = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "user_id") and self.user_id:
            result["userId"] = str(self.user_id)
        elif include_empty:
            result["userId"] = ""
        if hasattr(self, "friend_id") and self.friend_id:
            result["friendId"] = str(self.friend_id)
        elif include_empty:
            result["friendId"] = ""
        if hasattr(self, "friend_ids") and self.friend_ids:
            result["friendIds"] = [str(i0) for i0 in self.friend_ids]
        elif include_empty:
            result["friendIds"] = []
        if hasattr(self, "limit") and self.limit:
            result["limit"] = int(self.limit)
        elif include_empty:
            result["limit"] = 0
        if hasattr(self, "offset") and self.offset:
            result["offset"] = int(self.offset)
        elif include_empty:
            result["offset"] = 0
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[
        Union[None, ModelGetFriendsResponse],
        Union[None, HttpResponse, RestapiErrorResponseBody],
    ]:
        """Parse the given response.

        200: OK - ModelGetFriendsResponse

        400: Bad Request - RestapiErrorResponseBody (Bad Request)

        401: Unauthorized - RestapiErrorResponseBody (Unauthorized)

        403: Forbidden - RestapiErrorResponseBody (Forbidden)

        500: Internal Server Error - RestapiErrorResponseBody (Internal Server Error)

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
            return ModelGetFriendsResponse.create_from_dict(content), None
        if code == 400:
            return None, RestapiErrorResponseBody.create_from_dict(content)
        if code == 401:
            return None, RestapiErrorResponseBody.create_from_dict(content)
        if code == 403:
            return None, RestapiErrorResponseBody.create_from_dict(content)
        if code == 500:
            return None, RestapiErrorResponseBody.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls,
        namespace: str,
        user_id: str,
        friend_id: Optional[str] = None,
        friend_ids: Optional[List[str]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        **kwargs,
    ) -> GetListOfFriends:
        instance = cls()
        instance.namespace = namespace
        instance.user_id = user_id
        if friend_id is not None:
            instance.friend_id = friend_id
        if friend_ids is not None:
            instance.friend_ids = friend_ids
        if limit is not None:
            instance.limit = limit
        if offset is not None:
            instance.offset = offset
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> GetListOfFriends:
        instance = cls()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "userId" in dict_ and dict_["userId"] is not None:
            instance.user_id = str(dict_["userId"])
        elif include_empty:
            instance.user_id = ""
        if "friendId" in dict_ and dict_["friendId"] is not None:
            instance.friend_id = str(dict_["friendId"])
        elif include_empty:
            instance.friend_id = ""
        if "friendIds" in dict_ and dict_["friendIds"] is not None:
            instance.friend_ids = [str(i0) for i0 in dict_["friendIds"]]
        elif include_empty:
            instance.friend_ids = []
        if "limit" in dict_ and dict_["limit"] is not None:
            instance.limit = int(dict_["limit"])
        elif include_empty:
            instance.limit = 0
        if "offset" in dict_ and dict_["offset"] is not None:
            instance.offset = int(dict_["offset"])
        elif include_empty:
            instance.offset = 0
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "namespace": "namespace",
            "userId": "user_id",
            "friendId": "friend_id",
            "friendIds": "friend_ids",
            "limit": "limit",
            "offset": "offset",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "namespace": True,
            "userId": True,
            "friendId": False,
            "friendIds": False,
            "limit": False,
            "offset": False,
        }

    @staticmethod
    def get_collection_format_map() -> Dict[str, Union[None, str]]:
        return {
            "friendIds": "csv",  # in query
        }

    # endregion static methods
