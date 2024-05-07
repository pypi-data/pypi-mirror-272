# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.featured_snippet_dataforseo_labs_serp_element_item import FeaturedSnippetDataforseoLabsSerpElementItem

class TestFeaturedSnippetDataforseoLabsSerpElementItem(unittest.TestCase):
    """FeaturedSnippetDataforseoLabsSerpElementItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FeaturedSnippetDataforseoLabsSerpElementItem:
        """Test FeaturedSnippetDataforseoLabsSerpElementItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FeaturedSnippetDataforseoLabsSerpElementItem`
        """
        model = FeaturedSnippetDataforseoLabsSerpElementItem()
        if include_optional:
            return FeaturedSnippetDataforseoLabsSerpElementItem(
                rank_group = 56,
                rank_absolute = 56,
                position = '',
                xpath = '',
                domain = '',
                title = '',
                featured_title = '',
                description = '',
                url = '',
                table = dataforseo_client.models.table.Table(
                    table_element = '', 
                    table_header = [
                        ''
                        ], 
                    table_content = [
                        [
                            ''
                            ]
                        ], ),
                se_type = '',
                main_domain = '',
                relative_url = '',
                etv = 1.337,
                estimated_paid_traffic_cost = 1.337,
                rank_changes = dataforseo_client.models.rank_changes.RankChanges(
                    previous_rank_absolute = 56, 
                    is_new = True, 
                    is_up = True, 
                    is_down = True, ),
                backlinks_info = dataforseo_client.models.backlinks_info.BacklinksInfo(
                    referring_domains = 56, 
                    referring_main_domains = 56, 
                    referring_pages = 56, 
                    dofollow = 56, 
                    backlinks = 56, 
                    time_update = '', ),
                rank_info = dataforseo_client.models.rank_info.RankInfo(
                    page_rank = 56, 
                    main_domain_rank = 56, )
            )
        else:
            return FeaturedSnippetDataforseoLabsSerpElementItem(
        )
        """

    def testFeaturedSnippetDataforseoLabsSerpElementItem(self):
        """Test FeaturedSnippetDataforseoLabsSerpElementItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
