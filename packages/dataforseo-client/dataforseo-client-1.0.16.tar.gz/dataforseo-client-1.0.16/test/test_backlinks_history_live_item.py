# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.backlinks_history_live_item import BacklinksHistoryLiveItem

class TestBacklinksHistoryLiveItem(unittest.TestCase):
    """BacklinksHistoryLiveItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BacklinksHistoryLiveItem:
        """Test BacklinksHistoryLiveItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BacklinksHistoryLiveItem`
        """
        model = BacklinksHistoryLiveItem()
        if include_optional:
            return BacklinksHistoryLiveItem(
                type = '',
                var_date = '',
                rank = 56,
                backlinks = 56,
                new_backlinks = 56,
                lost_backlinks = 56,
                new_referring_domains = 56,
                lost_referring_domains = 56,
                crawled_pages = 56,
                info = dataforseo_client.models.target_info.TargetInfo(
                    server = '', 
                    cms = '', 
                    platform_type = [
                        ''
                        ], 
                    ip_address = '', 
                    country = '', 
                    is_ip = True, 
                    target_spam_score = 56, ),
                internal_links_count = 56,
                external_links_count = 56,
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
            return BacklinksHistoryLiveItem(
        )
        """

    def testBacklinksHistoryLiveItem(self):
        """Test BacklinksHistoryLiveItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
