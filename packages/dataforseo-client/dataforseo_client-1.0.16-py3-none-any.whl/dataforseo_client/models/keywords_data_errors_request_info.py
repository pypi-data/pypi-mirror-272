# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class KeywordsDataErrorsRequestInfo(BaseModel):
    """
    KeywordsDataErrorsRequestInfo
    """ # noqa: E501
    limit: Optional[StrictInt] = Field(default=None, description="the maximum number of returned tasks that responded with an error optional field default value: 1000 maximum value: 1000")
    offset: Optional[StrictInt] = Field(default=None, description="offset in the results array of returned tasks optional field default value: 0 if you specify the 10 value, the first ten tasks in the results array will be omitted and the data will be provided for the successive tasks")
    filtered_function: Optional[StrictStr] = Field(default=None, description="return tasks with a certain function use this field to obtain a list of tasks that returned an error filtered by a certain function you can filter the results by the values you receive in the function fields of the API response i.e., once you receive unfiltered results, you can call this API again to filter them by function example: keywords_data/keywords_for_site/task_post, postback_url, pingback_url")
    datetime_from: Optional[StrictStr] = Field(default=None, description="start time for filtering results optional field allows filtering results by the datetime parameter within the range of the last 24 hours; must be specified in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2021-11-15 12:57:46 +00:00")
    datetime_to: Optional[StrictStr] = Field(default=None, description="finish time for filtering results optional field allows filtering results by the datetime parameter within the range of the last 24 hours; must be specified in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2021-11-15 13:57:46 +00:00")
    __properties: ClassVar[List[str]] = ["limit", "offset", "filtered_function", "datetime_from", "datetime_to"]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of KeywordsDataErrorsRequestInfo from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if limit (nullable) is None
        # and model_fields_set contains the field
        if self.limit is None and "limit" in self.model_fields_set:
            _dict['limit'] = None

        # set to None if offset (nullable) is None
        # and model_fields_set contains the field
        if self.offset is None and "offset" in self.model_fields_set:
            _dict['offset'] = None

        # set to None if filtered_function (nullable) is None
        # and model_fields_set contains the field
        if self.filtered_function is None and "filtered_function" in self.model_fields_set:
            _dict['filtered_function'] = None

        # set to None if datetime_from (nullable) is None
        # and model_fields_set contains the field
        if self.datetime_from is None and "datetime_from" in self.model_fields_set:
            _dict['datetime_from'] = None

        # set to None if datetime_to (nullable) is None
        # and model_fields_set contains the field
        if self.datetime_to is None and "datetime_to" in self.model_fields_set:
            _dict['datetime_to'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KeywordsDataErrorsRequestInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "filtered_function": obj.get("filtered_function"),
            "datetime_from": obj.get("datetime_from"),
            "datetime_to": obj.get("datetime_to")
        })
        return _obj


