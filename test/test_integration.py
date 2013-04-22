from unittest import TestCase
import requests

from fundfindi.dao.DomainObject import delete as index_del
#from fundfind import whatever we're testing

base_url = "http://localhost:5000/lookup/"
funder_submit = ['url': base_url + 'describe_funder', 'method':'POST']
fundopp_submit = ['url': base_url + 'share_fundopp', 'method':'POST']

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
            "tags": [
                "healthcare",
                "medical",
                "biology",
                "support open access"
            ],
            "owner": "emanuil",
            "id": "3202f106e8894f08b49eb69d41863e88",
            "name": "Wellcome Trust",
            "created": "2013-02-08T10:38:29.273696",
            "homepage": "http://www.wellcome.ac.uk/",
            "modified": "2013-02-08T10:38:29.273719",
            "useful_links": [
                "http://www.wellcome.ac.uk/About-us/Policy/Policy-and-position-statements/wtd002766.htm",
                "http://www.wellcome.ac.uk/About-us/Jobs/index.htm"
            ],
            "policies": "http://www.wellcome.ac.uk/About-us/Policy/index.htm",
            "interested_in": "primarily healthcare, some other biology research, possibly other things but not primary focus - check their pages"
        }
        requests.post(funder_submit, data=funder)
