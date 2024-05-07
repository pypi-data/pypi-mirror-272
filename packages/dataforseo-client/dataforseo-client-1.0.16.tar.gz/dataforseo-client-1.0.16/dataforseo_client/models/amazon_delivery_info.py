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
from dataforseo_client.models.price_info import PriceInfo
from typing import Optional, Set
from typing_extensions import Self

class AmazonDeliveryInfo(BaseModel):
    """
    AmazonDeliveryInfo
    """ # noqa: E501
    delivery_message: Optional[StrictStr] = Field(default=None, description="message accompanying the delivery information as posted by the seller")
    delivery_date_from: Optional[StrictStr] = Field(default=None, description="the earliest date when the product can be shipped")
    delivery_date_to: Optional[StrictStr] = Field(default=None, description="the latest date when the product can be delivered")
    fastest_delivery_date_from: Optional[StrictStr] = Field(default=None, description="the earliest date when the product can be delivered with a fast delivery option")
    fastest_delivery_date_to: Optional[StrictStr] = Field(default=None, description="the latest date when the product can be delivered with a fast delivery option")
    delivery_price: Optional[PriceInfo] = None
    __properties: ClassVar[List[str]] = ["delivery_message", "delivery_date_from", "delivery_date_to", "fastest_delivery_date_from", "fastest_delivery_date_to", "delivery_price"]

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
        """Create an instance of AmazonDeliveryInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of delivery_price
        if self.delivery_price:
            _dict['delivery_price'] = self.delivery_price.to_dict()
        # set to None if delivery_message (nullable) is None
        # and model_fields_set contains the field
        if self.delivery_message is None and "delivery_message" in self.model_fields_set:
            _dict['delivery_message'] = None

        # set to None if delivery_date_from (nullable) is None
        # and model_fields_set contains the field
        if self.delivery_date_from is None and "delivery_date_from" in self.model_fields_set:
            _dict['delivery_date_from'] = None

        # set to None if delivery_date_to (nullable) is None
        # and model_fields_set contains the field
        if self.delivery_date_to is None and "delivery_date_to" in self.model_fields_set:
            _dict['delivery_date_to'] = None

        # set to None if fastest_delivery_date_from (nullable) is None
        # and model_fields_set contains the field
        if self.fastest_delivery_date_from is None and "fastest_delivery_date_from" in self.model_fields_set:
            _dict['fastest_delivery_date_from'] = None

        # set to None if fastest_delivery_date_to (nullable) is None
        # and model_fields_set contains the field
        if self.fastest_delivery_date_to is None and "fastest_delivery_date_to" in self.model_fields_set:
            _dict['fastest_delivery_date_to'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AmazonDeliveryInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "delivery_message": obj.get("delivery_message"),
            "delivery_date_from": obj.get("delivery_date_from"),
            "delivery_date_to": obj.get("delivery_date_to"),
            "fastest_delivery_date_from": obj.get("fastest_delivery_date_from"),
            "fastest_delivery_date_to": obj.get("fastest_delivery_date_to"),
            "delivery_price": PriceInfo.from_dict(obj["delivery_price"]) if obj.get("delivery_price") is not None else None
        })
        return _obj


