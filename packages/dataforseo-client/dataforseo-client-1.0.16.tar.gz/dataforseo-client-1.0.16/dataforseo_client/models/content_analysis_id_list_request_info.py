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

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ContentAnalysisIdListRequestInfo(BaseModel):
    """
    ContentAnalysisIdListRequestInfo
    """ # noqa: E501
    datetime_from: Optional[StrictStr] = Field(default=None, description="start time for filtering results required field if include_metadata is set to true, maximum value: a month from current datetime; if include_metadata is set to false, maximum value: six months from current datetime; must be specified in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2023-01-15 12:57:46 +00:00")
    datetime_to: Optional[StrictStr] = Field(default=None, description="finish time for filtering results required field maximum value: current datetime; must be specified in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2023-01-31 13:57:46 +00:00")
    limit: Optional[StrictInt] = Field(default=None, description="the maximum number of returned task IDs optional field default value: 1000 maximum value: 1000")
    offset: Optional[StrictInt] = Field(default=None, description="offset in the results array of returned task IDs optional field default value: 0 if you specify the 10 value, the first ten tasks in the results array will be omitted")
    sort: Optional[StrictStr] = Field(default=None, description="sorting by task execution time optional field possible values: \"asc\", \"desc\" default value: \"asc\"")
    include_metadata: Optional[StrictBool] = Field(default=None, description="include task metadata in the respond optional field default value: false")
    __properties: ClassVar[List[str]] = ["datetime_from", "datetime_to", "limit", "offset", "sort", "include_metadata"]

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
        """Create an instance of ContentAnalysisIdListRequestInfo from a JSON string"""
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

        # set to None if sort (nullable) is None
        # and model_fields_set contains the field
        if self.sort is None and "sort" in self.model_fields_set:
            _dict['sort'] = None

        # set to None if include_metadata (nullable) is None
        # and model_fields_set contains the field
        if self.include_metadata is None and "include_metadata" in self.model_fields_set:
            _dict['include_metadata'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ContentAnalysisIdListRequestInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "datetime_from": obj.get("datetime_from"),
            "datetime_to": obj.get("datetime_to"),
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "sort": obj.get("sort"),
            "include_metadata": obj.get("include_metadata")
        })
        return _obj


