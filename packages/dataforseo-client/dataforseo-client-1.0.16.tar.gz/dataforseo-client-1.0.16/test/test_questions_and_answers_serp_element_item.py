# coding: utf-8

"""
    DataForSEO API documentation

    DataForSEO API is the starting point on your journey towards building powerful SEO software. With DataForSEO you can get all the data you need to build an efficient application while also saving your time and budget. DataForSEO API is using the REST technology for interchanging data between your application and our service. The data exchange is made through the widely used HTTP protocol, which allows applying our API to almost all programming languages.

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from dataforseo_client.models.questions_and_answers_serp_element_item import QuestionsAndAnswersSerpElementItem

class TestQuestionsAndAnswersSerpElementItem(unittest.TestCase):
    """QuestionsAndAnswersSerpElementItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> QuestionsAndAnswersSerpElementItem:
        """Test QuestionsAndAnswersSerpElementItem
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `QuestionsAndAnswersSerpElementItem`
        """
        model = QuestionsAndAnswersSerpElementItem()
        if include_optional:
            return QuestionsAndAnswersSerpElementItem(
                rank_group = 56,
                rank_absolute = 56,
                position = '',
                xpath = '',
                items = [
                    dataforseo_client.models.questions_and_answers_element.QuestionsAndAnswersElement(
                        type = '', 
                        url = '', 
                        question_text = '', 
                        answer_text = '', 
                        source = '', 
                        domain = '', 
                        votes = 56, )
                    ],
                rectangle = dataforseo_client.models.rectangle.Rectangle(
                    x = 1.337, 
                    y = 1.337, 
                    width = 1.337, 
                    height = 1.337, )
            )
        else:
            return QuestionsAndAnswersSerpElementItem(
        )
        """

    def testQuestionsAndAnswersSerpElementItem(self):
        """Test QuestionsAndAnswersSerpElementItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
