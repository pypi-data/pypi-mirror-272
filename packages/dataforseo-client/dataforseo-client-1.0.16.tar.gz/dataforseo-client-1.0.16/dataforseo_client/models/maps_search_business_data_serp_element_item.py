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

from pydantic import Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from dataforseo_client.models.address_info import AddressInfo
from dataforseo_client.models.base_business_data_serp_element_item import BaseBusinessDataSerpElementItem
from dataforseo_client.models.rating_info import RatingInfo
from dataforseo_client.models.work_info import WorkInfo
from typing import Optional, Set
from typing_extensions import Self

class MapsSearchBusinessDataSerpElementItem(BaseBusinessDataSerpElementItem):
    """
    MapsSearchBusinessDataSerpElementItem
    """ # noqa: E501
    rank_group: Optional[StrictInt] = Field(default=None, description="position within a group of elements with identical type values positions of elements with different type values are omitted from the rank_group")
    rank_absolute: Optional[StrictInt] = Field(default=None, description="absolute rank among all the elements")
    domain: Optional[StrictStr] = Field(default=None, description="domain of the business entity")
    title: Optional[StrictStr] = Field(default=None, description="directory title can take the following values: At this place, Directory")
    url: Optional[StrictStr] = Field(default=None, description="URL to view the menu")
    rating: Optional[RatingInfo] = None
    rating_distribution: Optional[Dict[str, Optional[StrictInt]]] = Field(default=None, description="the distribution of ratings of the business entity the object displays the number of 1-star to 5-star ratings, as reviewed by users")
    snippet: Optional[StrictStr] = Field(default=None, description="additional information about the business entity")
    address: Optional[StrictStr] = Field(default=None, description="address of the business entity")
    address_info: Optional[AddressInfo] = None
    place_id: Optional[StrictStr] = Field(default=None, description="unique place identifier place id of the local establishment featured in the element learn more about the identifier in this help center article")
    phone: Optional[StrictStr] = Field(default=None, description="phone number of the business entity")
    main_image: Optional[StrictStr] = Field(default=None, description="URL of the main image featured in Google My Business profile")
    total_photos: Optional[StrictInt] = Field(default=None, description="total count of images featured in Google My Business profile")
    category: Optional[StrictStr] = Field(default=None, description="business category Google My Business general category that best describes the services provided by the business entity")
    additional_categories: Optional[List[StrictStr]] = Field(default=None, description="additional business categories additional Google My Business categories that describe the services provided by the business entity in more detail")
    price_level: Optional[StrictStr] = Field(default=None, description="property price level can take values: inexpensive, moderate, expensive, very_expensive if there is no price level information, the value will be null")
    hotel_rating: Optional[StrictInt] = Field(default=None, description="hotel class rating class ratings range between 1-5 stars, learn more if there is no hotel class rating information, the value will be null")
    category_ids: Optional[List[StrictStr]] = Field(default=None, description="global category IDs universal category IDs that do not change based on the selected country")
    work_hours: Optional[WorkInfo] = None
    feature_id: Optional[StrictStr] = Field(default=None, description="the unique identifier of the element in SERP learn more about the identifier in this help center article")
    cid: Optional[StrictStr] = Field(default=None, description="google-defined client id unique id of a local establishment; can be used with Google Reviews API to get a full list of reviews learn more about the identifier in this help center article")
    latitude: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="latitude coordinate of the local establishments in google maps example: \"latitude\": 51.584091")
    longitude: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="longitude coordinate of the local establishment in google maps example: \"longitude\": -0.31365919999999997")
    is_claimed: Optional[StrictBool] = Field(default=None, description="shows whether the entity is verified by its owner on Google Maps")
    local_justifications: Optional[List[StrictStr]] = Field(default=None, description="Google local justifications snippets of text that “justify” why the business is showing up for search query")
    is_directory_item: Optional[StrictBool] = Field(default=None, description="business establishment is a part of the directory indicates whether the business establishment is a part of the directory; if true, the item is a part of the larger directory of businesses with the same address (e.g., a mall or a business centre); note: if the business establishment is a parent item in the directory, the value will be null")
    __properties: ClassVar[List[str]] = ["type", "rank_group", "rank_absolute", "domain", "title", "url", "rating", "rating_distribution", "snippet", "address", "address_info", "place_id", "phone", "main_image", "total_photos", "category", "additional_categories", "price_level", "hotel_rating", "category_ids", "work_hours", "feature_id", "cid", "latitude", "longitude", "is_claimed", "local_justifications", "is_directory_item"]

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
        """Create an instance of MapsSearchBusinessDataSerpElementItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of rating
        if self.rating:
            _dict['rating'] = self.rating.to_dict()
        # override the default output from pydantic by calling `to_dict()` of address_info
        if self.address_info:
            _dict['address_info'] = self.address_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of work_hours
        if self.work_hours:
            _dict['work_hours'] = self.work_hours.to_dict()
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if rank_group (nullable) is None
        # and model_fields_set contains the field
        if self.rank_group is None and "rank_group" in self.model_fields_set:
            _dict['rank_group'] = None

        # set to None if rank_absolute (nullable) is None
        # and model_fields_set contains the field
        if self.rank_absolute is None and "rank_absolute" in self.model_fields_set:
            _dict['rank_absolute'] = None

        # set to None if domain (nullable) is None
        # and model_fields_set contains the field
        if self.domain is None and "domain" in self.model_fields_set:
            _dict['domain'] = None

        # set to None if title (nullable) is None
        # and model_fields_set contains the field
        if self.title is None and "title" in self.model_fields_set:
            _dict['title'] = None

        # set to None if url (nullable) is None
        # and model_fields_set contains the field
        if self.url is None and "url" in self.model_fields_set:
            _dict['url'] = None

        # set to None if rating_distribution (nullable) is None
        # and model_fields_set contains the field
        if self.rating_distribution is None and "rating_distribution" in self.model_fields_set:
            _dict['rating_distribution'] = None

        # set to None if snippet (nullable) is None
        # and model_fields_set contains the field
        if self.snippet is None and "snippet" in self.model_fields_set:
            _dict['snippet'] = None

        # set to None if address (nullable) is None
        # and model_fields_set contains the field
        if self.address is None and "address" in self.model_fields_set:
            _dict['address'] = None

        # set to None if place_id (nullable) is None
        # and model_fields_set contains the field
        if self.place_id is None and "place_id" in self.model_fields_set:
            _dict['place_id'] = None

        # set to None if phone (nullable) is None
        # and model_fields_set contains the field
        if self.phone is None and "phone" in self.model_fields_set:
            _dict['phone'] = None

        # set to None if main_image (nullable) is None
        # and model_fields_set contains the field
        if self.main_image is None and "main_image" in self.model_fields_set:
            _dict['main_image'] = None

        # set to None if total_photos (nullable) is None
        # and model_fields_set contains the field
        if self.total_photos is None and "total_photos" in self.model_fields_set:
            _dict['total_photos'] = None

        # set to None if category (nullable) is None
        # and model_fields_set contains the field
        if self.category is None and "category" in self.model_fields_set:
            _dict['category'] = None

        # set to None if additional_categories (nullable) is None
        # and model_fields_set contains the field
        if self.additional_categories is None and "additional_categories" in self.model_fields_set:
            _dict['additional_categories'] = None

        # set to None if price_level (nullable) is None
        # and model_fields_set contains the field
        if self.price_level is None and "price_level" in self.model_fields_set:
            _dict['price_level'] = None

        # set to None if hotel_rating (nullable) is None
        # and model_fields_set contains the field
        if self.hotel_rating is None and "hotel_rating" in self.model_fields_set:
            _dict['hotel_rating'] = None

        # set to None if category_ids (nullable) is None
        # and model_fields_set contains the field
        if self.category_ids is None and "category_ids" in self.model_fields_set:
            _dict['category_ids'] = None

        # set to None if feature_id (nullable) is None
        # and model_fields_set contains the field
        if self.feature_id is None and "feature_id" in self.model_fields_set:
            _dict['feature_id'] = None

        # set to None if cid (nullable) is None
        # and model_fields_set contains the field
        if self.cid is None and "cid" in self.model_fields_set:
            _dict['cid'] = None

        # set to None if latitude (nullable) is None
        # and model_fields_set contains the field
        if self.latitude is None and "latitude" in self.model_fields_set:
            _dict['latitude'] = None

        # set to None if longitude (nullable) is None
        # and model_fields_set contains the field
        if self.longitude is None and "longitude" in self.model_fields_set:
            _dict['longitude'] = None

        # set to None if is_claimed (nullable) is None
        # and model_fields_set contains the field
        if self.is_claimed is None and "is_claimed" in self.model_fields_set:
            _dict['is_claimed'] = None

        # set to None if local_justifications (nullable) is None
        # and model_fields_set contains the field
        if self.local_justifications is None and "local_justifications" in self.model_fields_set:
            _dict['local_justifications'] = None

        # set to None if is_directory_item (nullable) is None
        # and model_fields_set contains the field
        if self.is_directory_item is None and "is_directory_item" in self.model_fields_set:
            _dict['is_directory_item'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MapsSearchBusinessDataSerpElementItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "rank_group": obj.get("rank_group"),
            "rank_absolute": obj.get("rank_absolute"),
            "domain": obj.get("domain"),
            "title": obj.get("title"),
            "url": obj.get("url"),
            "rating": RatingInfo.from_dict(obj["rating"]) if obj.get("rating") is not None else None,
            "rating_distribution": obj.get("rating_distribution"),
            "snippet": obj.get("snippet"),
            "address": obj.get("address"),
            "address_info": AddressInfo.from_dict(obj["address_info"]) if obj.get("address_info") is not None else None,
            "place_id": obj.get("place_id"),
            "phone": obj.get("phone"),
            "main_image": obj.get("main_image"),
            "total_photos": obj.get("total_photos"),
            "category": obj.get("category"),
            "additional_categories": obj.get("additional_categories"),
            "price_level": obj.get("price_level"),
            "hotel_rating": obj.get("hotel_rating"),
            "category_ids": obj.get("category_ids"),
            "work_hours": WorkInfo.from_dict(obj["work_hours"]) if obj.get("work_hours") is not None else None,
            "feature_id": obj.get("feature_id"),
            "cid": obj.get("cid"),
            "latitude": obj.get("latitude"),
            "longitude": obj.get("longitude"),
            "is_claimed": obj.get("is_claimed"),
            "local_justifications": obj.get("local_justifications"),
            "is_directory_item": obj.get("is_directory_item")
        })
        return _obj


