from typing import List
from unittest import TestCase

from events_parsers.utils.referrer import get_normalized_referrer, has_gclid_in_query, parse_urls, get_utm_source


class GetNormalizedReferrerTest(TestCase):
    def test_null(self):
        self.assertIsNone(get_normalized_referrer(None, None, None))
        self.assertIsNone(get_normalized_referrer('a', 'a', None))
        self.assertIsNone(get_normalized_referrer(None, 'a', None))
        self.assertIsNone(get_normalized_referrer('a', None, 'a'))

    def test_utm(self):
        self.assertEqual(
            'google ads',
            get_normalized_referrer(
                'https://podscribe.com/?gclid=123123',
                'https://podscribe.com/?utm_source=google',
                'cerebral'
            )
        )


        self.assertNotEqual(
            'google ads',
            get_normalized_referrer(
                'https://podscribe.com/',
                'https://podscribe.com/',
                'podscribe'
            )
        )

    def test_same_domain(self):
        self.assertIsNone(
            get_normalized_referrer(
                'https://podscribe.com/',
                None,
                'podscribe'
            )
        )

        self.assertIsNone(
            get_normalized_referrer(
                'https://aaa-podscribe-aaa.com/',
                None,
                'podscribe'
            )
        )

    def test_referer(self):
        self.assertEqual(
            'googleusercontent',
            get_normalized_referrer('https://12342134-atari-embeds.googleusercontent.com/', None, 'podscribe'),
        )

        self.assertEqual(
            'google',
            get_normalized_referrer('https://mail.google.com/mail/mu/mp/144/', None, 'podscribe'),
        )

        self.assertEqual(
            'google',
            get_normalized_referrer('https://www.google.com.pg/', None, 'podscribe'),
        )

        self.assertEqual(
            'google',
            get_normalized_referrer('https://myactivity.google.com/', None, 'podscribe'),
        )

        self.assertEqual(
            't',
            get_normalized_referrer('https://t.co/', None, 'podscribe'),
        )

        self.assertEqual(
            'newprogrammatic',
            get_normalized_referrer('http://media.newprogrammatic.click/', None, 'podscribe'),
        )

        self.assertEqual(
            'duomai',
            get_normalized_referrer(
                'https://c.duomai.com/track.php?aid=9245&dm_fid=16055&euid=&site_id=929462&t=https://cariuma.com/',
                None,
                'podscribe'
            ),
        )

class GetUtmSourceTest(TestCase):
    def test_returns_null_if_empty(self):
        result = get_utm_source(None)
        self.assertEqual(None, result)

    def test_returns_utm_source(self):
        result = get_utm_source('https://podscribe.com/?utm_source=google')
        self.assertEqual('google', result)


class ParseUrlsTest(TestCase):
    @staticmethod
    def __filter_len(data: List) -> int:
        return len(list(filter(None, data)))

    def test_null(self):
        result = parse_urls(['', None, '_'])
        self.assertEqual(0, self.__filter_len(result))

    def test_exception(self):
        result = parse_urls([
            'http://',
            'jija',
            'http://localhost:8000',
            'http://1.2.3.4/'
        ])

        self.assertEqual(0, self.__filter_len(result))

    def test_scheme(self):
        result = parse_urls([
            'android-app://and.some.app/',
            'posgresql://podscribe.com/',
        ])
        self.assertEqual(0, self.__filter_len(result))

    def test_normal(self):
        result = parse_urls([
            'http://podscribe.com/',
            'https://podscribe.com/'
        ])
        self.assertEqual(2, self.__filter_len(result))

    def test_mixed(self):
        result = parse_urls([
            'some_meme',
            'mysql://podscribe.com/',
            'https://www.google.com/',
            'https://podscribe.com.au/',
            'https://not-podscribe.com/?utm_source=google'
        ])
        self.assertEqual(3, self.__filter_len(result))


class HasGclidInQueryTest(TestCase):
    def test_true(self):
        self.assertTrue(has_gclid_in_query(['https://podscribe.com/?gclid=google&some_another_param=123']))

        self.assertTrue(has_gclid_in_query([
            'https://podscribe.com/?gclid=google',
            'https://podscribe.com/?gclid=google'
        ]))


    def test_false(self):
        self.assertFalse(has_gclid_in_query(['https://podscribe.com/?some_another_param=123']))

        self.assertFalse(has_gclid_in_query([
            'https://podscribe.com/',
            'https://podscribe.com/'
        ]))
