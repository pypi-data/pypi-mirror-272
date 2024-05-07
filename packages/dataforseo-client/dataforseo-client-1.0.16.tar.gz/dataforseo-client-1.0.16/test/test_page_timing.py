# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.page_timing import PageTiming

class TestPageTiming(unittest.TestCase):
    """PageTiming unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PageTiming:
        """Test PageTiming
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PageTiming`
        """
        model = PageTiming()
        if include_optional:
            return PageTiming(
                time_to_interactive = 56,
                dom_complete = 56,
                largest_contentful_paint = 1.337,
                first_input_delay = 1.337,
                connection_time = 56,
                time_to_secure_connection = 56,
                request_sent_time = 56,
                waiting_time = 56,
                download_time = 56,
                duration_time = 56,
                fetch_start = 56,
                fetch_end = 56
            )
        else:
            return PageTiming(
        )
        """

    def testPageTiming(self):
        """Test PageTiming"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
