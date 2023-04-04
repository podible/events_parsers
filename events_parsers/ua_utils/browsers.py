import re

browsers = [
    {"name": "Brave", "pattern": re.compile(".+[Bb]rave")},
    {
        "name": "Opera",
        "pattern": re.compile("Opera/|Macintosh.*OPR/|Windows.*OPR/|Mobile/.* OPT/"),
        "examples": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36 OPR/72.0.3815.186",
            "Mozilla/5.0 (iPad; CPU OS 15_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 OPT/3.2.13",
        ],
        "comments": "Must match above Chrome",
    },
    {
        "name": "Edge",
        "pattern": re.compile("(Xbox.+Edg?/|Android.+EdgA/|iPhone.+EdgiOS/|Macintosh.+MacEdgeClient/|Windows Phone.+Edge?/|Windows.+Edge?/)"),
        "examples": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; WebView/3.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
        ],
        "comments": "Must match above Chrome",
    },
    {
        "name": "Chrome",
        "pattern": re.compile("^.*Android.*Chrome/|CrOS.*Chrome/|Linux.*Chrome/|Mac OS X.*Chrome/|Windows.*Chrome/|iPad.*CriOS/|iPhone.*CriOS/|^Chrome/\\d.*CFNetwork"),
        "examples": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Chrome/103.0.5060.63 CFNetwork/1390 Darwin/22.0.0",
        ],
        "comments": "Must match below Edge",
    },
    {
        "name": "Firefox",
        "pattern": re.compile("Firefox/|(Android|iPhone|iPad).*Focus/| FxiOS/"),
        "examples": [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) FxiOS/100 Mobile/15E148 Version/15.0",
        ],
    },
    {
        "name": "Internet Explorer",
        "pattern": re.compile("MSIE | Trident/"),
        "examples": [
            "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        ],
    },
    {"name": "NCSA Mosaic", "pattern": re.compile("^NCSA Mosaic/"), "examples": ["NCSA Mosaic/1.0 (X11;SunOS 4.1.4 sun4m)"]},
    {
        "name": "Safari",
        "pattern": re.compile("Macintosh.*AppleWebKit.*Safari/|Windows.*AppleWebKit.*Safari/|iPhone.*AppleWebKit.*Safari/|iPad.*AppleWebKit.*Safari/|^MobileSafari/"),
        "comments": "Must match below Chrome",
        "examples": [
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
            "MobileSafari/604.1 CFNetwork/1107.1 Darwin/19.0.0",
        ],
    },
]
