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

# AccelByte Gaming Services Dsm Controller Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from .....core import Operation
from .....core import HeaderStr
from .....core import HttpResponse

from ...models import ModelsDSHeartbeatRequest
from ...models import ResponseError


class ServerHeartbeat(Operation):
    """Server Heartbeat (ServerHeartbeat)

    ```
    Required permission: NAMESPACE:{namespace}:DSM:SERVER [UPDATE]
    Required scope: social

    This endpoint is intended to be called by dedicated server
    which already has claimed to extend its lifetime.
    DS should call this periodically after it claimed.
    The timeframe between 2 heartbeat call should be smaller than
    the session timout in the deployment configuration.
    If the last heartbeat is longer than the session timout, the server.
    will be considered as expired and will be terminated by DSMC.```

    Required Permission(s):
        - NAMESPACE:{namespace}:DSM:SERVER [UPDATE]

    Required Scope(s):
        - social

    Properties:
        url: /dsmcontroller/namespaces/{namespace}/servers/heartbeat

        method: PUT

        tags: ["Server"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        body: (body) REQUIRED ModelsDSHeartbeatRequest in body

        namespace: (namespace) REQUIRED str in path

    Responses:
        202: Accepted - (heartbeat accepted)

        400: Bad Request - ResponseError (malformed request)

        401: Unauthorized - ResponseError (Unauthorized)

        404: Not Found - ResponseError (server not found)

        500: Internal Server Error - ResponseError (Internal Server Error)
    """

    # region fields

    _url: str = "/dsmcontroller/namespaces/{namespace}/servers/heartbeat"
    _method: str = "PUT"
    _consumes: List[str] = ["application/json"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    body: ModelsDSHeartbeatRequest  # REQUIRED in [body]
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
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_body(self, value: ModelsDSHeartbeatRequest) -> ServerHeartbeat:
        self.body = value
        return self

    def with_namespace(self, value: str) -> ServerHeartbeat:
        self.namespace = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "body") and self.body:
            result["body"] = self.body.to_dict(include_empty=include_empty)
        elif include_empty:
            result["body"] = ModelsDSHeartbeatRequest()
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
    ) -> Tuple[Union[None, HttpResponse], Union[None, HttpResponse, ResponseError]]:
        """Parse the given response.

        202: Accepted - (heartbeat accepted)

        400: Bad Request - ResponseError (malformed request)

        401: Unauthorized - ResponseError (Unauthorized)

        404: Not Found - ResponseError (server not found)

        500: Internal Server Error - ResponseError (Internal Server Error)

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

        if code == 202:
            return HttpResponse.create(code, "Accepted"), None
        if code == 400:
            return None, ResponseError.create_from_dict(content)
        if code == 401:
            return None, ResponseError.create_from_dict(content)
        if code == 404:
            return None, ResponseError.create_from_dict(content)
        if code == 500:
            return None, ResponseError.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls, body: ModelsDSHeartbeatRequest, namespace: str, **kwargs
    ) -> ServerHeartbeat:
        instance = cls()
        instance.body = body
        instance.namespace = namespace
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ServerHeartbeat:
        instance = cls()
        if "body" in dict_ and dict_["body"] is not None:
            instance.body = ModelsDSHeartbeatRequest.create_from_dict(
                dict_["body"], include_empty=include_empty
            )
        elif include_empty:
            instance.body = ModelsDSHeartbeatRequest()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "body": "body",
            "namespace": "namespace",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "body": True,
            "namespace": True,
        }

    # endregion static methods
