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

from pydantic import Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.base_dataforseo_trends_item import BaseDataforseoTrendsItem
from dataforseo_client.models.demography import Demography
from typing import Optional, Set
from typing_extensions import Self

class DataforseoTrendsDemographyElementItem(BaseDataforseoTrendsItem):
    """
    DataforseoTrendsDemographyElementItem
    """ # noqa: E501
    position: Optional[StrictInt] = Field(default=None, description="the alignment of the element can take the following values: 1, 2, 3, 4, etc.")
    keywords: Optional[List[Optional[StrictStr]]] = Field(default=None, description="relevant keywords the data included in the interests and interests_comparison is based on the keywords listed in this array")
    demography: Optional[Demography] = None
    demography_comparison: Optional[Dict[str, Any]] = Field(default=None, description="comparison of demographic data on keyword popularity for the specified parameters conains keyword popularity data by age and gender if you specified a single keyword, the value will be null")
    __properties: ClassVar[List[str]] = ["type", "position", "keywords", "demography", "demography_comparison"]

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
        """Create an instance of DataforseoTrendsDemographyElementItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of demography
        if self.demography:
            _dict['demography'] = self.demography.to_dict()
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if position (nullable) is None
        # and model_fields_set contains the field
        if self.position is None and "position" in self.model_fields_set:
            _dict['position'] = None

        # set to None if keywords (nullable) is None
        # and model_fields_set contains the field
        if self.keywords is None and "keywords" in self.model_fields_set:
            _dict['keywords'] = None

        # set to None if demography_comparison (nullable) is None
        # and model_fields_set contains the field
        if self.demography_comparison is None and "demography_comparison" in self.model_fields_set:
            _dict['demography_comparison'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataforseoTrendsDemographyElementItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "position": obj.get("position"),
            "keywords": obj.get("keywords"),
            "demography": Demography.from_dict(obj["demography"]) if obj.get("demography") is not None else None,
            "demography_comparison": obj.get("demography_comparison")
        })
        return _obj


