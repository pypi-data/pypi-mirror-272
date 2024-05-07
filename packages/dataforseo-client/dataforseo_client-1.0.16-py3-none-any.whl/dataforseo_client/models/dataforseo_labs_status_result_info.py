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

from pydantic import BaseModel
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.dataforseo_labs_status_info import DataforseoLabsStatusInfo
from typing import Optional, Set
from typing_extensions import Self

class DataforseoLabsStatusResultInfo(BaseModel):
    """
    DataforseoLabsStatusResultInfo
    """ # noqa: E501
    google: Optional[DataforseoLabsStatusInfo] = None
    bing: Optional[DataforseoLabsStatusInfo] = None
    amazon: Optional[DataforseoLabsStatusInfo] = None
    __properties: ClassVar[List[str]] = ["google", "bing", "amazon"]

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
        """Create an instance of DataforseoLabsStatusResultInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of google
        if self.google:
            _dict['google'] = self.google.to_dict()
        # override the default output from pydantic by calling `to_dict()` of bing
        if self.bing:
            _dict['bing'] = self.bing.to_dict()
        # override the default output from pydantic by calling `to_dict()` of amazon
        if self.amazon:
            _dict['amazon'] = self.amazon.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DataforseoLabsStatusResultInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "google": DataforseoLabsStatusInfo.from_dict(obj["google"]) if obj.get("google") is not None else None,
            "bing": DataforseoLabsStatusInfo.from_dict(obj["bing"]) if obj.get("bing") is not None else None,
            "amazon": DataforseoLabsStatusInfo.from_dict(obj["amazon"]) if obj.get("amazon") is not None else None
        })
        return _obj


