# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: ags_py_codegen

# pylint: disable=duplicate-code
# pylint: disable=line-too-long
# pylint: disable=missing-function-docstring
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

from typing import Any, Dict, List, Optional, Tuple, Union

from ....core import HeaderStr
from ....core import get_namespace as get_services_namespace
from ....core import run_request
from ....core import run_request_async
from ....core import same_doc_as

from ..models import ResponseErrorResponse

from ..operations.auth import AuthCheck


@same_doc_as(AuthCheck)
def auth_check(x_additional_headers: Optional[Dict[str, str]] = None, **kwargs):
    """checks if fleet commander can auth with AMS (AuthCheck)

    Check if fleet commander is authorized to talk to AMS with this IAM

    Properties:
        url: /ams/auth

        method: GET

        tags: ["Auth"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

    Responses:
        200: OK - (success)

        401: Unauthorized - ResponseErrorResponse (unauthorized)

        403: Forbidden - ResponseErrorResponse (forbidden)

        500: Internal Server Error - ResponseErrorResponse (internal server error)
    """
    request = AuthCheck.create()
    return run_request(request, additional_headers=x_additional_headers, **kwargs)


@same_doc_as(AuthCheck)
async def auth_check_async(
    x_additional_headers: Optional[Dict[str, str]] = None, **kwargs
):
    """checks if fleet commander can auth with AMS (AuthCheck)

    Check if fleet commander is authorized to talk to AMS with this IAM

    Properties:
        url: /ams/auth

        method: GET

        tags: ["Auth"]

        consumes: ["application/json"]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

    Responses:
        200: OK - (success)

        401: Unauthorized - ResponseErrorResponse (unauthorized)

        403: Forbidden - ResponseErrorResponse (forbidden)

        500: Internal Server Error - ResponseErrorResponse (internal server error)
    """
    request = AuthCheck.create()
    return await run_request_async(
        request, additional_headers=x_additional_headers, **kwargs
    )
