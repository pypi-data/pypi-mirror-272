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


class AssignmentRuleEnum(StrEnum):
    FIXED = "FIXED"
    RANDOMIZED = "RANDOMIZED"
    UNSCHEDULED = "UNSCHEDULED"


class GoalsVisibilityEnum(StrEnum):
    PERIODONLY = "PERIODONLY"
    SHOWALL = "SHOWALL"


class RotationEnum(StrEnum):
    DAILY = "DAILY"
    MONTHLY = "MONTHLY"
    NONE = "NONE"
    WEEKLY = "WEEKLY"


class ModelsUpdateChallengeRequest(Model):
    """Models update challenge request (models.UpdateChallengeRequest)

    Properties:
        active_goals_per_rotation: (activeGoalsPerRotation) OPTIONAL int

        assignment_rule: (assignmentRule) OPTIONAL Union[str, AssignmentRuleEnum]

        description: (description) OPTIONAL str

        end_after: (endAfter) OPTIONAL int

        end_date: (endDate) OPTIONAL str

        goals_visibility: (goalsVisibility) OPTIONAL Union[str, GoalsVisibilityEnum]

        name: (name) OPTIONAL str

        repeat_after: (repeatAfter) OPTIONAL int

        rotation: (rotation) OPTIONAL Union[str, RotationEnum]

        start_date: (startDate) OPTIONAL str
    """

    # region fields

    active_goals_per_rotation: int  # OPTIONAL
    assignment_rule: Union[str, AssignmentRuleEnum]  # OPTIONAL
    description: str  # OPTIONAL
    end_after: int  # OPTIONAL
    end_date: str  # OPTIONAL
    goals_visibility: Union[str, GoalsVisibilityEnum]  # OPTIONAL
    name: str  # OPTIONAL
    repeat_after: int  # OPTIONAL
    rotation: Union[str, RotationEnum]  # OPTIONAL
    start_date: str  # OPTIONAL

    # endregion fields

    # region with_x methods

    def with_active_goals_per_rotation(
        self, value: int
    ) -> ModelsUpdateChallengeRequest:
        self.active_goals_per_rotation = value
        return self

    def with_assignment_rule(
        self, value: Union[str, AssignmentRuleEnum]
    ) -> ModelsUpdateChallengeRequest:
        self.assignment_rule = value
        return self

    def with_description(self, value: str) -> ModelsUpdateChallengeRequest:
        self.description = value
        return self

    def with_end_after(self, value: int) -> ModelsUpdateChallengeRequest:
        self.end_after = value
        return self

    def with_end_date(self, value: str) -> ModelsUpdateChallengeRequest:
        self.end_date = value
        return self

    def with_goals_visibility(
        self, value: Union[str, GoalsVisibilityEnum]
    ) -> ModelsUpdateChallengeRequest:
        self.goals_visibility = value
        return self

    def with_name(self, value: str) -> ModelsUpdateChallengeRequest:
        self.name = value
        return self

    def with_repeat_after(self, value: int) -> ModelsUpdateChallengeRequest:
        self.repeat_after = value
        return self

    def with_rotation(
        self, value: Union[str, RotationEnum]
    ) -> ModelsUpdateChallengeRequest:
        self.rotation = value
        return self

    def with_start_date(self, value: str) -> ModelsUpdateChallengeRequest:
        self.start_date = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "active_goals_per_rotation"):
            result["activeGoalsPerRotation"] = int(self.active_goals_per_rotation)
        elif include_empty:
            result["activeGoalsPerRotation"] = 0
        if hasattr(self, "assignment_rule"):
            result["assignmentRule"] = str(self.assignment_rule)
        elif include_empty:
            result["assignmentRule"] = Union[str, AssignmentRuleEnum]()
        if hasattr(self, "description"):
            result["description"] = str(self.description)
        elif include_empty:
            result["description"] = ""
        if hasattr(self, "end_after"):
            result["endAfter"] = int(self.end_after)
        elif include_empty:
            result["endAfter"] = 0
        if hasattr(self, "end_date"):
            result["endDate"] = str(self.end_date)
        elif include_empty:
            result["endDate"] = ""
        if hasattr(self, "goals_visibility"):
            result["goalsVisibility"] = str(self.goals_visibility)
        elif include_empty:
            result["goalsVisibility"] = Union[str, GoalsVisibilityEnum]()
        if hasattr(self, "name"):
            result["name"] = str(self.name)
        elif include_empty:
            result["name"] = ""
        if hasattr(self, "repeat_after"):
            result["repeatAfter"] = int(self.repeat_after)
        elif include_empty:
            result["repeatAfter"] = 0
        if hasattr(self, "rotation"):
            result["rotation"] = str(self.rotation)
        elif include_empty:
            result["rotation"] = Union[str, RotationEnum]()
        if hasattr(self, "start_date"):
            result["startDate"] = str(self.start_date)
        elif include_empty:
            result["startDate"] = ""
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls,
        active_goals_per_rotation: Optional[int] = None,
        assignment_rule: Optional[Union[str, AssignmentRuleEnum]] = None,
        description: Optional[str] = None,
        end_after: Optional[int] = None,
        end_date: Optional[str] = None,
        goals_visibility: Optional[Union[str, GoalsVisibilityEnum]] = None,
        name: Optional[str] = None,
        repeat_after: Optional[int] = None,
        rotation: Optional[Union[str, RotationEnum]] = None,
        start_date: Optional[str] = None,
        **kwargs,
    ) -> ModelsUpdateChallengeRequest:
        instance = cls()
        if active_goals_per_rotation is not None:
            instance.active_goals_per_rotation = active_goals_per_rotation
        if assignment_rule is not None:
            instance.assignment_rule = assignment_rule
        if description is not None:
            instance.description = description
        if end_after is not None:
            instance.end_after = end_after
        if end_date is not None:
            instance.end_date = end_date
        if goals_visibility is not None:
            instance.goals_visibility = goals_visibility
        if name is not None:
            instance.name = name
        if repeat_after is not None:
            instance.repeat_after = repeat_after
        if rotation is not None:
            instance.rotation = rotation
        if start_date is not None:
            instance.start_date = start_date
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ModelsUpdateChallengeRequest:
        instance = cls()
        if not dict_:
            return instance
        if (
            "activeGoalsPerRotation" in dict_
            and dict_["activeGoalsPerRotation"] is not None
        ):
            instance.active_goals_per_rotation = int(dict_["activeGoalsPerRotation"])
        elif include_empty:
            instance.active_goals_per_rotation = 0
        if "assignmentRule" in dict_ and dict_["assignmentRule"] is not None:
            instance.assignment_rule = str(dict_["assignmentRule"])
        elif include_empty:
            instance.assignment_rule = Union[str, AssignmentRuleEnum]()
        if "description" in dict_ and dict_["description"] is not None:
            instance.description = str(dict_["description"])
        elif include_empty:
            instance.description = ""
        if "endAfter" in dict_ and dict_["endAfter"] is not None:
            instance.end_after = int(dict_["endAfter"])
        elif include_empty:
            instance.end_after = 0
        if "endDate" in dict_ and dict_["endDate"] is not None:
            instance.end_date = str(dict_["endDate"])
        elif include_empty:
            instance.end_date = ""
        if "goalsVisibility" in dict_ and dict_["goalsVisibility"] is not None:
            instance.goals_visibility = str(dict_["goalsVisibility"])
        elif include_empty:
            instance.goals_visibility = Union[str, GoalsVisibilityEnum]()
        if "name" in dict_ and dict_["name"] is not None:
            instance.name = str(dict_["name"])
        elif include_empty:
            instance.name = ""
        if "repeatAfter" in dict_ and dict_["repeatAfter"] is not None:
            instance.repeat_after = int(dict_["repeatAfter"])
        elif include_empty:
            instance.repeat_after = 0
        if "rotation" in dict_ and dict_["rotation"] is not None:
            instance.rotation = str(dict_["rotation"])
        elif include_empty:
            instance.rotation = Union[str, RotationEnum]()
        if "startDate" in dict_ and dict_["startDate"] is not None:
            instance.start_date = str(dict_["startDate"])
        elif include_empty:
            instance.start_date = ""
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ModelsUpdateChallengeRequest]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ModelsUpdateChallengeRequest]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        ModelsUpdateChallengeRequest,
        List[ModelsUpdateChallengeRequest],
        Dict[Any, ModelsUpdateChallengeRequest],
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
            "activeGoalsPerRotation": "active_goals_per_rotation",
            "assignmentRule": "assignment_rule",
            "description": "description",
            "endAfter": "end_after",
            "endDate": "end_date",
            "goalsVisibility": "goals_visibility",
            "name": "name",
            "repeatAfter": "repeat_after",
            "rotation": "rotation",
            "startDate": "start_date",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "activeGoalsPerRotation": False,
            "assignmentRule": False,
            "description": False,
            "endAfter": False,
            "endDate": False,
            "goalsVisibility": False,
            "name": False,
            "repeatAfter": False,
            "rotation": False,
            "startDate": False,
        }

    @staticmethod
    def get_enum_map() -> Dict[str, List[Any]]:
        return {
            "assignmentRule": ["FIXED", "RANDOMIZED", "UNSCHEDULED"],
            "goalsVisibility": ["PERIODONLY", "SHOWALL"],
            "rotation": ["DAILY", "MONTHLY", "NONE", "WEEKLY"],
        }

    # endregion static methods
