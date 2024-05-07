# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.backlinks_anchors_live_request_info import BacklinksAnchorsLiveRequestInfo

class TestBacklinksAnchorsLiveRequestInfo(unittest.TestCase):
    """BacklinksAnchorsLiveRequestInfo unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BacklinksAnchorsLiveRequestInfo:
        """Test BacklinksAnchorsLiveRequestInfo
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BacklinksAnchorsLiveRequestInfo`
        """
        model = BacklinksAnchorsLiveRequestInfo()
        if include_optional:
            return BacklinksAnchorsLiveRequestInfo(
                target = '',
                limit = 56,
                offset = 56,
                internal_list_limit = 56,
                backlinks_status_type = '',
                filters = [
                    None
                    ],
                order_by = [
                    ''
                    ],
                backlinks_filters = [
                    None
                    ],
                include_subdomains = True,
                include_indirect_links = True,
                exclude_internal_backlinks = True,
                tag = ''
            )
        else:
            return BacklinksAnchorsLiveRequestInfo(
        )
        """

    def testBacklinksAnchorsLiveRequestInfo(self):
        """Test BacklinksAnchorsLiveRequestInfo"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
