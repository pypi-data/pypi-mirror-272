# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: model.j2

# AccelByte Gaming Services Iam Service

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

from ..models.clientmodel_client_update_v3_request import (
    ClientmodelClientUpdateV3Request,
)


class ClientmodelClientsUpdateRequestV3(Model):
    """Clientmodel clients update request V3 (clientmodel.ClientsUpdateRequestV3)

    Properties:
        client_ids: (clientIds) REQUIRED List[str]

        client_update_request: (clientUpdateRequest) REQUIRED ClientmodelClientUpdateV3Request
    """

    # region fields

    client_ids: List[str]  # REQUIRED
    client_update_request: ClientmodelClientUpdateV3Request  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_client_ids(self, value: List[str]) -> ClientmodelClientsUpdateRequestV3:
        self.client_ids = value
        return self

    def with_client_update_request(
        self, value: ClientmodelClientUpdateV3Request
    ) -> ClientmodelClientsUpdateRequestV3:
        self.client_update_request = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "client_ids"):
            result["clientIds"] = [str(i0) for i0 in self.client_ids]
        elif include_empty:
            result["clientIds"] = []
        if hasattr(self, "client_update_request"):
            result["clientUpdateRequest"] = self.client_update_request.to_dict(
                include_empty=include_empty
            )
        elif include_empty:
            result["clientUpdateRequest"] = ClientmodelClientUpdateV3Request()
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls,
        client_ids: List[str],
        client_update_request: ClientmodelClientUpdateV3Request,
        **kwargs,
    ) -> ClientmodelClientsUpdateRequestV3:
        instance = cls()
        instance.client_ids = client_ids
        instance.client_update_request = client_update_request
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> ClientmodelClientsUpdateRequestV3:
        instance = cls()
        if not dict_:
            return instance
        if "clientIds" in dict_ and dict_["clientIds"] is not None:
            instance.client_ids = [str(i0) for i0 in dict_["clientIds"]]
        elif include_empty:
            instance.client_ids = []
        if "clientUpdateRequest" in dict_ and dict_["clientUpdateRequest"] is not None:
            instance.client_update_request = (
                ClientmodelClientUpdateV3Request.create_from_dict(
                    dict_["clientUpdateRequest"], include_empty=include_empty
                )
            )
        elif include_empty:
            instance.client_update_request = ClientmodelClientUpdateV3Request()
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, ClientmodelClientsUpdateRequestV3]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[ClientmodelClientsUpdateRequestV3]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        ClientmodelClientsUpdateRequestV3,
        List[ClientmodelClientsUpdateRequestV3],
        Dict[Any, ClientmodelClientsUpdateRequestV3],
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
            "clientIds": "client_ids",
            "clientUpdateRequest": "client_update_request",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "clientIds": True,
            "clientUpdateRequest": True,
        }

    # endregion static methods
