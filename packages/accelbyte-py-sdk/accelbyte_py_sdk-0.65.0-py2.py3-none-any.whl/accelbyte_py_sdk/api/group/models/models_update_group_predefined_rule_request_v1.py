# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# AccelByte Gaming Services Group Service

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

from ..models.models_rule_information import ModelsRuleInformation


class ModelsUpdateGroupPredefinedRuleRequestV1(Model):
    """Models update group predefined rule request V1 (models.UpdateGroupPredefinedRuleRequestV1)

    Properties:
        rule_detail: (ruleDetail) REQUIRED List[ModelsRuleInformation]
    """

    # region fields

    rule_detail: List[ModelsRuleInformation]  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_rule_detail(
        self, value: List[ModelsRuleInformation]
    ) -> ModelsUpdateGroupPredefinedRuleRequestV1:
        self.rule_detail = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "rule_detail"):
            result["ruleDetail"] = [
                i0.to_dict(include_empty=include_empty) for i0 in self.rule_detail
            ]
        elif include_empty:
            result["ruleDetail"] = []
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls, rule_detail: List[ModelsRuleInformation], **kwargs
    ) -> ModelsUpdateGroupPredefinedRuleRequestV1:
        instance = cls()
        instance.rule_detail = rule_detail
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ModelsUpdateGroupPredefinedRuleRequestV1:
        instance = cls()
        if not dict_:
            return instance
        if "ruleDetail" in dict_ and dict_["ruleDetail"] is not None:
            instance.rule_detail = [
                ModelsRuleInformation.create_from_dict(i0, include_empty=include_empty)
                for i0 in dict_["ruleDetail"]
            ]
        elif include_empty:
            instance.rule_detail = []
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ModelsUpdateGroupPredefinedRuleRequestV1]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ModelsUpdateGroupPredefinedRuleRequestV1]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        ModelsUpdateGroupPredefinedRuleRequestV1,
        List[ModelsUpdateGroupPredefinedRuleRequestV1],
        Dict[Any, ModelsUpdateGroupPredefinedRuleRequestV1],
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
            "ruleDetail": "rule_detail",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "ruleDetail": True,
        }

    # endregion static methods
