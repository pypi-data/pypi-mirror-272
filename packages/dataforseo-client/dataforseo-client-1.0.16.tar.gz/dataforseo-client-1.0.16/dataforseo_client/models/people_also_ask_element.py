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

from pydantic import BaseModel, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.people_also_ask_expanded_element import PeopleAlsoAskExpandedElement
from typing import Optional, Set
from typing_extensions import Self

class PeopleAlsoAskElement(BaseModel):
    """
    PeopleAlsoAskElement
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    title: Optional[StrictStr] = Field(default=None, description="title of a given link element")
    seed_question: Optional[StrictStr] = Field(default=None, description="question that triggered additional expanded elements")
    xpath: Optional[StrictStr] = Field(default=None, description="the XPath of the element")
    expanded_element: Optional[List[PeopleAlsoAskExpandedElement]] = Field(default=None, description="expanded element")
    __properties: ClassVar[List[str]] = ["type", "title", "seed_question", "xpath", "expanded_element"]

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
        """Create an instance of PeopleAlsoAskElement from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in expanded_element (list)
        _items = []
        if self.expanded_element:
            for _item in self.expanded_element:
                if _item:
                    _items.append(_item.to_dict())
            _dict['expanded_element'] = _items
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if title (nullable) is None
        # and model_fields_set contains the field
        if self.title is None and "title" in self.model_fields_set:
            _dict['title'] = None

        # set to None if seed_question (nullable) is None
        # and model_fields_set contains the field
        if self.seed_question is None and "seed_question" in self.model_fields_set:
            _dict['seed_question'] = None

        # set to None if xpath (nullable) is None
        # and model_fields_set contains the field
        if self.xpath is None and "xpath" in self.model_fields_set:
            _dict['xpath'] = None

        # set to None if expanded_element (nullable) is None
        # and model_fields_set contains the field
        if self.expanded_element is None and "expanded_element" in self.model_fields_set:
            _dict['expanded_element'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PeopleAlsoAskElement from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "title": obj.get("title"),
            "seed_question": obj.get("seed_question"),
            "xpath": obj.get("xpath"),
            "expanded_element": [PeopleAlsoAskExpandedElement.from_dict(_item) for _item in obj["expanded_element"]] if obj.get("expanded_element") is not None else None
        })
        return _obj


