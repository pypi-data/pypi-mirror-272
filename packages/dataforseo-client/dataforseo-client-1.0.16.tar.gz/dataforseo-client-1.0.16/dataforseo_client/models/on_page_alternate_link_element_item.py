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

from pydantic import Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.base_on_page_link_item_info import BaseOnPageLinkItemInfo
from typing import Optional, Set
from typing_extensions import Self

class OnPageAlternateLinkElementItem(BaseOnPageLinkItemInfo):
    """
    OnPageAlternateLinkElementItem
    """ # noqa: E501
    domain_from: Optional[StrictStr] = Field(default=None, description="referring domain the link was found on this domain")
    domain_to: Optional[StrictStr] = Field(default=None, description="referenced domain the link is pointing to this domain")
    page_from: Optional[StrictStr] = Field(default=None, description="referring page relative URL of the page on which the link was found")
    page_to: Optional[StrictStr] = Field(default=None, description="referenced page relative URL of the page to which the link is pointing")
    link_from: Optional[StrictStr] = Field(default=None, description="referring page absolute URL of the page on which the link was found")
    link_to: Optional[StrictStr] = Field(default=None, description="referenced page absolute URL of the page to which the link is pointing")
    dofollow: Optional[StrictBool] = Field(default=None, description="indicates whether the link is dofollow if the value is true, the link doesn’t have a rel=\"nofollow\" attribute")
    page_from_scheme: Optional[StrictStr] = Field(default=None, description="url scheme of the referring page")
    page_to_scheme: Optional[StrictStr] = Field(default=None, description="url scheme of the referenced page")
    direction: Optional[StrictStr] = Field(default=None, description="direction of the link possible values: internal, external")
    is_broken: Optional[StrictBool] = Field(default=None, description="link is broken indicates whether a link is directing to a broken page or resource")
    is_link_relation_conflict: Optional[StrictBool] = Field(default=None, description="indicates that the link may have a conflict with another link if true, at least one link pointing to link_to has a rel=\"nofollow\" attribute and at least one is dofollow")
    page_to_status_code: Optional[StrictInt] = Field(default=None, description="status code of the referenced page status code of the page to which the link is pointing")
    __properties: ClassVar[List[str]] = ["type", "domain_from", "domain_to", "page_from", "page_to", "link_from", "link_to", "dofollow", "page_from_scheme", "page_to_scheme", "direction", "is_broken", "is_link_relation_conflict", "page_to_status_code"]

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
        """Create an instance of OnPageAlternateLinkElementItem from a JSON string"""
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
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if domain_from (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from is None and "domain_from" in self.model_fields_set:
            _dict['domain_from'] = None

        # set to None if domain_to (nullable) is None
        # and model_fields_set contains the field
        if self.domain_to is None and "domain_to" in self.model_fields_set:
            _dict['domain_to'] = None

        # set to None if page_from (nullable) is None
        # and model_fields_set contains the field
        if self.page_from is None and "page_from" in self.model_fields_set:
            _dict['page_from'] = None

        # set to None if page_to (nullable) is None
        # and model_fields_set contains the field
        if self.page_to is None and "page_to" in self.model_fields_set:
            _dict['page_to'] = None

        # set to None if link_from (nullable) is None
        # and model_fields_set contains the field
        if self.link_from is None and "link_from" in self.model_fields_set:
            _dict['link_from'] = None

        # set to None if link_to (nullable) is None
        # and model_fields_set contains the field
        if self.link_to is None and "link_to" in self.model_fields_set:
            _dict['link_to'] = None

        # set to None if dofollow (nullable) is None
        # and model_fields_set contains the field
        if self.dofollow is None and "dofollow" in self.model_fields_set:
            _dict['dofollow'] = None

        # set to None if page_from_scheme (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_scheme is None and "page_from_scheme" in self.model_fields_set:
            _dict['page_from_scheme'] = None

        # set to None if page_to_scheme (nullable) is None
        # and model_fields_set contains the field
        if self.page_to_scheme is None and "page_to_scheme" in self.model_fields_set:
            _dict['page_to_scheme'] = None

        # set to None if direction (nullable) is None
        # and model_fields_set contains the field
        if self.direction is None and "direction" in self.model_fields_set:
            _dict['direction'] = None

        # set to None if is_broken (nullable) is None
        # and model_fields_set contains the field
        if self.is_broken is None and "is_broken" in self.model_fields_set:
            _dict['is_broken'] = None

        # set to None if is_link_relation_conflict (nullable) is None
        # and model_fields_set contains the field
        if self.is_link_relation_conflict is None and "is_link_relation_conflict" in self.model_fields_set:
            _dict['is_link_relation_conflict'] = None

        # set to None if page_to_status_code (nullable) is None
        # and model_fields_set contains the field
        if self.page_to_status_code is None and "page_to_status_code" in self.model_fields_set:
            _dict['page_to_status_code'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of OnPageAlternateLinkElementItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "domain_from": obj.get("domain_from"),
            "domain_to": obj.get("domain_to"),
            "page_from": obj.get("page_from"),
            "page_to": obj.get("page_to"),
            "link_from": obj.get("link_from"),
            "link_to": obj.get("link_to"),
            "dofollow": obj.get("dofollow"),
            "page_from_scheme": obj.get("page_from_scheme"),
            "page_to_scheme": obj.get("page_to_scheme"),
            "direction": obj.get("direction"),
            "is_broken": obj.get("is_broken"),
            "is_link_relation_conflict": obj.get("is_link_relation_conflict"),
            "page_to_status_code": obj.get("page_to_status_code")
        })
        return _obj


