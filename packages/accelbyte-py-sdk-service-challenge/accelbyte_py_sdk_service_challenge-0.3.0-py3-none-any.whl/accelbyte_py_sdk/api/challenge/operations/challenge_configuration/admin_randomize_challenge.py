# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: operation.j2

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

# AccelByte Gaming Services Challenge Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from accelbyte_py_sdk.core import Operation
from accelbyte_py_sdk.core import HeaderStr
from accelbyte_py_sdk.core import HttpResponse

from ...models import IamErrorResponse
from ...models import ModelSchedule
from ...models import ResponseError


class AdminRandomizeChallenge(Operation):
    """Randomize Goals of a Challenge (adminRandomizeChallenge)

    * Required permission: ADMIN:NAMESPACE:{namespace}:CHALLENGE [UPDATE]
    This is a utility endpoint to execute randomize goals schedule on challenge that the assignmentRule is RANDOMIZED.

    Required Permission(s):
        - ADMIN:NAMESPACE:{namespace}:CHALLENGE [UPDATE]

    Properties:
        url: /challenge/v1/admin/namespaces/{namespace}/challenges/{challengeCode}/randomize

        method: POST

        tags: ["Challenge Configuration"]

        consumes: []

        produces: ["application/json"]

        securities: [BEARER_AUTH]

        challenge_code: (challengeCode) REQUIRED str in path

        namespace: (namespace) REQUIRED str in path

    Responses:
        200: OK - List[ModelSchedule] (OK)

        401: Unauthorized - IamErrorResponse (20001: unauthorized access)

        403: Forbidden - IamErrorResponse (20013: insufficient permission)

        404: Not Found - ResponseError (20029: not found)

        500: Internal Server Error - ResponseError (20000: internal server error: {{message}})
    """

    # region fields

    _url: str = "/challenge/v1/admin/namespaces/{namespace}/challenges/{challengeCode}/randomize"
    _path: str = "/challenge/v1/admin/namespaces/{namespace}/challenges/{challengeCode}/randomize"
    _base_path: str = ""
    _method: str = "POST"
    _consumes: List[str] = []
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    service_name: Optional[str] = "challenge"

    challenge_code: str  # REQUIRED in [path]
    namespace: str  # REQUIRED in [path]

    # endregion fields

    # region properties

    @property
    def url(self) -> str:
        return self._url

    @property
    def path(self) -> str:
        return self._path

    @property
    def base_path(self) -> str:
        return self._base_path

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
        }

    def get_path_params(self) -> dict:
        result = {}
        if hasattr(self, "challenge_code"):
            result["challengeCode"] = self.challenge_code
        if hasattr(self, "namespace"):
            result["namespace"] = self.namespace
        return result

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    def with_challenge_code(self, value: str) -> AdminRandomizeChallenge:
        self.challenge_code = value
        return self

    def with_namespace(self, value: str) -> AdminRandomizeChallenge:
        self.namespace = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "challenge_code") and self.challenge_code:
            result["challengeCode"] = str(self.challenge_code)
        elif include_empty:
            result["challengeCode"] = ""
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
    ) -> Tuple[
        Union[None, List[ModelSchedule]],
        Union[None, HttpResponse, IamErrorResponse, ResponseError],
    ]:
        """Parse the given response.

        200: OK - List[ModelSchedule] (OK)

        401: Unauthorized - IamErrorResponse (20001: unauthorized access)

        403: Forbidden - IamErrorResponse (20013: insufficient permission)

        404: Not Found - ResponseError (20029: not found)

        500: Internal Server Error - ResponseError (20000: internal server error: {{message}})

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
            return [ModelSchedule.create_from_dict(i) for i in content], None
        if code == 401:
            return None, IamErrorResponse.create_from_dict(content)
        if code == 403:
            return None, IamErrorResponse.create_from_dict(content)
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
        cls, challenge_code: str, namespace: str, **kwargs
    ) -> AdminRandomizeChallenge:
        instance = cls()
        instance.challenge_code = challenge_code
        instance.namespace = namespace
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> AdminRandomizeChallenge:
        instance = cls()
        if "challengeCode" in dict_ and dict_["challengeCode"] is not None:
            instance.challenge_code = str(dict_["challengeCode"])
        elif include_empty:
            instance.challenge_code = ""
        if "namespace" in dict_ and dict_["namespace"] is not None:
            instance.namespace = str(dict_["namespace"])
        elif include_empty:
            instance.namespace = ""
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {
            "challengeCode": "challenge_code",
            "namespace": "namespace",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "challengeCode": True,
            "namespace": True,
        }

    # endregion static methods
