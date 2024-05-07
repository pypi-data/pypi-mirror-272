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

from pydantic import BaseModel, Field, StrictInt
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class BusinessListingAggregationInfo(BaseModel):
    """
    BusinessListingAggregationInfo
    """ # noqa: E501
    top_categories: Optional[Dict[str, Optional[StrictInt]]] = Field(default=None, description="the most mentioned related categories top categories displayed with the number of businesses in each category")
    top_countries: Optional[Dict[str, Optional[StrictInt]]] = Field(default=None, description="the most mentioned counties country codes with the biggest number of businesses in the category")
    websites_count: Optional[StrictInt] = Field(default=None, description="number of unique websites")
    count: Optional[StrictInt] = Field(default=None, description="number of unique entities")
    top_attributes: Optional[Dict[str, Optional[StrictInt]]] = Field(default=None, description="the most mentioned service details service details of a business entity displayed in a form of checks and the number of entities mentioning each attribute")
    top_place_topics: Optional[Dict[str, Optional[StrictInt]]] = Field(default=None, description="top keywords mentioned in customer reviews contains most popular keywords related to products/services mentioned in customer reviews of a business entity and the number of reviews mentioning each keyword")
    __properties: ClassVar[List[str]] = ["top_categories", "top_countries", "websites_count", "count", "top_attributes", "top_place_topics"]

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
        """Create an instance of BusinessListingAggregationInfo from a JSON string"""
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
        # set to None if top_categories (nullable) is None
        # and model_fields_set contains the field
        if self.top_categories is None and "top_categories" in self.model_fields_set:
            _dict['top_categories'] = None

        # set to None if top_countries (nullable) is None
        # and model_fields_set contains the field
        if self.top_countries is None and "top_countries" in self.model_fields_set:
            _dict['top_countries'] = None

        # set to None if websites_count (nullable) is None
        # and model_fields_set contains the field
        if self.websites_count is None and "websites_count" in self.model_fields_set:
            _dict['websites_count'] = None

        # set to None if count (nullable) is None
        # and model_fields_set contains the field
        if self.count is None and "count" in self.model_fields_set:
            _dict['count'] = None

        # set to None if top_attributes (nullable) is None
        # and model_fields_set contains the field
        if self.top_attributes is None and "top_attributes" in self.model_fields_set:
            _dict['top_attributes'] = None

        # set to None if top_place_topics (nullable) is None
        # and model_fields_set contains the field
        if self.top_place_topics is None and "top_place_topics" in self.model_fields_set:
            _dict['top_place_topics'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BusinessListingAggregationInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "top_categories": obj.get("top_categories"),
            "top_countries": obj.get("top_countries"),
            "websites_count": obj.get("websites_count"),
            "count": obj.get("count"),
            "top_attributes": obj.get("top_attributes"),
            "top_place_topics": obj.get("top_place_topics")
        })
        return _obj


