# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: model.j2

# AccelByte Gaming Services Challenge Service

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

from accelbyte_py_sdk.core import Model
from accelbyte_py_sdk.core import StrEnum

from ..models.model_predicate import ModelPredicate


class OperatorEnum(StrEnum):
    AND = "AND"


class ModelRequirement(Model):
    """Model requirement (model.Requirement)

    Properties:
        operator: (operator) REQUIRED Union[str, OperatorEnum]

        predicates: (predicates) REQUIRED List[ModelPredicate]
    """

    # region fields

    operator: Union[str, OperatorEnum]  # REQUIRED
    predicates: List[ModelPredicate]  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_operator(self, value: Union[str, OperatorEnum]) -> ModelRequirement:
        self.operator = value
        return self

    def with_predicates(self, value: List[ModelPredicate]) -> ModelRequirement:
        self.predicates = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "operator"):
            result["operator"] = str(self.operator)
        elif include_empty:
            result["operator"] = Union[str, OperatorEnum]()
        if hasattr(self, "predicates"):
            result["predicates"] = [
                i0.to_dict(include_empty=include_empty) for i0 in self.predicates
            ]
        elif include_empty:
            result["predicates"] = []
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls,
        operator: Union[str, OperatorEnum],
        predicates: List[ModelPredicate],
        **kwargs,
    ) -> ModelRequirement:
        instance = cls()
        instance.operator = operator
        instance.predicates = predicates
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ModelRequirement:
        instance = cls()
        if not dict_:
            return instance
        if "operator" in dict_ and dict_["operator"] is not None:
            instance.operator = str(dict_["operator"])
        elif include_empty:
            instance.operator = Union[str, OperatorEnum]()
        if "predicates" in dict_ and dict_["predicates"] is not None:
            instance.predicates = [
                ModelPredicate.create_from_dict(i0, include_empty=include_empty)
                for i0 in dict_["predicates"]
            ]
        elif include_empty:
            instance.predicates = []
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ModelRequirement]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ModelRequirement]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[ModelRequirement, List[ModelRequirement], Dict[Any, ModelRequirement]]:
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
            "operator": "operator",
            "predicates": "predicates",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "operator": True,
            "predicates": True,
        }

    @staticmethod
    def get_enum_map() -> Dict[str, List[Any]]:
        return {
            "operator": ["AND"],
        }

    # endregion static methods
