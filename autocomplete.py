#!/usr/bin/env python3
# encoding: utf-8

import requests, json, sys
import html


def google(query, pos=-1):
    url = 'https://www.google.com/complete/search'
    payload = {
        'client': 'hp',
        'xhr': 't',
        'q': query,
        'cp': len(query) if pos < 0 else pos,
        'hl': 'zh-CN'
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36'
    }
    r = requests.get(url, params=payload, headers=headers, timeout=5)
    d = json.loads(r.text)
    print(r.text, file=sys.stderr)
    return [html.unescape(i[0]) for i in d[1]]
