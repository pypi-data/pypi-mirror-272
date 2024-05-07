# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# AccelByte Gaming Services Event Log Service

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

from ..models.models_ux import ModelsUX


class ModelsMultipleUX(Model):
    """Models multiple UX (models.MultipleUX)

    Properties:
        ux: (UX) REQUIRED List[ModelsUX]
    """

    # region fields

    ux: List[ModelsUX]  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_ux(self, value: List[ModelsUX]) -> ModelsMultipleUX:
        self.ux = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "ux"):
            result["UX"] = [i0.to_dict(include_empty=include_empty) for i0 in self.ux]
        elif include_empty:
            result["UX"] = []
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(cls, ux: List[ModelsUX], **kwargs) -> ModelsMultipleUX:
        instance = cls()
        instance.ux = ux
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ModelsMultipleUX:
        instance = cls()
        if not dict_:
            return instance
        if "UX" in dict_ and dict_["UX"] is not None:
            instance.ux = [
                ModelsUX.create_from_dict(i0, include_empty=include_empty)
                for i0 in dict_["UX"]
            ]
        elif include_empty:
            instance.ux = []
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ModelsMultipleUX]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ModelsMultipleUX]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[ModelsMultipleUX, List[ModelsMultipleUX], Dict[Any, ModelsMultipleUX]]:
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
            "UX": "ux",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "UX": True,
        }

    # endregion static methods
