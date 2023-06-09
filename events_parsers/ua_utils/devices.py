import re

devices = [
    {"name": "Apple HomePod", "pattern": re.compile("HomePod"), "category": "smart_speaker"},
    {"name": "Apple iPad", "pattern": re.compile("ipad|iPad|IPAD"), "category": "mobile"},
    {
        "name": "Apple TV",
        "pattern": re.compile("Apple TV|AppleTV|apple;apple_tv"),
        "category": "smart_tv",
        "examples": [
            "apple;apple_tv;33ddb95064d1479ab37179579af23b77;;tpapi;3.200.405",
            "AppleCoreMedia/1.0.0.20K71 (Apple TV; U; CPU OS 16_1 like Mac OS X; en_au)",
        ],
    },
    {
        "name": "Apple iPhone",
        "pattern": re.compile("iphone|iOS|iPhone|CFNetwork| ios |phone;ios"),
        "category": "mobile",
        "examples": [
            "Fountain/0.5.3 ios https://www.fountain.fm",
            "Anytime/1.1 b64 (phone;ios Version 15.6.1 (Build 19G82)) https://github.com/amugofjava/anytime_podcast_player",
        ],
    },
    {"name": "Apple Watch", "pattern": re.compile("watch|Watch OS"), "category": "watch"},
    {"name": "Apple iPod", "pattern": re.compile("iPod|IPOD"), "category": "mobile"},
    {"name": "Apple Computer", "pattern": re.compile("OS X|OSX|Macintosh|Macbook"), "category": "computer"},
    {"name": "Google Home", "pattern": re.compile("GoogleChirp|Google-Speech-Actions"), "category": "smart_speaker"},
    {"name": "Google Chromebook", "pattern": re.compile("Chromebook|CrOS"), "category": "computer"},
    {
        "name": "Android Tablet",
        "pattern": re.compile("[a|A]ndroid.*[t|T]ablet|[t|T]ablet.*[a|A]ndroid|SM-T| GT-"),
        "category": "mobile",
    },
    {
        "name": "Other Smart TV",
        "pattern": re.compile("SmartTV|Roku|CrKey|AFTT Build|AFTM Build|BRAVIA 4K|Opera TV|SmartTv|TSBNetTV|SMART-TV|TV Safari|WebTV|InettvBrowser|GoogleTV|HbbTV|smart-tv|olleh tv|^sony_tv;ps5;|Microsoft Xbox|^Google;Chromecast"),
        "category": "smart_tv",
        "comments": "Must be before Android Phones",
        "examples": [
            "Microsoft Xbox",
            "sony_tv;ps5;9b18101888dd42948afd0b8792122bec;;tpapi;3.200.405",
            "Google;ChromecastHD;756a522d9f1648b89e76e80be654456a;;tpapi;3.200.454",
        ],
    },
    {
        "name": "Android Phone",
        "pattern": re.compile("ServeStream|Android|android|HTC|ExoPlayer|^AntennaPod/|^GSA/.*\\.arm(64)?$|^sp-agent"),
        "category": "mobile",
        "comments": "Must be after CrKey and Android Tablet",
        "examples": ["GSA/13.39.12.26.arm64", "GSA/13.39.12.26.arm", "sp-agent", "FileDownloader (Android)"],
    },
    {
        "name": "Windows Computer",
        "pattern": re.compile("Windows|windows|WMPlayer|Winamp|Win32|Win64|NSPlayer|MediaMonkey|NSPlayer|PC"),
        "category": "computer",
    },
    {"name": "Amazon Smart Speaker", "pattern": re.compile("Alexa|^Echo/"), "category": "smart_speaker"},
    {"name": "Other Smart Speaker", "pattern": re.compile("sonos|Sonos|^Bose/|^VictorReader"), "category": "smart_speaker"},
    {"name": "Other Computer", "pattern": re.compile("Lavf/|desktop|Linux|linux|VLC|^okhttp/|CastBox/"), "category": "computer"},
    {"name": "Other Tablet", "pattern": re.compile("tablet|Tablet"), "category": "mobile"},
    {"name": "Other Watch", "pattern": re.compile("watch|Watch"), "category": "watch"},
    {
        "name": "Other Mobile Device",
        "pattern": re.compile("Player FM$|^Podkicker\/|spotify_unknown|^Castro|^Swoot Agent| KAIOS/|^Zune/|^PodcastGuru |^Pocket Casts$|^AmazonMusic$"),
        "category": "mobile",
        "examples": [
            "Mozilla/5.0 (Mobile; Nokia_8110_4G; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.5.1 PodKast",
            "Zune/4.8",
            "PodcastGuru 2.0.2-beta3",
            "Pocket Casts",
            "AmazonMusic",
        ],
    },
]
