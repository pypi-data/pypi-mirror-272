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

# AccelByte Gaming Services Iam Service

from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

from accelbyte_py_sdk.core import Operation
from accelbyte_py_sdk.core import HeaderStr
from accelbyte_py_sdk.core import HttpResponse
from accelbyte_py_sdk.core import deprecated

from ...models import OauthcommonJWKSet


class GetJWKS(Operation):
    """[DEPRECATED] JSON Web Key Set for verifying JWT (GetJWKS)

    ## The endpoint is going to be deprecated
    This endpoint serves public keys for verifying JWT access tokens generated by this service.

    When a client application wants to verify a JWT token, it needs to get the 'kid' value found in the JWT token header and use it
    to look up the corresponding public key from a set returned by this endpoint. The client application can then use that public key to verify the JWT.

    A client application might cache the keys so it doesn't need to do request every time it needs to verify a JWT token. If a client application
    caches the keys and a key with the same 'kid' cannot be found in the cache, it should then try to refresh the keys by making a request to this
    endpoint again.

    Please refer to the RFC for more information about JWK (JSON Web Key): https://tools.ietf.org/html/rfc7517

    ### Endpoint migration guide
    - **Substitute endpoint: _/iam/v3/oauth/jwks [GET]_**

    Properties:
        url: /iam/oauth/jwks

        method: GET

        tags: ["OAuth"]

        consumes: [""]

        produces: ["application/json"]

        securities: [BEARER_AUTH]

    Responses:
        200: OK - OauthcommonJWKSet (JWKS returned)
    """

    # region fields

    _url: str = "/iam/oauth/jwks"
    _path: str = "/iam/oauth/jwks"
    _base_path: str = ""
    _method: str = "GET"
    _consumes: List[str] = [""]
    _produces: List[str] = ["application/json"]
    _securities: List[List[str]] = [["BEARER_AUTH"]]
    _location_query: str = None

    service_name: Optional[str] = "iam"

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
        return {}

    # endregion get_x_params methods

    # region is/has methods

    # endregion is/has methods

    # region with_x methods

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        return result

    # endregion to methods

    # region response methods

    # noinspection PyMethodMayBeStatic
    def parse_response(
        self, code: int, content_type: str, content: Any
    ) -> Tuple[Union[None, OauthcommonJWKSet], Union[None, HttpResponse]]:
        """Parse the given response.

        200: OK - OauthcommonJWKSet (JWKS returned)

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
            return OauthcommonJWKSet.create_from_dict(content), None

        return self.handle_undocumented_response(
            code=code, content_type=content_type, content=content
        )

    # endregion response methods

    # region static methods

    @classmethod
    def create(cls, **kwargs) -> GetJWKS:
        instance = cls()
        if x_flight_id := kwargs.get("x_flight_id", None):
            instance.x_flight_id = x_flight_id
        return instance

    @classmethod
    def create_from_dict(cls, dict_: dict, include_empty: bool = False) -> GetJWKS:
        instance = cls()
        return instance

    @staticmethod
    def get_field_info() -> Dict[str, str]:
        return {}

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {}

    # endregion static methods
