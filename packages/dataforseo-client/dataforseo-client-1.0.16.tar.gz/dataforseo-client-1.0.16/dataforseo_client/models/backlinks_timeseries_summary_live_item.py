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

class BacklinksTimeseriesSummaryLiveItem(BaseModel):
    """
    BacklinksTimeseriesSummaryLiveItem
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    var_date: Optional[StrictStr] = Field(default=None, description="date and time when the data for the target was stored in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2019-11-15 12:57:46 +00:00", alias="date")
    rank: Optional[StrictInt] = Field(default=None, description="target rank for the given date learn more about the metric and how it is calculated in this help center article")
    backlinks: Optional[StrictInt] = Field(default=None, description="number of backlinks for the given date")
    backlinks_nofollow: Optional[StrictInt] = Field(default=None, description="number of nofollow backlinks for the given date")
    referring_pages: Optional[StrictInt] = Field(default=None, description="number of pages pointing to target for the given date")
    referring_pages_nofollow: Optional[StrictInt] = Field(default=None, description="number of referring pages pointing at least one nofollow link to the target for the given date")
    referring_domains: Optional[StrictInt] = Field(default=None, description="number of referring domains for the given date referring domains include subdomains that are counted as separate domains for this metric")
    referring_domains_nofollow: Optional[StrictInt] = Field(default=None, description="number of domains pointing at least one nofollow link to the target for the given date")
    referring_main_domains: Optional[StrictInt] = Field(default=None, description="number of referring main domains for the given date")
    referring_main_domains_nofollow: Optional[StrictInt] = Field(default=None, description="number of main domains pointing at least one nofollow link to the target for the given date")
    referring_ips: Optional[StrictInt] = Field(default=None, description="number of referring IP addresses for the given date number of IP addresses pointing to this page")
    referring_subnets: Optional[StrictInt] = Field(default=None, description="number of referring subnetworks for the given date")
    __properties: ClassVar[List[str]] = ["type", "date", "rank", "backlinks", "backlinks_nofollow", "referring_pages", "referring_pages_nofollow", "referring_domains", "referring_domains_nofollow", "referring_main_domains", "referring_main_domains_nofollow", "referring_ips", "referring_subnets"]

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
        """Create an instance of BacklinksTimeseriesSummaryLiveItem from a JSON string"""
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

        # set to None if var_date (nullable) is None
        # and model_fields_set contains the field
        if self.var_date is None and "var_date" in self.model_fields_set:
            _dict['date'] = None

        # set to None if rank (nullable) is None
        # and model_fields_set contains the field
        if self.rank is None and "rank" in self.model_fields_set:
            _dict['rank'] = None

        # set to None if backlinks (nullable) is None
        # and model_fields_set contains the field
        if self.backlinks is None and "backlinks" in self.model_fields_set:
            _dict['backlinks'] = None

        # set to None if backlinks_nofollow (nullable) is None
        # and model_fields_set contains the field
        if self.backlinks_nofollow is None and "backlinks_nofollow" in self.model_fields_set:
            _dict['backlinks_nofollow'] = None

        # set to None if referring_pages (nullable) is None
        # and model_fields_set contains the field
        if self.referring_pages is None and "referring_pages" in self.model_fields_set:
            _dict['referring_pages'] = None

        # set to None if referring_pages_nofollow (nullable) is None
        # and model_fields_set contains the field
        if self.referring_pages_nofollow is None and "referring_pages_nofollow" in self.model_fields_set:
            _dict['referring_pages_nofollow'] = None

        # set to None if referring_domains (nullable) is None
        # and model_fields_set contains the field
        if self.referring_domains is None and "referring_domains" in self.model_fields_set:
            _dict['referring_domains'] = None

        # set to None if referring_domains_nofollow (nullable) is None
        # and model_fields_set contains the field
        if self.referring_domains_nofollow is None and "referring_domains_nofollow" in self.model_fields_set:
            _dict['referring_domains_nofollow'] = None

        # set to None if referring_main_domains (nullable) is None
        # and model_fields_set contains the field
        if self.referring_main_domains is None and "referring_main_domains" in self.model_fields_set:
            _dict['referring_main_domains'] = None

        # set to None if referring_main_domains_nofollow (nullable) is None
        # and model_fields_set contains the field
        if self.referring_main_domains_nofollow is None and "referring_main_domains_nofollow" in self.model_fields_set:
            _dict['referring_main_domains_nofollow'] = None

        # set to None if referring_ips (nullable) is None
        # and model_fields_set contains the field
        if self.referring_ips is None and "referring_ips" in self.model_fields_set:
            _dict['referring_ips'] = None

        # set to None if referring_subnets (nullable) is None
        # and model_fields_set contains the field
        if self.referring_subnets is None and "referring_subnets" in self.model_fields_set:
            _dict['referring_subnets'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BacklinksTimeseriesSummaryLiveItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "date": obj.get("date"),
            "rank": obj.get("rank"),
            "backlinks": obj.get("backlinks"),
            "backlinks_nofollow": obj.get("backlinks_nofollow"),
            "referring_pages": obj.get("referring_pages"),
            "referring_pages_nofollow": obj.get("referring_pages_nofollow"),
            "referring_domains": obj.get("referring_domains"),
            "referring_domains_nofollow": obj.get("referring_domains_nofollow"),
            "referring_main_domains": obj.get("referring_main_domains"),
            "referring_main_domains_nofollow": obj.get("referring_main_domains_nofollow"),
            "referring_ips": obj.get("referring_ips"),
            "referring_subnets": obj.get("referring_subnets")
        })
        return _obj


