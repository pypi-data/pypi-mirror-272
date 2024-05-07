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
from typing import Optional, Set
from typing_extensions import Self

class BacklinksBulkNewLostReferringDomainsLiveRequestInfo(BaseModel):
    """
    BacklinksBulkNewLostReferringDomainsLiveRequestInfo
    """ # noqa: E501
    targets: Optional[List[StrictStr]] = Field(default=None, description="domains, subdomains or webpages to get  new & lost referring domains for required field you can set up to 1000 domains, subdomains or webpages the domain or subdomain should be specified without https:// and www. the page should be specified with absolute URL (including http:// or https://) example: \"targets\": [   \"forbes.com\",   \"cnn.com\",   \"bbc.com\",   \"yelp.com\",   \"https://www.apple.com/iphone/\",   \"https://ahrefs.com/blog/\",   \"ibm.com\",   \"https://variety.com/\",   \"https://stackoverflow.com/\",   \"www.trustpilot.com\" ]")
    date_from: Optional[StrictStr] = Field(default=None, description="starting date of the time range optional field this field indicates the date which will be used as a threshold for new and lost referring domains; the referring domains that appeared in our index after the specified date will be considered as new; the referring domains that weren’t found after the specified date, but were present before, will be considered as lost; default value: today’s date -(minus) one month; e.g. if today is 2021-10-13, default date_from will be 2021-09-13. minimum value equals today’s date -(minus) one year; e.g. if today is 2021-10-13, minimum date_from will be 2020-10-13. date format: \"yyyy-mm-dd\" example: \"2021-01-01\"")
    tag: Optional[StrictStr] = Field(default=None, description="user-defined task identifier optional field the character limit is 255 you can use this parameter to identify the task and match it with the result you will find the specified tag value in the data object of the response")
    __properties: ClassVar[List[str]] = ["targets", "date_from", "tag"]

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
        """Create an instance of BacklinksBulkNewLostReferringDomainsLiveRequestInfo from a JSON string"""
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
        # set to None if date_from (nullable) is None
        # and model_fields_set contains the field
        if self.date_from is None and "date_from" in self.model_fields_set:
            _dict['date_from'] = None

        # set to None if tag (nullable) is None
        # and model_fields_set contains the field
        if self.tag is None and "tag" in self.model_fields_set:
            _dict['tag'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BacklinksBulkNewLostReferringDomainsLiveRequestInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "targets": obj.get("targets"),
            "date_from": obj.get("date_from"),
            "tag": obj.get("tag")
        })
        return _obj


