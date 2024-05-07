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

# AccelByte Gaming Services Platform Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from .....core import Operation
from .....core import HeaderStr
from .....core import HttpResponse

from ...models import ErrorEntity
from ...models import PopulatedItemInfo


class GetLocaleItemBySku(Operation):
    """Get an item by sku in locale (getLocaleItemBySku)

    This API is used to get an item by sku in specific locale. If item not exist in specific region, default region item will return.

    Other detail info:

      * Returns : item data

    Properties:
        url: /platform/admin/namespaces/{namespace}/items/bySku/locale

        method: GET

        tags: ["Item"]

        consumes: []

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        namespace: (namespace) REQUIRED str in path

        active_only: (activeOnly) OPTIONAL bool in query

        language: (language) OPTIONAL str in query

        populate_bundle: (populateBundle) OPTIONAL bool in query

        region: (region) OPTIONAL str in query

        store_id: (storeId) OPTIONAL str in query

        sku: (sku) REQUIRED str in query

    Responses:
        200: OK - PopulatedItemInfo (successful operation)

        404: Not Found - ErrorEntity (30141: Store [{storeId}] does not exist in namespace [{namespace}] | 30142: Published store does not exist in namespace [{namespace}] | 30343: Item of sku [{sku}] does not exist)
    """

    # region fields

    _url: str = "/platform/admin/namespaces/{namespace}/items/bySku/locale"
    _method: str = "GET"
    _consumes: List[str] = []
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    namespace: str  # REQUIRED in [path]
    active_only: bool  # OPTIONAL in [query]
    language: str  # OPTIONAL in [query]
    populate_bundle: bool  # OPTIONAL in [query]
    region: str  # OPTIONAL in [query]
    store_id: str  # OPTIONAL in [query]
    sku: str  # REQUIRED in [query]

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
        return result

    def get_query_params(self) -> dict:
        result = {}
        if hasattr(self, "active_only"):
            result["activeOnly"] = self.active_only
        if hasattr(self, "language"):
            result["language"] = self.language
        if hasattr(self, "populate_bundle"):
            result["populateBundle"] = self.populate_bundle
        if hasattr(self, "region"):
            result["region"] = self.region
        if hasattr(self, "store_id"):
            result["storeId"] = self.store_id
        if hasattr(self, "sku"):
            result["sku"] = self.sku
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_namespace(self, value: str) -> GetLocaleItemBySku:
        self.namespace = value
        return self

    def with_active_only(self, value: bool) -> GetLocaleItemBySku:
        self.active_only = value
        return self

    def with_language(self, value: str) -> GetLocaleItemBySku:
        self.language = value
        return self

    def with_populate_bundle(self, value: bool) -> GetLocaleItemBySku:
        self.populate_bundle = value
        return self

    def with_region(self, value: str) -> GetLocaleItemBySku:
        self.region = value
        return self

    def with_store_id(self, value: str) -> GetLocaleItemBySku:
        self.store_id = value
        return self

    def with_sku(self, value: str) -> GetLocaleItemBySku:
        self.sku = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "namespace") and self.namespace:
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "active_only") and self.active_only:
            result["activeOnly"] = bool(self.active_only)
        elif include_empty:
            result["activeOnly"] = False
        if hasattr(self, "language") and self.language:
            result["language"] = str(self.language)
        elif include_empty:
            result["language"] = ""
        if hasattr(self, "populate_bundle") and self.populate_bundle:
            result["populateBundle"] = bool(self.populate_bundle)
        elif include_empty:
            result["populateBundle"] = False
        if hasattr(self, "region") and self.region:
            result["region"] = str(self.region)
        elif include_empty:
            result["region"] = ""
        if hasattr(self, "store_id") and self.store_id:
            result["storeId"] = str(self.store_id)
        elif include_empty:
            result["storeId"] = ""
        if hasattr(self, "sku") and self.sku:
            result["sku"] = str(self.sku)
        elif include_empty:
            result["sku"] = ""
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[Union[None, PopulatedItemInfo], Union[None, ErrorEntity, HttpResponse]]:
        """Parse the given response.

        200: OK - PopulatedItemInfo (successful operation)

        404: Not Found - ErrorEntity (30141: Store [{storeId}] does not exist in namespace [{namespace}] | 30142: Published store does not exist in namespace [{namespace}] | 30343: Item of sku [{sku}] does not exist)

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
            return PopulatedItemInfo.create_from_dict(content), None
        if code == 404:
            return None, ErrorEntity.create_from_dict(content)

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(
        cls,
        namespace: str,
        sku: str,
        active_only: Optional[bool] = None,
        language: Optional[str] = None,
        populate_bundle: Optional[bool] = None,
        region: Optional[str] = None,
        store_id: Optional[str] = None,
        **kwargs,
    ) -> GetLocaleItemBySku:
        instance = cls()
        instance.namespace = namespace
        instance.sku = sku
        if active_only is not None:
            instance.active_only = active_only
        if language is not None:
            instance.language = language
        if populate_bundle is not None:
            instance.populate_bundle = populate_bundle
        if region is not None:
            instance.region = region
        if store_id is not None:
            instance.store_id = store_id
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> GetLocaleItemBySku:
        instance = cls()
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "activeOnly" in dict_ and dict_["activeOnly"] is not None:
            instance.active_only = bool(dict_["activeOnly"])
        elif include_empty:
            instance.active_only = False
        if "language" in dict_ and dict_["language"] is not None:
            instance.language = str(dict_["language"])
        elif include_empty:
            instance.language = ""
        if "populateBundle" in dict_ and dict_["populateBundle"] is not None:
            instance.populate_bundle = bool(dict_["populateBundle"])
        elif include_empty:
            instance.populate_bundle = False
        if "region" in dict_ and dict_["region"] is not None:
            instance.region = str(dict_["region"])
        elif include_empty:
            instance.region = ""
        if "storeId" in dict_ and dict_["storeId"] is not None:
            instance.store_id = str(dict_["storeId"])
        elif include_empty:
            instance.store_id = ""
        if "sku" in dict_ and dict_["sku"] is not None:
            instance.sku = str(dict_["sku"])
        elif include_empty:
            instance.sku = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "namespace": "namespace",
            "activeOnly": "active_only",
            "language": "language",
            "populateBundle": "populate_bundle",
            "region": "region",
            "storeId": "store_id",
            "sku": "sku",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "namespace": True,
            "activeOnly": False,
            "language": False,
            "populateBundle": False,
            "region": False,
            "storeId": False,
            "sku": True,
        }

    # endregion static methods
