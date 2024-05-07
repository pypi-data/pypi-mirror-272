# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# AccelByte Gaming Services Session History Service

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

from ..models.apimodels_history import ApimodelsHistory


class ApimodelsGameSessionDetail(Model):
    """Apimodels game session detail (apimodels.GameSessionDetail)

    Properties:
        created_at: (created_at) REQUIRED str

        histories: (histories) REQUIRED List[ApimodelsHistory]

        namespace: (namespace) REQUIRED str

        session_id: (sessionID) REQUIRED str

        session_template: (session_template) REQUIRED str
    """

    # region fields

    created_at: str  # REQUIRED
    histories: List[ApimodelsHistory]  # REQUIRED
    namespace: str  # REQUIRED
    session_id: str  # REQUIRED
    session_template: str  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_created_at(self, value: str) -> ApimodelsGameSessionDetail:
        self.created_at = value
        return self

    def with_histories(
        self, value: List[ApimodelsHistory]
    ) -> ApimodelsGameSessionDetail:
        self.histories = value
        return self

    def with_namespace(self, value: str) -> ApimodelsGameSessionDetail:
        self.namespace = value
        return self

    def with_session_id(self, value: str) -> ApimodelsGameSessionDetail:
        self.session_id = value
        return self

    def with_session_template(self, value: str) -> ApimodelsGameSessionDetail:
        self.session_template = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "created_at"):
            result["created_at"] = str(self.created_at)
        elif include_empty:
            result["created_at"] = ""
        if hasattr(self, "histories"):
            result["histories"] = [
                i0.to_dict(include_empty=include_empty) for i0 in self.histories
            ]
        elif include_empty:
            result["histories"] = []
        if hasattr(self, "namespace"):
            result["namespace"] = str(self.namespace)
        elif include_empty:
            result["namespace"] = ""
        if hasattr(self, "session_id"):
            result["sessionID"] = str(self.session_id)
        elif include_empty:
            result["sessionID"] = ""
        if hasattr(self, "session_template"):
            result["session_template"] = str(self.session_template)
        elif include_empty:
            result["session_template"] = ""
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls,
        created_at: str,
        histories: List[ApimodelsHistory],
        namespace: str,
        session_id: str,
        session_template: str,
        **kwargs,
    ) -> ApimodelsGameSessionDetail:
        instance = cls()
        instance.created_at = created_at
        instance.histories = histories
        instance.namespace = namespace
        instance.session_id = session_id
        instance.session_template = session_template
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ApimodelsGameSessionDetail:
        instance = cls()
        if not dict_:
            return instance
        if "created_at" in dict_ and dict_["created_at"] is not None:
            instance.created_at = str(dict_["created_at"])
        elif include_empty:
            instance.created_at = ""
        if "histories" in dict_ and dict_["histories"] is not None:
            instance.histories = [
                ApimodelsHistory.create_from_dict(i0, include_empty=include_empty)
                for i0 in dict_["histories"]
            ]
        elif include_empty:
            instance.histories = []
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        if "sessionID" in dict_ and dict_["sessionID"] is not None:
            instance.session_id = str(dict_["sessionID"])
        elif include_empty:
            instance.session_id = ""
        if "session_template" in dict_ and dict_["session_template"] is not None:
            instance.session_template = str(dict_["session_template"])
        elif include_empty:
            instance.session_template = ""
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ApimodelsGameSessionDetail]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ApimodelsGameSessionDetail]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        ApimodelsGameSessionDetail,
        List[ApimodelsGameSessionDetail],
        Dict[Any, ApimodelsGameSessionDetail],
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
            "created_at": "created_at",
            "histories": "histories",
            "namespace": "namespace",
            "sessionID": "session_id",
            "session_template": "session_template",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "created_at": True,
            "histories": True,
            "namespace": True,
            "sessionID": True,
            "session_template": True,
        }

    # endregion static methods
