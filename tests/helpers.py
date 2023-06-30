from unittest import TestCase

from events_parsers.helpers import get_normalized_referrer


class ReferrerTest(TestCase):

    def test_null(self):
        self.assertIsNone(get_normalized_referrer(''))
        self.assertIsNone(get_normalized_referrer(None))
        self.assertIsNone(get_normalized_referrer('_'))

    def test_exception(self):
        self.assertIsNone(get_normalized_referrer('http://'))
        self.assertIsNone(get_normalized_referrer('jija'))
        self.assertIsNone(get_normalized_referrer('http://localhost:8000'))
        self.assertIsNone(get_normalized_referrer('http://209.68.59.50/'))

    def test_scheme(self):
        self.assertIsNone(get_normalized_referrer('android-app://and.lihuhu.findmatch/'))
        self.assertIsNone(get_normalized_referrer('posgresql://podscribe.com/'))

        self.assertIsNotNone(get_normalized_referrer('http://podscribe.com/'))
        self.assertIsNotNone(get_normalized_referrer('https://podscribe.com/'))

    def test_domain(self):
        self.assertEqual(
            get_normalized_referrer('https://2005971197-atari-embeds.googleusercontent.com/'),
            'Googleusercontent'
        )

        self.assertEqual(
            get_normalized_referrer('https://mail.google.com/mail/mu/mp/144/'),
            'Google'
        )

        self.assertEqual(
            get_normalized_referrer('https://www.google.com.pg/'),
            'Google'
        )

        self.assertEqual(
            get_normalized_referrer('https://myactivity.google.com/'),
            'Google'
        )

        self.assertEqual(
            get_normalized_referrer('https://t.co/'),
            'T'
        )

        self.assertEqual(
            get_normalized_referrer('http://media.newprogrammatic.click/'),
            'Newprogrammatic'
        )

        self.assertEqual(
            get_normalized_referrer('https://c.duomai.com/track.php?aid=9245&dm_fid=16055&euid=&site_id=929462&t=https://cariuma.com/'),
            'Duomai'
        )


    def test_google_ads(self):
        self.assertEqual(
            get_normalized_referrer('https://cerebral.com/?cabt=price:week&utm_source=google&utm_medium=cpc&utm_campaign=Branded_mCPC_2022&utm_campaignid=14992201590&utm_term=cerebral&utm_mt=e&utm_content=651903148753&utm_adgroup=134286538691&utm_device=m&utm_location=9004045&utm_position=&gclid=Cj0KCQjw1_SkBhDwARIsANbGpFvoMKz1mhHqU-G60n9Ho04hboIkGngWSk-ic5pPCiIKbH2w5imcYhcaAtYnEALw_wcB'),
            'Google ads'
        )

        self.assertEqual(
            get_normalized_referrer('https://cerebral.com/?utm_source=google'),
            'Google ads'
        )
