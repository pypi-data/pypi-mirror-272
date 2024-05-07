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
from dataforseo_client.models.technologies_info import TechnologiesInfo
from typing import Optional, Set
from typing_extensions import Self

class DomainAnalyticsTechnologiesDomainsByLiveItem(BaseModel):
    """
    items array
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    domain: Optional[StrictStr] = Field(default=None, description="specified domain name")
    title: Optional[StrictStr] = Field(default=None, description="domain meta title")
    description: Optional[StrictStr] = Field(default=None, description="domain meta description")
    meta_keywords: Optional[List[Optional[StrictStr]]] = Field(default=None, description="domain meta keywords")
    domain_rank: Optional[StrictStr] = Field(default=None, description="backlink rank of the target domain learn more about the metric and how it is calculated in this help center article")
    last_visited: Optional[StrictStr] = Field(default=None, description="most recent date when our crawler visited the domain in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2022-10-10 12:57:46 +00:00")
    country_iso_code: Optional[StrictStr] = Field(default=None, description="domain ISO code ISO code of the country that target domain is determined to belong to")
    language_code: Optional[StrictStr] = Field(default=None, description="domain language code of the language that target domain is determined to be associated with")
    content_language_code: Optional[StrictStr] = Field(default=None, description="content language code of the language that content on the target domain is written with")
    phone_numbers: Optional[List[Optional[StrictStr]]] = Field(default=None, description="phone numbers of the target contact phone numbers indicated on the target website")
    emails: Optional[List[Optional[StrictStr]]] = Field(default=None, description="emails of the target emails indicated on the target website")
    social_graph_urls: Optional[List[Optional[StrictStr]]] = Field(default=None, description="social media links and handles social media URLs detected in the social graphs of the target website")
    technologies: Optional[TechnologiesInfo] = None
    __properties: ClassVar[List[str]] = ["type", "domain", "title", "description", "meta_keywords", "domain_rank", "last_visited", "country_iso_code", "language_code", "content_language_code", "phone_numbers", "emails", "social_graph_urls", "technologies"]

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
        """Create an instance of DomainAnalyticsTechnologiesDomainsByLiveItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of technologies
        if self.technologies:
            _dict['technologies'] = self.technologies.to_dict()
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if domain (nullable) is None
        # and model_fields_set contains the field
        if self.domain is None and "domain" in self.model_fields_set:
            _dict['domain'] = None

        # set to None if title (nullable) is None
        # and model_fields_set contains the field
        if self.title is None and "title" in self.model_fields_set:
            _dict['title'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if meta_keywords (nullable) is None
        # and model_fields_set contains the field
        if self.meta_keywords is None and "meta_keywords" in self.model_fields_set:
            _dict['meta_keywords'] = None

        # set to None if domain_rank (nullable) is None
        # and model_fields_set contains the field
        if self.domain_rank is None and "domain_rank" in self.model_fields_set:
            _dict['domain_rank'] = None

        # set to None if last_visited (nullable) is None
        # and model_fields_set contains the field
        if self.last_visited is None and "last_visited" in self.model_fields_set:
            _dict['last_visited'] = None

        # set to None if country_iso_code (nullable) is None
        # and model_fields_set contains the field
        if self.country_iso_code is None and "country_iso_code" in self.model_fields_set:
            _dict['country_iso_code'] = None

        # set to None if language_code (nullable) is None
        # and model_fields_set contains the field
        if self.language_code is None and "language_code" in self.model_fields_set:
            _dict['language_code'] = None

        # set to None if content_language_code (nullable) is None
        # and model_fields_set contains the field
        if self.content_language_code is None and "content_language_code" in self.model_fields_set:
            _dict['content_language_code'] = None

        # set to None if phone_numbers (nullable) is None
        # and model_fields_set contains the field
        if self.phone_numbers is None and "phone_numbers" in self.model_fields_set:
            _dict['phone_numbers'] = None

        # set to None if emails (nullable) is None
        # and model_fields_set contains the field
        if self.emails is None and "emails" in self.model_fields_set:
            _dict['emails'] = None

        # set to None if social_graph_urls (nullable) is None
        # and model_fields_set contains the field
        if self.social_graph_urls is None and "social_graph_urls" in self.model_fields_set:
            _dict['social_graph_urls'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DomainAnalyticsTechnologiesDomainsByLiveItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "domain": obj.get("domain"),
            "title": obj.get("title"),
            "description": obj.get("description"),
            "meta_keywords": obj.get("meta_keywords"),
            "domain_rank": obj.get("domain_rank"),
            "last_visited": obj.get("last_visited"),
            "country_iso_code": obj.get("country_iso_code"),
            "language_code": obj.get("language_code"),
            "content_language_code": obj.get("content_language_code"),
            "phone_numbers": obj.get("phone_numbers"),
            "emails": obj.get("emails"),
            "social_graph_urls": obj.get("social_graph_urls"),
            "technologies": TechnologiesInfo.from_dict(obj["technologies"]) if obj.get("technologies") is not None else None
        })
        return _obj


