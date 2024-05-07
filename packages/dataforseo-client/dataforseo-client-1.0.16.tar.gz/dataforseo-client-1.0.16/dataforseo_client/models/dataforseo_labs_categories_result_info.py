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

class DataforseoLabsCategoriesResultInfo(BaseModel):
    """
    DataforseoLabsCategoriesResultInfo
    """ # noqa: E501
    category_code: Optional[StrictInt] = Field(default=None, description="category code")
    category_name: Optional[StrictStr] = Field(default=None, description="full name of the category")
    category_code_parent: Optional[StrictInt] = Field(default=None, description="the code of the superordinate category example: \"category_code\": 10178, \"category_name\": \"Apparel Accessories\", \"category_code_parent\": 10021 where category_code_parent corresponds to: \"category_code\": 10021, \"category_name\": \"Apparel\" \"category_code_parent\": null")
    __properties: ClassVar[List[str]] = ["category_code", "category_name", "category_code_parent"]

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
        """Create an instance of DataforseoLabsCategoriesResultInfo from a JSON string"""
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
        # set to None if category_code (nullable) is None
        # and model_fields_set contains the field
        if self.category_code is None and "category_code" in self.model_fields_set:
            _dict['category_code'] = None

        # set to None if category_name (nullable) is None
        # and model_fields_set contains the field
        if self.category_name is None and "category_name" in self.model_fields_set:
            _dict['category_name'] = None

        # set to None if category_code_parent (nullable) is None
        # and model_fields_set contains the field
        if self.category_code_parent is None and "category_code_parent" in self.model_fields_set:
            _dict['category_code_parent'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataforseoLabsCategoriesResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "category_code": obj.get("category_code"),
            "category_name": obj.get("category_name"),
            "category_code_parent": obj.get("category_code_parent")
        })
        return _obj


