# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# AccelByte Gaming Services Reporting Service

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

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from ....core import Model


class RestapiUpdateReasonGroupRequest(Model):
    """Restapi update reason group request (restapi.updateReasonGroupRequest)

    Properties:
        title: (title) REQUIRED str

        reason_ids: (reasonIds) OPTIONAL List[str]
    """

    # region fields

    title: str  # REQUIRED
    reason_ids: List[str]  # OPTIONAL

    # endregion fields

    # region with_x methods

    def with_title(self, value: str) -> RestapiUpdateReasonGroupRequest:
        self.title = value
        return self

    def with_reason_ids(self, value: List[str]) -> RestapiUpdateReasonGroupRequest:
        self.reason_ids = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "title"):
            result["title"] = str(self.title)
        elif include_empty:
            result["title"] = ""
        if hasattr(self, "reason_ids"):
            result["reasonIds"] = [str(i0) for i0 in self.reason_ids]
        elif include_empty:
            result["reasonIds"] = []
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls, title: str, reason_ids: Optional[List[str]] = None, **kwargs
    ) -> RestapiUpdateReasonGroupRequest:
        instance = cls()
        instance.title = title
        if reason_ids is not None:
            instance.reason_ids = reason_ids
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> RestapiUpdateReasonGroupRequest:
        instance = cls()
        if not dict_:
            return instance
        if "title" in dict_ and dict_["title"] is not None:
            instance.title = str(dict_["title"])
        elif include_empty:
            instance.title = ""
        if "reasonIds" in dict_ and dict_["reasonIds"] is not None:
            instance.reason_ids = [str(i0) for i0 in dict_["reasonIds"]]
        elif include_empty:
            instance.reason_ids = []
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, RestapiUpdateReasonGroupRequest]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[RestapiUpdateReasonGroupRequest]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        RestapiUpdateReasonGroupRequest,
        List[RestapiUpdateReasonGroupRequest],
        Dict[Any, RestapiUpdateReasonGroupRequest],
    ]:
        if many:
            if isinstance(any_, dict):
                return cls.create_many_from_dict(any_, include_empty=include_empty)
            elif isinstance(any_, list):
                return cls.create_many_from_list(any_, include_empty=include_empty)
            else:
                raise ValueError()
        else:
            return cls.create_from_dict(any_, include_empty=include_empty)

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "title": "title",
            "reasonIds": "reason_ids",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "title": True,
            "reasonIds": False,
        }

    # endregion static methods
