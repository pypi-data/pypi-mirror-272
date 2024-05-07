# Copyright (c) 2021 AccelByte Inc. All Rights Reserved.
# This is licensed software from AccelByte Inc, for limitations
# and restrictions contact your company contract manager.
#
# Code generated. DO NOT EDIT!

# template file: model.j2

# AccelByte Gaming Services Chat Service

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


class MessageActionDeleteTopicResult(Model):
    """Message action delete topic result (message.ActionDeleteTopicResult)

    Properties:
        processed: (processed) REQUIRED int

        topic_id: (topicId) REQUIRED str
    """

    # region fields

    processed: int  # REQUIRED
    topic_id: str  # REQUIRED

    # endregion fields

    # region with_x methods

    def with_processed(self, value: int) -> MessageActionDeleteTopicResult:
        self.processed = value
        return self

    def with_topic_id(self, value: str) -> MessageActionDeleteTopicResult:
        self.topic_id = value
        return self

    # endregion with_x methods

    # region to methods

    def to_dict(self, include_empty: bool = False) -> dict:
        result: dict = {}
        if hasattr(self, "processed"):
            result["processed"] = int(self.processed)
        elif include_empty:
            result["processed"] = 0
        if hasattr(self, "topic_id"):
            result["topicId"] = str(self.topic_id)
        elif include_empty:
            result["topicId"] = ""
        return result

    # endregion to methods

    # region static methods

    @classmethod
    def create(
        cls, processed: int, topic_id: str, **kwargs
    ) -> MessageActionDeleteTopicResult:
        instance = cls()
        instance.processed = processed
        instance.topic_id = topic_id
        return instance

    @classmethod
    def create_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> MessageActionDeleteTopicResult:
        instance = cls()
        if not dict_:
            return instance
        if "processed" in dict_ and dict_["processed"] is not None:
            instance.processed = int(dict_["processed"])
        elif include_empty:
            instance.processed = 0
        if "topicId" in dict_ and dict_["topicId"] is not None:
            instance.topic_id = str(dict_["topicId"])
        elif include_empty:
            instance.topic_id = ""
        return instance

    @classmethod
    def create_many_from_dict(
        cls, dict_: dict, include_empty: bool = False
    ) -> Dict[str, MessageActionDeleteTopicResult]:
        return (
            {k: cls.create_from_dict(v, include_empty=include_empty) for k, v in dict_}
            if dict_
            else {}
        )

    @classmethod
    def create_many_from_list(
        cls, list_: list, include_empty: bool = False
    ) -> List[MessageActionDeleteTopicResult]:
        return (
            [cls.create_from_dict(i, include_empty=include_empty) for i in list_]
            if list_
            else []
        )

    @classmethod
    def create_from_any(
        cls, any_: any, include_empty: bool = False, many: bool = False
    ) -> Union[
        MessageActionDeleteTopicResult,
        List[MessageActionDeleteTopicResult],
        Dict[Any, MessageActionDeleteTopicResult],
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
            "processed": "processed",
            "topicId": "topic_id",
        }

    @staticmethod
    def get_required_map() -> Dict[str, bool]:
        return {
            "processed": True,
            "topicId": True,
        }

    # endregion static methods
