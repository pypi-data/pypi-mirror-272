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

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from dataforseo_client.models.ranked_keywords_info import RankedKeywordsInfo
from dataforseo_client.models.redirect import Redirect
from typing import Optional, Set
from typing_extensions import Self

class BacklinksBacklinksLiveItem(BaseModel):
    """
    BacklinksBacklinksLiveItem
    """ # noqa: E501
    type: Optional[StrictStr] = Field(default=None, description="type of element")
    domain_from: Optional[StrictStr] = Field(default=None, description="domain referring to the target domain or webpage")
    url_from: Optional[StrictStr] = Field(default=None, description="URL of the page where the backlink is found")
    url_from_https: Optional[StrictBool] = Field(default=None, description="indicates whether the referring URL is secured with HTTPS if true, the referring URL is secured with HTTPS")
    domain_to: Optional[StrictStr] = Field(default=None, description="domain the backlink is pointing to")
    url_to: Optional[StrictStr] = Field(default=None, description="URL the backlink is pointing to")
    url_to_https: Optional[StrictBool] = Field(default=None, description="indicates if the URL the backlink is pointing to is secured with HTTPS if true, the URL is secured with HTTPS")
    tld_from: Optional[StrictStr] = Field(default=None, description="top-level domain of the referring URL")
    is_new: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink is new if true, the backlink was found on the page last time our crawler visited it")
    is_lost: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink was removed if true, the backlink or the entire page was removed")
    backlink_spam_score: Optional[StrictInt] = Field(default=None, description="spam score of the backlink learn more about how the metric is calculated on this help center page")
    rank: Optional[StrictInt] = Field(default=None, description="backlink rank rank that the given backlink passes to the target rank is calculated based on the method for node ranking in a linked database – a principle used in the original Google PageRank algorithm learn more about the metric and how it is calculated in this help center article")
    page_from_rank: Optional[StrictInt] = Field(default=None, description="page rank of the referring page page_from_rank is calculated based on the method for node ranking in a linked database – a principle used in the original Google PageRank algorithm learn more about the metric and how it is calculated in this help center article")
    domain_from_rank: Optional[StrictInt] = Field(default=None, description="domain rank of the referring domain domain_from_rank is calculated based on the method for node ranking in a linked database – a principle used in the original Google PageRank algorithm learn more about the metric and how it is calculated in this help center article")
    domain_from_platform_type: Optional[List[Optional[StrictStr]]] = Field(default=None, description="platform types of the referring domain example: \"cms\", \"blogs\"")
    domain_from_is_ip: Optional[StrictBool] = Field(default=None, description="indicates if the domain is IP if true, the domain functions as an IP address and does not have a domain name")
    domain_from_ip: Optional[StrictStr] = Field(default=None, description="IP address of the referring domain")
    domain_from_country: Optional[StrictStr] = Field(default=None, description="ISO country code of the referring domain")
    page_from_external_links: Optional[StrictInt] = Field(default=None, description="number of external links found on the referring page")
    page_from_internal_links: Optional[StrictInt] = Field(default=None, description="number of internal links found on the referring page")
    page_from_size: Optional[StrictInt] = Field(default=None, description="size of the referring page, in bytes example: 63357")
    page_from_encoding: Optional[StrictStr] = Field(default=None, description="character encoding of the referring page example: utf-8")
    page_from_language: Optional[StrictStr] = Field(default=None, description="language of the referring page in ISO 639-1 format example: en")
    page_from_title: Optional[StrictStr] = Field(default=None, description="title of the referring page")
    page_from_status_code: Optional[StrictInt] = Field(default=None, description="HTTP status code returned by the referring page example: 200")
    first_seen: Optional[StrictStr] = Field(default=None, description="date and time when our crawler found the backlink for the first time in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2019-11-15 12:57:46 +00:00")
    prev_seen: Optional[StrictStr] = Field(default=None, description="previous to the most recent date when our crawler visited the backlink in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2019-11-15 12:57:46 +00:00")
    last_seen: Optional[StrictStr] = Field(default=None, description="most recent date when our crawler visited the backlink in the UTC format: “yyyy-mm-dd hh-mm-ss +00:00” example: 2019-11-15 12:57:46 +00:00")
    item_type: Optional[StrictStr] = Field(default=None, description="link type possible values: anchor, image, meta, canonical, alternate, redirect")
    attributes: Optional[List[Optional[StrictStr]]] = Field(default=None, description="link attributes of the referring links example: nofollow")
    dofollow: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink is dofollow if false, the backlink is nofollow")
    original: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink was present on the referring page when our crawler first visited it")
    alt: Optional[StrictStr] = Field(default=None, description="alternative text of the image this field will be null if backlink type is not image")
    image_url: Optional[StrictStr] = Field(default=None, description="URL of the image the URL leading to the image on the original resource or DataForSEO storage (in case the original source is not available)")
    anchor: Optional[StrictStr] = Field(default=None, description="anchor text of the backlink")
    text_pre: Optional[StrictStr] = Field(default=None, description="snippet before the anchor text")
    text_post: Optional[StrictStr] = Field(default=None, description="snippet after the anchor text")
    semantic_location: Optional[StrictStr] = Field(default=None, description="indicates semantic element in HTML where the backlink is found you can get the full list of semantic elements here examples: article, section, summary")
    links_count: Optional[StrictInt] = Field(default=None, description="number of identical backlinks found on the referring page")
    group_count: Optional[StrictInt] = Field(default=None, description="indicates total number of backlinks from this domain for example, if mode is set to one_per_domain, this field will indicate the total number of backlinks coming from this domain")
    is_broken: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink is broken if true, the backlink is pointing to a page responding with a 4xx or 5xx status code")
    url_to_status_code: Optional[StrictInt] = Field(default=None, description="status code of the referenced page if the value is null, our crawler hasn’t yet visited the webpage the link is pointing to example: 200")
    url_to_spam_score: Optional[StrictInt] = Field(default=None, description="spam score of the referenced page if the value is null, our crawler hasn’t yet visited the webpage the link is pointing to; learn more about how the metric is calculated on this help center page")
    url_to_redirect_target: Optional[StrictStr] = Field(default=None, description="target url of the redirect target page the redirect is pointing to")
    ranked_keywords_info: Optional[RankedKeywordsInfo] = None
    is_indirect_link: Optional[StrictBool] = Field(default=None, description="indicates whether the backlink is an indirect link if true, the backlink is an indirect link pointing to a page that either redirects to url_to, or points to a canonical page")
    indirect_link_path: Optional[List[Redirect]] = Field(default=None, description="indirect link path indicates a URL or a sequence of URLs that lead to url_to")
    __properties: ClassVar[List[str]] = ["type", "domain_from", "url_from", "url_from_https", "domain_to", "url_to", "url_to_https", "tld_from", "is_new", "is_lost", "backlink_spam_score", "rank", "page_from_rank", "domain_from_rank", "domain_from_platform_type", "domain_from_is_ip", "domain_from_ip", "domain_from_country", "page_from_external_links", "page_from_internal_links", "page_from_size", "page_from_encoding", "page_from_language", "page_from_title", "page_from_status_code", "first_seen", "prev_seen", "last_seen", "item_type", "attributes", "dofollow", "original", "alt", "image_url", "anchor", "text_pre", "text_post", "semantic_location", "links_count", "group_count", "is_broken", "url_to_status_code", "url_to_spam_score", "url_to_redirect_target", "ranked_keywords_info", "is_indirect_link", "indirect_link_path"]

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
        """Create an instance of BacklinksBacklinksLiveItem from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of ranked_keywords_info
        if self.ranked_keywords_info:
            _dict['ranked_keywords_info'] = self.ranked_keywords_info.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in indirect_link_path (list)
        _items = []
        if self.indirect_link_path:
            for _item in self.indirect_link_path:
                if _item:
                    _items.append(_item.to_dict())
            _dict['indirect_link_path'] = _items
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if domain_from (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from is None and "domain_from" in self.model_fields_set:
            _dict['domain_from'] = None

        # set to None if url_from (nullable) is None
        # and model_fields_set contains the field
        if self.url_from is None and "url_from" in self.model_fields_set:
            _dict['url_from'] = None

        # set to None if url_from_https (nullable) is None
        # and model_fields_set contains the field
        if self.url_from_https is None and "url_from_https" in self.model_fields_set:
            _dict['url_from_https'] = None

        # set to None if domain_to (nullable) is None
        # and model_fields_set contains the field
        if self.domain_to is None and "domain_to" in self.model_fields_set:
            _dict['domain_to'] = None

        # set to None if url_to (nullable) is None
        # and model_fields_set contains the field
        if self.url_to is None and "url_to" in self.model_fields_set:
            _dict['url_to'] = None

        # set to None if url_to_https (nullable) is None
        # and model_fields_set contains the field
        if self.url_to_https is None and "url_to_https" in self.model_fields_set:
            _dict['url_to_https'] = None

        # set to None if tld_from (nullable) is None
        # and model_fields_set contains the field
        if self.tld_from is None and "tld_from" in self.model_fields_set:
            _dict['tld_from'] = None

        # set to None if is_new (nullable) is None
        # and model_fields_set contains the field
        if self.is_new is None and "is_new" in self.model_fields_set:
            _dict['is_new'] = None

        # set to None if is_lost (nullable) is None
        # and model_fields_set contains the field
        if self.is_lost is None and "is_lost" in self.model_fields_set:
            _dict['is_lost'] = None

        # set to None if backlink_spam_score (nullable) is None
        # and model_fields_set contains the field
        if self.backlink_spam_score is None and "backlink_spam_score" in self.model_fields_set:
            _dict['backlink_spam_score'] = None

        # set to None if rank (nullable) is None
        # and model_fields_set contains the field
        if self.rank is None and "rank" in self.model_fields_set:
            _dict['rank'] = None

        # set to None if page_from_rank (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_rank is None and "page_from_rank" in self.model_fields_set:
            _dict['page_from_rank'] = None

        # set to None if domain_from_rank (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from_rank is None and "domain_from_rank" in self.model_fields_set:
            _dict['domain_from_rank'] = None

        # set to None if domain_from_platform_type (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from_platform_type is None and "domain_from_platform_type" in self.model_fields_set:
            _dict['domain_from_platform_type'] = None

        # set to None if domain_from_is_ip (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from_is_ip is None and "domain_from_is_ip" in self.model_fields_set:
            _dict['domain_from_is_ip'] = None

        # set to None if domain_from_ip (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from_ip is None and "domain_from_ip" in self.model_fields_set:
            _dict['domain_from_ip'] = None

        # set to None if domain_from_country (nullable) is None
        # and model_fields_set contains the field
        if self.domain_from_country is None and "domain_from_country" in self.model_fields_set:
            _dict['domain_from_country'] = None

        # set to None if page_from_external_links (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_external_links is None and "page_from_external_links" in self.model_fields_set:
            _dict['page_from_external_links'] = None

        # set to None if page_from_internal_links (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_internal_links is None and "page_from_internal_links" in self.model_fields_set:
            _dict['page_from_internal_links'] = None

        # set to None if page_from_size (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_size is None and "page_from_size" in self.model_fields_set:
            _dict['page_from_size'] = None

        # set to None if page_from_encoding (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_encoding is None and "page_from_encoding" in self.model_fields_set:
            _dict['page_from_encoding'] = None

        # set to None if page_from_language (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_language is None and "page_from_language" in self.model_fields_set:
            _dict['page_from_language'] = None

        # set to None if page_from_title (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_title is None and "page_from_title" in self.model_fields_set:
            _dict['page_from_title'] = None

        # set to None if page_from_status_code (nullable) is None
        # and model_fields_set contains the field
        if self.page_from_status_code is None and "page_from_status_code" in self.model_fields_set:
            _dict['page_from_status_code'] = None

        # set to None if first_seen (nullable) is None
        # and model_fields_set contains the field
        if self.first_seen is None and "first_seen" in self.model_fields_set:
            _dict['first_seen'] = None

        # set to None if prev_seen (nullable) is None
        # and model_fields_set contains the field
        if self.prev_seen is None and "prev_seen" in self.model_fields_set:
            _dict['prev_seen'] = None

        # set to None if last_seen (nullable) is None
        # and model_fields_set contains the field
        if self.last_seen is None and "last_seen" in self.model_fields_set:
            _dict['last_seen'] = None

        # set to None if item_type (nullable) is None
        # and model_fields_set contains the field
        if self.item_type is None and "item_type" in self.model_fields_set:
            _dict['item_type'] = None

        # set to None if attributes (nullable) is None
        # and model_fields_set contains the field
        if self.attributes is None and "attributes" in self.model_fields_set:
            _dict['attributes'] = None

        # set to None if dofollow (nullable) is None
        # and model_fields_set contains the field
        if self.dofollow is None and "dofollow" in self.model_fields_set:
            _dict['dofollow'] = None

        # set to None if original (nullable) is None
        # and model_fields_set contains the field
        if self.original is None and "original" in self.model_fields_set:
            _dict['original'] = None

        # set to None if alt (nullable) is None
        # and model_fields_set contains the field
        if self.alt is None and "alt" in self.model_fields_set:
            _dict['alt'] = None

        # set to None if image_url (nullable) is None
        # and model_fields_set contains the field
        if self.image_url is None and "image_url" in self.model_fields_set:
            _dict['image_url'] = None

        # set to None if anchor (nullable) is None
        # and model_fields_set contains the field
        if self.anchor is None and "anchor" in self.model_fields_set:
            _dict['anchor'] = None

        # set to None if text_pre (nullable) is None
        # and model_fields_set contains the field
        if self.text_pre is None and "text_pre" in self.model_fields_set:
            _dict['text_pre'] = None

        # set to None if text_post (nullable) is None
        # and model_fields_set contains the field
        if self.text_post is None and "text_post" in self.model_fields_set:
            _dict['text_post'] = None

        # set to None if semantic_location (nullable) is None
        # and model_fields_set contains the field
        if self.semantic_location is None and "semantic_location" in self.model_fields_set:
            _dict['semantic_location'] = None

        # set to None if links_count (nullable) is None
        # and model_fields_set contains the field
        if self.links_count is None and "links_count" in self.model_fields_set:
            _dict['links_count'] = None

        # set to None if group_count (nullable) is None
        # and model_fields_set contains the field
        if self.group_count is None and "group_count" in self.model_fields_set:
            _dict['group_count'] = None

        # set to None if is_broken (nullable) is None
        # and model_fields_set contains the field
        if self.is_broken is None and "is_broken" in self.model_fields_set:
            _dict['is_broken'] = None

        # set to None if url_to_status_code (nullable) is None
        # and model_fields_set contains the field
        if self.url_to_status_code is None and "url_to_status_code" in self.model_fields_set:
            _dict['url_to_status_code'] = None

        # set to None if url_to_spam_score (nullable) is None
        # and model_fields_set contains the field
        if self.url_to_spam_score is None and "url_to_spam_score" in self.model_fields_set:
            _dict['url_to_spam_score'] = None

        # set to None if url_to_redirect_target (nullable) is None
        # and model_fields_set contains the field
        if self.url_to_redirect_target is None and "url_to_redirect_target" in self.model_fields_set:
            _dict['url_to_redirect_target'] = None

        # set to None if is_indirect_link (nullable) is None
        # and model_fields_set contains the field
        if self.is_indirect_link is None and "is_indirect_link" in self.model_fields_set:
            _dict['is_indirect_link'] = None

        # set to None if indirect_link_path (nullable) is None
        # and model_fields_set contains the field
        if self.indirect_link_path is None and "indirect_link_path" in self.model_fields_set:
            _dict['indirect_link_path'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BacklinksBacklinksLiveItem from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "domain_from": obj.get("domain_from"),
            "url_from": obj.get("url_from"),
            "url_from_https": obj.get("url_from_https"),
            "domain_to": obj.get("domain_to"),
            "url_to": obj.get("url_to"),
            "url_to_https": obj.get("url_to_https"),
            "tld_from": obj.get("tld_from"),
            "is_new": obj.get("is_new"),
            "is_lost": obj.get("is_lost"),
            "backlink_spam_score": obj.get("backlink_spam_score"),
            "rank": obj.get("rank"),
            "page_from_rank": obj.get("page_from_rank"),
            "domain_from_rank": obj.get("domain_from_rank"),
            "domain_from_platform_type": obj.get("domain_from_platform_type"),
            "domain_from_is_ip": obj.get("domain_from_is_ip"),
            "domain_from_ip": obj.get("domain_from_ip"),
            "domain_from_country": obj.get("domain_from_country"),
            "page_from_external_links": obj.get("page_from_external_links"),
            "page_from_internal_links": obj.get("page_from_internal_links"),
            "page_from_size": obj.get("page_from_size"),
            "page_from_encoding": obj.get("page_from_encoding"),
            "page_from_language": obj.get("page_from_language"),
            "page_from_title": obj.get("page_from_title"),
            "page_from_status_code": obj.get("page_from_status_code"),
            "first_seen": obj.get("first_seen"),
            "prev_seen": obj.get("prev_seen"),
            "last_seen": obj.get("last_seen"),
            "item_type": obj.get("item_type"),
            "attributes": obj.get("attributes"),
            "dofollow": obj.get("dofollow"),
            "original": obj.get("original"),
            "alt": obj.get("alt"),
            "image_url": obj.get("image_url"),
            "anchor": obj.get("anchor"),
            "text_pre": obj.get("text_pre"),
            "text_post": obj.get("text_post"),
            "semantic_location": obj.get("semantic_location"),
            "links_count": obj.get("links_count"),
            "group_count": obj.get("group_count"),
            "is_broken": obj.get("is_broken"),
            "url_to_status_code": obj.get("url_to_status_code"),
            "url_to_spam_score": obj.get("url_to_spam_score"),
            "url_to_redirect_target": obj.get("url_to_redirect_target"),
            "ranked_keywords_info": RankedKeywordsInfo.from_dict(obj["ranked_keywords_info"]) if obj.get("ranked_keywords_info") is not None else None,
            "is_indirect_link": obj.get("is_indirect_link"),
            "indirect_link_path": [Redirect.from_dict(_item) for _item in obj["indirect_link_path"]] if obj.get("indirect_link_path") is not None else None
        })
        return _obj


