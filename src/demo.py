from mitmproxy import http
import json

replacement_meta = [
    ('Hack all the things', 'https://www.youtube.com/watch?v=FoUWHfh733Y', 'https://i.kym-cdn.com/photos/images/newsfeed/001/209/715/032.png'),
    ('Hacker descends into New York', 'https://www.youtube.com/watch?v=bV-hSgL1R74', 'https://pbs.twimg.com/media/CV-TEEpWwAMWLMU.jpg'),
    ('Hacker flees canadian bar', 'https://www.whistlerblackcomb.com/', 'https://www.wired.com/images_blogs/thisdayintech/2012/02/mitnick-2.jpg'),
    ('Norwegian party wins swedish election', 'https://www.youtube.com/watch?v=GYNJuP6m9JU', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/4b/Swedish_civil_ensign_%281844%E2%80%931905%29.svg/800px-Swedish_civil_ensign_%281844%E2%80%931905%29.svg.png')
]


def response(flow: http.HTTPFlow) -> None:
    if '/svc/mcs/v3/composites/sections/cnn/' in flow.request.path:
        j = json.loads(flow.response.content.decode())
        for card_i in range(len(j['cards'])):
            card = j['cards'][card_i]
            replacement = replacement_meta[card_i % len(replacement_meta)]
            card['headline'] = replacement[0]
            card['url'] = replacement[1]
            if card['cuts'] is not None:
                for cut_key in card['cuts'].keys():
                    card['cuts'][cut_key]['url'] = replacement[2]
        flow.response.content = json.dumps(j).encode()
    elif '/mobile/android/prod/partner/edgepanel/edge-config.json' in flow.request.path:
        flow.response.status_code = 200
        flow.response.content = json.dumps({
            "content_api_prefix": "http://compositor.api.cnn.com/svc/mcs/v3/composites",
            "content_api_suffix": "/rows:10/start:0",
            "killswitch_url": "http://config.outturner.com/mobile/android/prod/partner/edgepanel/edgepanelkill.json",
            "domestic_sections": [
                {"name":"Hacking", "segment":"/sections/cnn/homepage"},
                {"name":"Hacking", "segment":"/sections/cnn/mobile-app-featured"},
                {"name":"Hacking", "segment":"/sections/cnn/us"},
                {"name":"Hacking", "segment":"/sections/cnn/world"},
                {"name":"Hacking", "segment":"/sections/cnn/entertainment"},
                {"name":"Hacking", "segment": "/sections/cnn/politics"},
                {"name":"Hacking", "segment":"/sections/cnn/tech"},
                {"name":"Hacking", "segment":"/sections/money/home"}
            ],
            "international_sections":
            [
                {"name":"Hacking", "segment":"/sections/cnn/homepage_intl"},
                {"name":"Hacking", "segment":"/sections/cnn/intl_mobile-app-featured"},
                {"name":"Hacking", "segment":"/sections/cnn/us"},
                {"name":"Hacking", "segment":"/sections/cnn/africa"},
                {"name":"Hacking", "segment":"/sections/cnn/asia"},
                {"name":"Hacking", "segment": "/sections/cnn/europe"},
                {"name":"Hacking", "segment":"/sections/cnn/americas"},
                {"name":"Hacking", "segment":"/sections/cnn/middleeast"},
                {"name":"Hacking", "segment":"/sections/money/home-international"},
                {"name":"Hacking", "segment":"/sections/cnn/style"},
                {"name":"Hacking", "segment":"/sections/cnn/entertainment"},
                {"name":"Hacking", "segment":"/sections/cnn/tech"},
                {"name":"Hacking", "segment":"/sections/cnn/intl_travel"}
            ],
            "enable_appstore_item": True
        }).encode()
    elif '/b/ss/cnn-adbp-apps-widgets/0/JAVA-3.2.5-AN/' in flow.request.path:
        print('Got metrics', flow.request.query['pageName'], flow.request.query['CarrierName'], flow.request.query['DeviceName'], flow.request.query['OSVersion'])
    elif '/mobile/android/prod/partner/edgepanel/edgepanelkill.json' in flow.request.path:
        j = json.loads(flow.response.content.decode())
        flow.response.content = json.dumps(j + [{'highestVersion': '', 'specificVersion': '1.0.rc41', 'deviceModel': 'SM-G950F', 'liveDate': '2015-04-28 12:00:00', 'alertTitle': 'Upgrade Sun', 'alertMessage': 'An upd8 is available.', 'alertOKButtonTitle': 'Upgrade Nauw', 'alertCancelButtonTitle': 'Upgrade Laiter', 'numTimesIgnoreBetweenTrigger': 3, 'phoneWebPageUrl': 'http://cnn.com', 'shouldForceUpgrade': True, 'shouldUpgrade': True, 'appStoreURL': 'https://www.youtube.com/watch?v=AvAnfi8WpVE'}]).encode()
