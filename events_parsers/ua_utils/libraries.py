import re

libraries = [
    {"name": "AndroidDownloadManager", "pattern": re.compile("^AndroidDownloadManager")},
    {
        "name": "Apache HttpClient",
        "pattern": re.compile("Apache-HttpClient"),
        "examples": ["Apache-HttpClient/4.5.3-SNAPSHOT (Java/1.8.0_73)"],
        "comments": "While the Apache HttpClient can also be used in an Android podcast player app, it's mostly seen today on the server-side (bots).  Most Android apps use other HTTP libraries these days.",
        "category": "bot",
    },
    {
        "name": "AppleCoreMedia",
        "pattern": re.compile("^AppleCoreMedia/1"),
        "description": "AppleCoreMedia library",
        "urls": ["https://podnews.net/article/applecoremedia-user-agent"],
        "comments": "This is a library used by a number of apps when progressively downloading podcasts. It is not (just) Apple Podcasts, and should not be treated as an Apple Podcasts useragent",
        "examples": [
            "AppleCoreMedia/1.0.0.16G114 (iPod touch; U; CPU OS 12_4_2 like Mac OS X; en_us)",
            "AppleCoreMedia/1.0.0.19A583 (Macintosh; U; Intel Mac OS X 10_15; en_us)",
            "AppleCoreMedia/1.0.0.15G77 (iPhone; U; CPU OS 11_4_1 like Mac OS X; en_us)",
            "AppleCoreMedia/1.0.0.17A860 (iPad; U; CPU OS 13_1_2 like Mac OS X; en_us)",
            "AppleCoreMedia/1.0.0.16G78 (HomePod; U; CPU OS 12_4 like Mac OS X; en_us)",
            "AppleCoreMedia/1.0.0.17J586 (Apple TV; U; CPU OS 13_0 like Mac OS X; en_us)",
        ],
    },
    {
        "name": "Armadillo",
        "pattern": re.compile("^Armadillo/1"),
        "urls": ["https://tech.scribd.com/blog/2021/android-audio-player-tutorial-with-armadillo.html"],
        "comments": "This is a library, and not an app",
        "examples": ["Armadillo/12.19 (Linux;Android 11) ExoPlayerLib/2.17.1"],
    },
    {"name": "Axios (Node)", "pattern": re.compile("^axios/"), "examples": ["axios/0.26.1"], "category": "bot"},
    {
        "name": "Colly",
        "description": "Lightning Fast and Elegant Scraping Framework for Go",
        "pattern": re.compile("github\\.com/gocolly"),
        "examples": ["colly - https://github.com/gocolly/colly"],
        "urls": ["https://github.com/gocolly/colly"],
        "category": "bot",
    },
    {
        "name": "Dalvik",
        "pattern": re.compile("^Dalvik[/ ]"),
        "examples": [
            "Dalvik/2.1.0 (Linux; U; Android 9; SM-N950U Build/PPR1.180610.011)",
            "Dalvik (Linux; U; Android 4.1.1;aries/JRO03L)",
        ],
    },
    {
        "name": "Dart",
        "pattern": re.compile("^Dart/"),
        "examples": ["Dart/2.18 (dart:io)"],
        "comments": "Default for the Dart programming language (Flutter uses Dart)",
        "category": "bot",
    },
    {
        "name": "Deno",
        "pattern": re.compile("^Deno/"),
        "examples": ["Deno/1.26.1"],
        "comments": "Default for the Deno JavaScript/TypeScript runtime",
        "category": "bot",
    },
    {
        "name": "Down (ruby)",
        "description": "Streaming downloads using net/http, http.rb, HTTPX or wget",
        "pattern": re.compile("^Down/\\d"),
        "examples": ["Down/5.3.1"],
        "urls": ["https://github.com/janko/down"],
        "category": "bot",
    },
    {
        "name": "ffmpeg",
        "pattern": re.compile("^Lavf/"),
        "comments": "ffmpeg is a library used within TuneIn, VLC, ffmpeg and other programs. This is the default useragent for the ffmpeg library.",
        "category": "bot",
    },
    {
        "name": "FileDownloader (Android)",
        "pattern": re.compile("^FileDownloader/"),
        "examples": ["FileDownloader/1.7.7"],
        "urls": ["https://github.com/lingochamp/FileDownloader"],
    },
    {
        "name": "Go Http Client",
        "pattern": re.compile("^Go-http-client"),
        "comments": "Default user-agent for Go programs",
        "examples": ["Go-http-client/2.0"],
        "urls": ["https://pkg.go.dev/net/http"],
        "category": "bot",
    },
    {
        "name": "Got (node)",
        "pattern": re.compile("^got(/| \\()"),
        "examples": ["got (https://github.com/sindresorhus/got)"],
        "urls": ["https://play.google.com/store/apps/details?id=com.podimo&hl=en_US"],
        "comments": "Got is a HTTP library for NodeJs",
        "category": "bot",
    },
    {
        "name": "GStreamer",
        "pattern": re.compile("^GStreamer|GStreamer/"),
        "examples": ["amarok/2.8.0 (Phonon/4.7.80; Phonon-GStreamer/4.7.80)"],
        "comments": "User-facing Linux media playback apps like Amarok",
    },
    {"name": "gvfs", "pattern": re.compile("^gvfs")},
    {
        "name": "hackney (elixir)",
        "pattern": re.compile("^hackney/\\d"),
        "examples": ["hackney/1.18.1"],
        "urls": ["https://github.com/benoitc/hackney"],
        "category": "bot",
    },
    {
        "name": "KaiOS Downloader",
        "pattern": re.compile("KaiOS Downloader"),
        "comments": "This is the KaiOS Downloader library, and this could refer to any app on this platform",
        "examples": ["KaiOS Downloader"],
    },
    {
        "name": "libsoup",
        "pattern": re.compile("^libsoup/"),
        "examples": ["libsoup/2.68.2"],
        "urls": ["https://libsoup.org/"],
        "description": "HTTP client/server library for GNOME",
    },
    {"name": "Android License Verification Library", "pattern": re.compile("^Android\\.LVLDM$"), "examples": ["Android.LVLDM"]},
    {
        "name": "node-fetch",
        "pattern": re.compile("^node-fetch(/.*)?$"),
        "examples": ["node-fetch/1.0 (+https://github.com/bitinn/node-fetch)", "node-fetch"],
        "category": "bot",
    },
    {"name": "okhttp", "pattern": re.compile("okhttp"), "examples": ["okhttp/3.11.0"], "category": "bot"},
    {
        "name": "python-httpx",
        "pattern": re.compile("^python-httpx/"),
        "examples": ["python-httpx/0.18.2"],
        "urls": ["https://www.python-httpx.org/"],
        "category": "bot",
    },
    {
        "name": "react-native-track-player",
        "pattern": re.compile("^react-native-track-player/"),
        "examples": ["react-native-track-player/0.5.1 (Linux;Android 12) ExoPlayerLib/2.18.1"],
        "urls": ["https://github.com/doublesymmetry/react-native-track-player"],
        "description": "A fully fledged audio module created for music apps. Provides audio playback, external media controls, chromecast support, background mode and more!",
        "comments": "Must match before exoplayer",
    },
    {"name": "Request (node)", "pattern": re.compile("request\\.js"), "category": "bot"},
    {
        "name": "reqwest (rust)",
        "pattern": re.compile("^reqwest/\\d"),
        "urls": ["https://docs.rs/reqwest/latest/reqwest/"],
        "examples": ["reqwest/0.9.19"],
    },
    {
        "name": "resty-requests (lua)",
        "pattern": re.compile("^resty-requests"),
        "urls": ["https://github.com/tokers/lua-resty-requests"],
        "examples": ["resty-requests"],
        "category": "bot",
    },
    {"name": "ruby", "pattern": re.compile("^Ruby"), "comments": "The generic Ruby user-agent."},
    {
        "name": "rest-client (ruby)",
        "pattern": re.compile("^rest-client/.*ruby/"),
        "description": "A simple HTTP and REST client for Ruby, inspired by Sinatra",
        "comments": "Found mostly coming from Amazon IPs",
        "examples": ["rest-client/2.0.2 (linux-gnu x86_64) ruby/2.6.8p205"],
        "urls": ["https://github.com/rest-client/rest-client"],
        "category": "bot",
    },
    {
        "name": "Safari View Service (SFSafariViewController)",
        "pattern": re.compile("^SafariViewService/"),
        "examples": ["SafariViewService/8614.1.25.0.31 CFNetwork/1390 Darwin/22.0.0"],
    },
    {"name": "stagefright", "pattern": re.compile("stagefright/"), "comments": "(android)"},
    {
        "name": "Symfony (php)",
        "pattern": re.compile("^Symfony HttpClient/"),
        "examples": ["Symfony HttpClient/Curl"],
        "category": "bot",
    },
    {"name": "urllib (python)", "pattern": re.compile("^Python-urllib/"), "examples": ["Python-urllib/3.9"], "category": "bot"},
    {
        "name": "ExoPlayer (Android)",
        "pattern": re.compile(" ExoPlayerLib/"),
        "examples": [
            "yourApplicationName/2.21.9 (Linux;Android 11) ExoPlayerLib/2.14.0",
            "ExoPlayerLib/2.14.0 (Linux; Android 12) ExoPlayerLib/2.14.0",
        ],
        "urls": ["https://github.com/google/ExoPlayer"],
        "comments": "Must match after react-native-track-player. Unable to track down where everyone is copying yourApplicationName from, there are several small exoplayer examples with similar code.",
    },
]
