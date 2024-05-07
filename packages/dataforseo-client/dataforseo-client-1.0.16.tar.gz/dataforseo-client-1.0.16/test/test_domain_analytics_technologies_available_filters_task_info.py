# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.domain_analytics_technologies_available_filters_task_info import DomainAnalyticsTechnologiesAvailableFiltersTaskInfo

class TestDomainAnalyticsTechnologiesAvailableFiltersTaskInfo(unittest.TestCase):
    """DomainAnalyticsTechnologiesAvailableFiltersTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DomainAnalyticsTechnologiesAvailableFiltersTaskInfo:
        """Test DomainAnalyticsTechnologiesAvailableFiltersTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DomainAnalyticsTechnologiesAvailableFiltersTaskInfo`
        """
        model = DomainAnalyticsTechnologiesAvailableFiltersTaskInfo()
        if include_optional:
            return DomainAnalyticsTechnologiesAvailableFiltersTaskInfo(
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
                    dataforseo_client.models.domain_analytics_technologies_available_filters_result_info.DomainAnalyticsTechnologiesAvailableFiltersResultInfo(
                        domains_by_technology = {
                            'key' : ''
                            }, 
                        aggregation_technologies = {
                            'key' : ''
                            }, 
                        technologies_summary = {
                            'key' : ''
                            }, 
                        domains_by_html_terms = {
                            'key' : ''
                            }, )
                    ]
            )
        else:
            return DomainAnalyticsTechnologiesAvailableFiltersTaskInfo(
        )
        """

    def testDomainAnalyticsTechnologiesAvailableFiltersTaskInfo(self):
        """Test DomainAnalyticsTechnologiesAvailableFiltersTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
