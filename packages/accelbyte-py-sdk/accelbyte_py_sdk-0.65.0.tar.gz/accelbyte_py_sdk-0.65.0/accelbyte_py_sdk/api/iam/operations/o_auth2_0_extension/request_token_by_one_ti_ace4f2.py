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

# AccelByte Gaming Services Iam Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from .....core import Operation
from .....core import HeaderStr
from .....core import HttpResponse

from ...models import OauthmodelTokenResponseV3


class RequestTokenByOneTimeLinkCodeResponseV3(Operation):
    """Generate publisher token by headless account's one time link code (RequestTokenByOneTimeLinkCodeResponseV3)

    This endpoint is being used to generate user's token by one time link code.
    It require publisher ClientID
    It required a code which can be generated from `/iam/v3/link/code/request`.

    This endpoint support creating transient token by utilizing **isTransient** param:
    **isTransient=true** will generate a transient token with a short Time Expiration and without a refresh token
    **isTransient=false** will consume the one-time code and generate the access token with a refresh token.

    Properties:
        url: /iam/v3/link/token/exchange

        method: POST

        tags: ["OAuth2.0 - Extension"]

        consumes: ["application/x-www-form-urlencoded"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        additional_data: (additionalData) OPTIONAL str in form_data

        is_transient: (isTransient) OPTIONAL bool in form_data

        client_id: (client_id) REQUIRED str in form_data

        one_time_link_code: (oneTimeLinkCode) REQUIRED str in form_data

    Responses:
        200: OK - OauthmodelTokenResponseV3 (Succeed to generate user token by one time link code.)
    """

    # region fields

    _url: str = "/iam/v3/link/token/exchange"
    _method: str = "POST"
    _consumes: List[str] = ["application/x-www-form-urlencoded"]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    additional_data: str  # OPTIONAL in [form_data]
    is_transient: bool  # OPTIONAL in [form_data]
    client_id: str  # REQUIRED in [form_data]
    one_time_link_code: str  # REQUIRED in [form_data]

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
            "form_data": self.get_form_data_params(),
        }

    def get_form_data_params(self) -> dict:
        result = {}
        if hasattr(self, "additional_data"):
            result["additionalData"] = self.additional_data
        if hasattr(self, "is_transient"):
            result["isTransient"] = self.is_transient
        if hasattr(self, "client_id"):
            result["client_id"] = self.client_id
        if hasattr(self, "one_time_link_code"):
            result["oneTimeLinkCode"] = self.one_time_link_code
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_additional_data(
        self, value: str
    ) -> RequestTokenByOneTimeLinkCodeResponseV3:
        self.additional_data = value
        return self

    def with_is_transient(self, value: bool) -> RequestTokenByOneTimeLinkCodeResponseV3:
        self.is_transient = value
        return self

    def with_client_id(self, value: str) -> RequestTokenByOneTimeLinkCodeResponseV3:
        self.client_id = value
        return self

    def with_one_time_link_code(
        self, value: str
    ) -> RequestTokenByOneTimeLinkCodeResponseV3:
        self.one_time_link_code = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "additional_data") and self.additional_data:
            result["additionalData"] = str(self.additional_data)
        elif include_empty:
            result["additionalData"] = ""
        if hasattr(self, "is_transient") and self.is_transient:
            result["isTransient"] = bool(self.is_transient)
        elif include_empty:
            result["isTransient"] = False
        if hasattr(self, "client_id") and self.client_id:
            result["client_id"] = str(self.client_id)
        elif include_empty:
            result["client_id"] = ""
        if hasattr(self, "one_time_link_code") and self.one_time_link_code:
            result["oneTimeLinkCode"] = str(self.one_time_link_code)
        elif include_empty:
            result["oneTimeLinkCode"] = ""
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[Union[None, OauthmodelTokenResponseV3], Union[None, HttpResponse]]:
        """Parse the given response.

        200: OK - OauthmodelTokenResponseV3 (Succeed to generate user token by one time link code.)

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
            return OauthmodelTokenResponseV3.create_from_dict(content), None

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls,
        client_id: str,
        one_time_link_code: str,
        additional_data: Optional[str] = None,
        is_transient: Optional[bool] = None,
        **kwargs,
    ) -> RequestTokenByOneTimeLinkCodeResponseV3:
        instance = cls()
        instance.client_id = client_id
        instance.one_time_link_code = one_time_link_code
        if additional_data is not None:
            instance.additional_data = additional_data
        if is_transient is not None:
            instance.is_transient = is_transient
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> RequestTokenByOneTimeLinkCodeResponseV3:
        instance = cls()
        if "additionalData" in dict_ and dict_["additionalData"] is not None:
            instance.additional_data = str(dict_["additionalData"])
        elif include_empty:
            instance.additional_data = ""
        if "isTransient" in dict_ and dict_["isTransient"] is not None:
            instance.is_transient = bool(dict_["isTransient"])
        elif include_empty:
            instance.is_transient = False
        if "client_id" in dict_ and dict_["client_id"] is not None:
            instance.client_id = str(dict_["client_id"])
        elif include_empty:
            instance.client_id = ""
        if "oneTimeLinkCode" in dict_ and dict_["oneTimeLinkCode"] is not None:
            instance.one_time_link_code = str(dict_["oneTimeLinkCode"])
        elif include_empty:
            instance.one_time_link_code = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "additionalData": "additional_data",
            "isTransient": "is_transient",
            "client_id": "client_id",
            "oneTimeLinkCode": "one_time_link_code",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "additionalData": False,
            "isTransient": False,
            "client_id": True,
            "oneTimeLinkCode": True,
        }

    # endregion static methods
