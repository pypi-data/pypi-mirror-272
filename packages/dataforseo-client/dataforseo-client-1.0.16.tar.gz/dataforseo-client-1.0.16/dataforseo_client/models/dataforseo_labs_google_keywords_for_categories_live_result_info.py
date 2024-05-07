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
from dataforseo_client.models.keyword_data_info import KeywordDataInfo
from typing import Optional, Set
from typing_extensions import Self

class DataforseoLabsGoogleKeywordsForCategoriesLiveResultInfo(BaseModel):
    """
    DataforseoLabsGoogleKeywordsForCategoriesLiveResultInfo
    """ # noqa: E501
    se_type: Optional[StrictStr] = Field(default=None, description="search engine type")
    seed_categories: Optional[List[Optional[StrictInt]]] = Field(default=None, description="categories in a POST array")
    location_code: Optional[StrictInt] = Field(default=None, description="location code in a POST array")
    language_code: Optional[StrictStr] = Field(default=None, description="language code in a POST array")
    total_count: Optional[StrictInt] = Field(default=None, description="the total amount of results in our database relevant to your request")
    items_count: Optional[StrictInt] = Field(default=None, description="the number of results returned in the items array")
    offset: Optional[StrictInt] = Field(default=None, description="current offset value")
    offset_token: Optional[StrictStr] = Field(default=None, description="offset token for subsequent requests you can use the string provided in this field to get the subsequent results of the initial task; note: offset_token values are unique for each subsequent task")
    items: Optional[List[KeywordDataInfo]] = Field(default=None, description="contains keyword ideas and related data")
    __properties: ClassVar[List[str]] = ["se_type", "seed_categories", "location_code", "language_code", "total_count", "items_count", "offset", "offset_token", "items"]

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
        """Create an instance of DataforseoLabsGoogleKeywordsForCategoriesLiveResultInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in items (list)
        _items = []
        if self.items:
            for _item in self.items:
                if _item:
                    _items.append(_item.to_dict())
            _dict['items'] = _items
        # set to None if se_type (nullable) is None
        # and model_fields_set contains the field
        if self.se_type is None and "se_type" in self.model_fields_set:
            _dict['se_type'] = None

        # set to None if seed_categories (nullable) is None
        # and model_fields_set contains the field
        if self.seed_categories is None and "seed_categories" in self.model_fields_set:
            _dict['seed_categories'] = None

        # set to None if location_code (nullable) is None
        # and model_fields_set contains the field
        if self.location_code is None and "location_code" in self.model_fields_set:
            _dict['location_code'] = None

        # set to None if language_code (nullable) is None
        # and model_fields_set contains the field
        if self.language_code is None and "language_code" in self.model_fields_set:
            _dict['language_code'] = None

        # set to None if total_count (nullable) is None
        # and model_fields_set contains the field
        if self.total_count is None and "total_count" in self.model_fields_set:
            _dict['total_count'] = None

        # set to None if items_count (nullable) is None
        # and model_fields_set contains the field
        if self.items_count is None and "items_count" in self.model_fields_set:
            _dict['items_count'] = None

        # set to None if offset (nullable) is None
        # and model_fields_set contains the field
        if self.offset is None and "offset" in self.model_fields_set:
            _dict['offset'] = None

        # set to None if offset_token (nullable) is None
        # and model_fields_set contains the field
        if self.offset_token is None and "offset_token" in self.model_fields_set:
            _dict['offset_token'] = None

        # set to None if items (nullable) is None
        # and model_fields_set contains the field
        if self.items is None and "items" in self.model_fields_set:
            _dict['items'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataforseoLabsGoogleKeywordsForCategoriesLiveResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "se_type": obj.get("se_type"),
            "seed_categories": obj.get("seed_categories"),
            "location_code": obj.get("location_code"),
            "language_code": obj.get("language_code"),
            "total_count": obj.get("total_count"),
            "items_count": obj.get("items_count"),
            "offset": obj.get("offset"),
            "offset_token": obj.get("offset_token"),
            "items": [KeywordDataInfo.from_dict(_item) for _item in obj["items"]] if obj.get("items") is not None else None
        })
        return _obj


