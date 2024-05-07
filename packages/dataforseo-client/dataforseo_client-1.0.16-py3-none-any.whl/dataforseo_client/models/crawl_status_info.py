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

class CrawlStatusInfo(BaseModel):
    """
    CrawlStatusInfo
    """ # noqa: E501
    max_crawl_pages: Optional[StrictInt] = Field(default=None, description="maximum number of pages to crawl  indicates the max_crawl_pages limit you specified when setting a task")
    pages_in_queue: Optional[StrictInt] = Field(default=None, description="number of pages that are currently in the crawling queue")
    pages_crawled: Optional[StrictInt] = Field(default=None, description="number of crawled pages")
    __properties: ClassVar[List[str]] = ["max_crawl_pages", "pages_in_queue", "pages_crawled"]

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
        """Create an instance of CrawlStatusInfo from a JSON string"""
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
        # set to None if max_crawl_pages (nullable) is None
        # and model_fields_set contains the field
        if self.max_crawl_pages is None and "max_crawl_pages" in self.model_fields_set:
            _dict['max_crawl_pages'] = None

        # set to None if pages_in_queue (nullable) is None
        # and model_fields_set contains the field
        if self.pages_in_queue is None and "pages_in_queue" in self.model_fields_set:
            _dict['pages_in_queue'] = None

        # set to None if pages_crawled (nullable) is None
        # and model_fields_set contains the field
        if self.pages_crawled is None and "pages_crawled" in self.model_fields_set:
            _dict['pages_crawled'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CrawlStatusInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "max_crawl_pages": obj.get("max_crawl_pages"),
            "pages_in_queue": obj.get("pages_in_queue"),
            "pages_crawled": obj.get("pages_crawled")
        })
        return _obj


