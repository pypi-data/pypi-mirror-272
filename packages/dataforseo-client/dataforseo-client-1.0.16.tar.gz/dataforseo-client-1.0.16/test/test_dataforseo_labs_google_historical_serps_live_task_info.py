# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.dataforseo_labs_google_historical_serps_live_task_info import DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo

class TestDataforseoLabsGoogleHistoricalSerpsLiveTaskInfo(unittest.TestCase):
    """DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo:
        """Test DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo`
        """
        model = DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo()
        if include_optional:
            return DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo(
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
                    dataforseo_client.models.dataforseo_labs_google_historical_serps_live_result_info.DataforseoLabsGoogleHistoricalSerpsLiveResultInfo(
                        se_type = '', 
                        keyword = '', 
                        location_code = 56, 
                        language_code = '', 
                        total_count = 56, 
                        items_count = 56, 
                        items = [
                            dataforseo_client.models.dataforseo_labs_google_historical_serps_live_item.DataforseoLabsGoogleHistoricalSerpsLiveItem(
                                se_type = '', 
                                keyword = '', 
                                type = '', 
                                se_domain = '', 
                                location_code = 56, 
                                language_code = '', 
                                check_url = '', 
                                datetime = '', 
                                spell = dataforseo_client.models.spell_info.SpellInfo(
                                    keyword = '', 
                                    type = '', ), 
                                item_types = [
                                    ''
                                    ], 
                                se_results_count = 56, 
                                items_count = 56, )
                            ], )
                    ]
            )
        else:
            return DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo(
        )
        """

    def testDataforseoLabsGoogleHistoricalSerpsLiveTaskInfo(self):
        """Test DataforseoLabsGoogleHistoricalSerpsLiveTaskInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
