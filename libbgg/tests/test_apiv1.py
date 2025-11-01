from unittest import (
    TestCase,
    mock,
)
from unittest.mock import MagicMock


from libbgg.apibase import BGGBase
from libbgg.tests.fixtures import bgg_boardgame_response

class TestBGGBase(TestCase):

    def setUp(self):
        self.api_token = 'abc123'
        self.url_base = 'http://www.boardgamegeek.com'
        self.path_base = '/xmlapi'
        self.base = BGGBase(
            self.api_token,
            self.url_base,
            self.path_base,
        )

    def test_init(self):
        self.assertEqual(self.base.api_token, self.api_token)
        self.assertEqual(self.base.url_base, 'http://www.boardgamegeek.com')
        self.assertEqual(self.base.path_base, 'xmlapi')
        self.assertEqual(self.base._base, 'http://www.boardgamegeek.com/xmlapi')

    @mock.patch('libbgg.apibase.build_opener')
    @mock.patch('libbgg.apibase.install_opener')
    def test_get_opener(self, install_opener, build_opener):
        self.base._get_opener()
        self.assertTrue(install_opener.called)
        self.assertTrue(build_opener.called)

    def test_call_boardgame(self):

        with mock.patch.object(self.base, '_opener', new=self.mock_get_opener(bgg_boardgame_response)):
            d = {
                'stats': int(False),
                'marketplace': int(False),
            }
            response = self.base.call('boardgame/1', d)
            self.assertEqual(response['boardgames']['boardgame']['name'][0].TEXT, 'Die Macher')

    def mock_get_opener(self, return_value):
        mock_open = MagicMock()
        mock_open.open = MagicMock()
        mock_open.open.return_value = MagicMock()
        mock_open.open.return_value.read = MagicMock()
        mock_open.open.return_value.read.return_value = return_value
        return mock_open
