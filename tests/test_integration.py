from unittest import TestCase
import requests
import json

base_url = "http://localhost:5001/"
req_format = '.json'
funder_submit = base_url + 'describe_funder' + req_format
fundopp_submit = base_url + 'share_fundopp' + req_format
slugify = base_url + 'slugify'
suggest = base_url + 'suggest'
suggest_projects = base_url + 'suggest/projects'

test_user_api_key = '385d7475-5e4b-4ce8-ab69-1fd7c3e5cbcb'

created_objects = [] # objects created during testing - each has "_type" & "id"

class TestIntegration(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        for obj in created_objects:
            index_del(obj['_type'], obj['id'])

    def test_describe_funder(self):
        funder = {
            "description": "We are a global charitable foundation dedicated to achieving extraordinary improvements in human and animal health.\r\n\r\nWe support the brightest minds in biomedical research and the medical humanities. Our breadth of support includes public engagement, education and the application of research to improve health. Find out more about our vision and what we do.\r\n\r\nWe are independent of both political and commercial interests.",
            "tags": "healthcare, medical  ,biology,  support open access  ",
            "name": "Wellcome Trust",
            "homepage": "http://www.wellcome.ac.uk/",
            "useful_links": [
                "http://www.wellcome.ac.uk/About-us/Policy/Policy-and-position-statements/wtd002766.htm",
                "http://www.wellcome.ac.uk/About-us/Jobs/index.htm"
            ],
            "policies": "http://www.wellcome.ac.uk/About-us/Policy/index.htm",
            "interested_in": "primarily healthcare, some other biology research, possibly other things but not primary focus - check their pages"
        }

        # only registered users can submit information - the application will
        # recognise the API key if it belongs to an existing user if we put
        # it in the request data
        funder['api_key'] = test_user_api_key

        r = requests.post(funder_submit, data=funder)
        assert r.status_code == 200, 'Funder information submission failed'

    def test_describe_fundopp(self):
        fundopp = {
            "description": "Description",
            "tags": "tag1, tag2,   tag  3  ",
            "funds": "10000",
            "funds_exactly_or_upto": "upto",
            "issue_date": "2012-12-11",
            "title": "ESRC opportunity title2",
            "closing_date": "2013-02-10",
            "useful_links": [
                "http://link1"
            ],
            "url": "",
            "unique_title": "esrc_opportunity_title2",
            "funder": "ESRC"
        }

        # only registered users can submit information - the application will
        # recognise the API key if it belongs to an existing user if we put
        # it in the request data
        fundopp['api_key'] = test_user_api_key

        r = requests.post(fundopp_submit, data=fundopp)
        assert r.status_code == 200, 'Funding opportunity information submission failed'

    def test_slugify(self):
        data = {'make_into_slug': ' Funding Opportunity Title! .'}
        expected_slug = 'funding_opportunity_title'
        
        # try GET-ing, the way the UI uses it
        r = requests.get(slugify, params=data)
        assert r.status_code == 200, 'slugification failed, status code unexpected'
        assert r.text == expected_slug, 'slugification failed, wrong slug'

        # try POST-ing as well, for the sake of API users
        r = requests.post(slugify, data=data)
        assert r.status_code == 200, 'slugification failed, status code unexpected'
        assert r.text == expected_slug, 'slugification failed, wrong slug'

    def test_suggest(self):
        data = {'similar_to': 'Aberystwyth'}
        
        # try GET-ing, the way the UI uses it
        r = requests.get(suggest, params=data)
        assert r.status_code == 200, 'suggestions failed, status code unexpected'
        assert len(json.loads(r.text)) > 0, 'suggestions failed, no suggestions came back (but should have)'

        # try POST-ing as well, for the sake of API users
        r = requests.post(suggest, data=data)
        assert r.status_code == 200, 'suggestions failed, status code unexpected'
        assert len(json.loads(r.text)) > 0, 'suggestions failed, no suggestions came back (but should have)'

    def test_suggest_projects(self):
        # very similar to previous test, just testing the other route here
        data = {'similar_to': 'Aberystwyth'}
        
        # try GET-ing, the way the UI uses it
        r = requests.get(suggest_projects, params=data)
        assert r.status_code == 200, 'suggestions failed, status code unexpected'
        assert len(json.loads(r.text)) > 0, 'suggestions failed, no suggestions came back (but should have)'

        # try POST-ing as well, for the sake of API users
        r = requests.post(suggest_projects, data=data)
        assert r.status_code == 200, 'suggestions failed, status code unexpected'
        assert len(json.loads(r.text)) > 0, 'suggestions failed, no suggestions came back (but should have)'
