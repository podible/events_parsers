import unittest
from .user_agent import normalize_user_agent, normalize_device

# Run test: python -m unittest utils.user_agent_test


class TestUserAgentMethods(unittest.TestCase):
    def test_normilize_device(self):
        normalized = normalize_device(
            "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)"
        )
        self.assertEqual(normalized, "Windows Computer")

    def test_normalize_user_agent_for_app(self):
        for ua in [
            ("iHeartRadio/9.24.3 (iPod touch; iOS 12.5.6; iPod7,1)", "iHeartRadio"),
        ]:
            normalized = normalize_user_agent(ua[0])
            self.assertEqual(normalized, ("app", ua[1]))

    def test_normalize_user_agent_for_browser(self):
        normalized = normalize_user_agent(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
        )
        self.assertEqual(normalized, ("browser", "Chrome"))

    def test_normalize_user_agent_for_bot(self):
        for ua in [
            ("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)", "Googlebot"),
            ("Trackable/0.1", "Chartable"),
        ]:
            normalized = normalize_user_agent(ua[0])
            self.assertEqual(normalized, ("bot", ua[1]))

    def test_normalize_user_agent_for_library_bot(self):
        for ua in [
            ("okhttp/3.12.1", "okhttp"),
        ]:
            normalized = normalize_user_agent(ua[0])
            self.assertEqual(normalized, ("bot", ua[1]))

    def test_normalize_user_agent_for_library(self):
        for ua in [
            ("AppleCoreMedia/1.0.0.16G114 (iPod touch; U; CPU OS 12_4_2 like Mac OS X; en_us)", "AppleCoreMedia"),
        ]:
            normalized = normalize_user_agent(ua[0])
            self.assertEqual(normalized, ("library", ua[1]))


if __name__ == "__main__":
    unittest.main()
