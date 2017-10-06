from common import BaseMockedTestCase, test_case

from pinterest.client import PintObject

class TestPin(BaseMockedTestCase):
    fields_list = 'attribution%2Cboard%2Ccolor%2Ccounts%2Ccreated_at%2Ccreator%2Cid%2Cimage%2Clink%2Cmedia%2Cmetadata%2Cnote%2Coriginal_link%2Curl'

    @test_case('pin', 'GET')
    def test_get(self):
        pin = self.client.pins.get(1234)
        self.mock_request.assert_called_with(
            method='get',
            params=None,
            url='https://api.pinterest.com/v1/pins/1234?access_token=test-mock-token&fields={fields}'.format(fields=self.fields_list)
        )
        self.assertIsInstance(pin, PintObject)
        self.assertEqual(pin.id, 1234)
        self.assertEqual(pin.note, u'A test pin')

    @test_case('pin', 'POST')
    def test_create(self):
        pin = self.client.pins.create(
            board='Testboard',
            note='this is a test',
            image_url='http://lorempixel/300/400/sports',
            link='http://example.com',
        )
        self.mock_request.assert_called_with(
            method='post',
            json=dict(board='Testboard',
                note='this is a test',
                image_url='http://lorempixel/300/400/sports',
                link='http://example.com'
            ),
            url='https://api.pinterest.com/v1/pins/?access_token=test-mock-token&'
                'fields={fields}'.format(fields=self.fields_list)
        )
        self.assertIsInstance(pin, PintObject)
        self.assertEqual(pin.id, 1234)
        self.assertEqual(pin.note, u'A test pin')
