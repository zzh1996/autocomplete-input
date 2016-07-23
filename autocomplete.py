#!/usr/bin/env python3
# encoding: utf-8

import requests, json, sys


def google(query, pos=-1):
    url = 'https://www.google.com/complete/search'
    payload = {
        # 'sclient': 'psy-ab',
        'gs_ri': 'psy-ab',
        'q': query,
        'tch': 1,
        'ech': '',
        'cp': len(query) if pos < 0 else pos
    }
    r = requests.get(url, params=payload, timeout=5)
    j = json.loads(r.text[:-6])
    d = json.loads(j['d'])
    return [i[0] for i in d[1]]
