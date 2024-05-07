# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.backlinks_anchors_live_item import BacklinksAnchorsLiveItem

class TestBacklinksAnchorsLiveItem(unittest.TestCase):
    """BacklinksAnchorsLiveItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BacklinksAnchorsLiveItem:
        """Test BacklinksAnchorsLiveItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BacklinksAnchorsLiveItem`
        """
        model = BacklinksAnchorsLiveItem()
        if include_optional:
            return BacklinksAnchorsLiveItem(
                type = '',
                anchor = '',
                rank = 56,
                backlinks = 56,
                first_seen = '',
                lost_date = '',
                backlinks_spam_score = 56,
                broken_backlinks = 56,
                broken_pages = 56,
                referring_domains = 56,
                referring_domains_nofollow = 56,
                referring_main_domains = 56,
                referring_main_domains_nofollow = 56,
                referring_ips = 56,
                referring_subnets = 56,
                referring_pages = 56,
                referring_pages_nofollow = 56,
                referring_links_tld = {
                    'key' : 56
                    },
                referring_links_types = {
                    'key' : 56
                    },
                referring_links_attributes = {
                    'key' : 56
                    },
                referring_links_platform_types = {
                    'key' : 56
                    },
                referring_links_semantic_locations = {
                    'key' : 56
                    },
                referring_links_countries = {
                    'key' : 56
                    }
            )
        else:
            return BacklinksAnchorsLiveItem(
        )
        """

    def testBacklinksAnchorsLiveItem(self):
        """Test BacklinksAnchorsLiveItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
