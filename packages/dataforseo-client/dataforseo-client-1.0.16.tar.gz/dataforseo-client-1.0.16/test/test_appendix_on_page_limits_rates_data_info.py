# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.appendix_on_page_limits_rates_data_info import AppendixOnPageLimitsRatesDataInfo

class TestAppendixOnPageLimitsRatesDataInfo(unittest.TestCase):
    """AppendixOnPageLimitsRatesDataInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppendixOnPageLimitsRatesDataInfo:
        """Test AppendixOnPageLimitsRatesDataInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppendixOnPageLimitsRatesDataInfo`
        """
        model = AppendixOnPageLimitsRatesDataInfo()
        if include_optional:
            return AppendixOnPageLimitsRatesDataInfo(
                task_post = 1.337,
                tasks_ready = 1.337,
                summary = 1.337,
                resources = 1.337,
                pages = 1.337,
                non_indexable = 1.337,
                duplicate_tags = 1.337,
                links = 1.337,
                waterfall = 1.337,
                errors = 1.337,
                pages_by_resource = 1.337,
                duplicate_content = 1.337,
                raw_html = 1.337,
                instant_pages = 1.337,
                redirect_chains = 1.337,
                lighthouse = dataforseo_client.models.appendix_function_info.AppendixFunctionInfo(
                    task_post = 1.337, 
                    task_get = 1.337, 
                    tasks_ready = 1.337, 
                    live = 1.337, ),
                keyword_density = 1.337,
                page_screenshot = 1.337,
                content_parsing = 1.337,
                content_parsing_live = 1.337
            )
        else:
            return AppendixOnPageLimitsRatesDataInfo(
        )
        """

    def testAppendixOnPageLimitsRatesDataInfo(self):
        """Test AppendixOnPageLimitsRatesDataInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
