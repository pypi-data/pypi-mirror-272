# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.dataforseo_labs_google_historical_serps_live_response_info import DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo

class TestDataforseoLabsGoogleHistoricalSerpsLiveResponseInfo(unittest.TestCase):
    """DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo:
        """Test DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo`
        """
        model = DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo()
        if include_optional:
            return DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo(
                version = '',
                status_code = 56,
                status_message = '',
                time = '',
                cost = 1.337,
                tasks_count = 56,
                tasks_error = 56,
                tasks = [
                    dataforseo_client.models.dataforseo_labs_google_historical_serps_live_task_info.DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo()
                    ]
            )
        else:
            return DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo(
        )
        """

    def testDataforseoLabsGoogleHistoricalSerpsLiveResponseInfo(self):
        """Test DataforseoLabsGoogleHistoricalSerpsLiveResponseInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
