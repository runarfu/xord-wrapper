#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from itertools import count
from itertools import groupby

_XORD_URL = 'http://kryssord.dyndns.org/X2index2.php'
_XORD_ENCODING = 'Latin-1'

_session = requests.session()

def lookup_all_synonyms(search_token):
    return lookup_synonyms(search_token, '*')

def lookup_synonyms_with_length(search_token, solution_length):
    return lookup_synonyms(search_token, '?' * solution_length)

def lookup_synonyms(search_token, solution_hints):
    parameters = {'X2f1' : search_token.encode(_XORD_ENCODING),
                  'MC'   : '1',
                  'X2ssy': 'Søk+Synonym',
                  'X2f2' : solution_hints}
    words = _lookup(parameters)

    extra_words = _lookup_synonyms_with_page_traversal(search_token, solution_hints)
    words.extend(extra_words)

    return _results_as_dict(words)

def _lookup(parameters):
    response = _session.post(_XORD_URL, data=parameters)
    response.encoding = _XORD_ENCODING
    return _find_words_in_tds(response.text)

def _find_words_in_tds(html):
    soup = BeautifulSoup(html)
    tds = soup.findAll('td', {'class' : 'td_ord'})
    return [td.find('a').contents[0] for td in tds]

def _lookup_synonyms_with_page_traversal(search_token, solution_hints):
    extra_words = []
    for pagenumber in count(2):
        words = _lookup_synonyms_page(search_token, solution_hints, pagenumber)
        if words:
            extra_words.extend(words)
        else:
            return extra_words

def _lookup_synonyms_page(search_token, solution_hints, pagenumber):
    parameters = {'X2f1'  : search_token,
                  'p'     : str(pagenumber),
                  'MP'    : '1',
                  'X2f'   : 'ss',
                  'X2f2'  : solution_hints}
    return _lookup(parameters)

def _results_as_dict(synonyms):
    groups = groupby(sorted(synonyms, key=len), len)
    return {'result_size' : len(synonyms), 'result' : [{'length' : length, 'words' : sorted(list(group))} for length, group in groups]}

