# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.on_page_links_task_info import OnPageLinksTaskInfo

class TestOnPageLinksTaskInfo(unittest.TestCase):
    """OnPageLinksTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OnPageLinksTaskInfo:
        """Test OnPageLinksTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OnPageLinksTaskInfo`
        """
        model = OnPageLinksTaskInfo()
        if include_optional:
            return OnPageLinksTaskInfo(
                id = '',
                status_code = 56,
                status_message = '',
                time = '',
                cost = 1.337,
                result_count = 56,
                path = [
                    ''
                    ],
                data = dataforseo_client.models.data.data(),
                result = [
                    dataforseo_client.models.on_page_links_result_info.OnPageLinksResultInfo(
                        crawl_progress = '', 
                        crawl_status = dataforseo_client.models.crawl_status_info.CrawlStatusInfo(
                            max_crawl_pages = 56, 
                            pages_in_queue = 56, 
                            pages_crawled = 56, ), 
                        total_items_count = 56, 
                        items_count = 56, 
                        items = [
                            dataforseo_client.models.base_on_page_link_item_info.BaseOnPageLinkItemInfo()
                            ], )
                    ]
            )
        else:
            return OnPageLinksTaskInfo(
        )
        """

    def testOnPageLinksTaskInfo(self):
        """Test OnPageLinksTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
