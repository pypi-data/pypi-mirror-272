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

from pydantic import BaseModel, Field
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.page_section_content_info import PageSectionContentInfo
from dataforseo_client.models.topic_info import TopicInfo
from typing import Optional, Set
from typing_extensions import Self

class PageContentInfo(BaseModel):
    """
    PageContentInfo
    """ # noqa: E501
    header: Optional[PageSectionContentInfo] = None
    footer: Optional[PageSectionContentInfo] = None
    main_topic: Optional[List[TopicInfo]] = Field(default=None, description="main topic on the page you can find more information about topic priority calculation in this help center article")
    secondary_topic: Optional[List[TopicInfo]] = Field(default=None, description="secondary topic on the page you can find more information about topic priority calculation in this help center article")
    __properties: ClassVar[List[str]] = ["header", "footer", "main_topic", "secondary_topic"]

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
        """Create an instance of PageContentInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of header
        if self.header:
            _dict['header'] = self.header.to_dict()
        # override the default output from pydantic by calling `to_dict()` of footer
        if self.footer:
            _dict['footer'] = self.footer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in main_topic (list)
        _items = []
        if self.main_topic:
            for _item in self.main_topic:
                if _item:
                    _items.append(_item.to_dict())
            _dict['main_topic'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in secondary_topic (list)
        _items = []
        if self.secondary_topic:
            for _item in self.secondary_topic:
                if _item:
                    _items.append(_item.to_dict())
            _dict['secondary_topic'] = _items
        # set to None if main_topic (nullable) is None
        # and model_fields_set contains the field
        if self.main_topic is None and "main_topic" in self.model_fields_set:
            _dict['main_topic'] = None

        # set to None if secondary_topic (nullable) is None
        # and model_fields_set contains the field
        if self.secondary_topic is None and "secondary_topic" in self.model_fields_set:
            _dict['secondary_topic'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PageContentInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "header": PageSectionContentInfo.from_dict(obj["header"]) if obj.get("header") is not None else None,
            "footer": PageSectionContentInfo.from_dict(obj["footer"]) if obj.get("footer") is not None else None,
            "main_topic": [TopicInfo.from_dict(_item) for _item in obj["main_topic"]] if obj.get("main_topic") is not None else None,
            "secondary_topic": [TopicInfo.from_dict(_item) for _item in obj["secondary_topic"]] if obj.get("secondary_topic") is not None else None
        })
        return _obj


