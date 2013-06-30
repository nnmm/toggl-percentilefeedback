#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests

from urllib import urlencode
from requests.auth import HTTPBasicAuth


class TogglAPI(object):
    """A wrapper for Toggl Api"""

    def __init__(self, api_token, timezone):
        self.api_token = api_token
        self.timezone  = timezone


    def _make_url(self, section='time_entries', params={}):
        """Constructs and returns an api url to call with the section of the API to be called
        and parameters defined by key/pair values in the paramas dict.
        Default section is "time_entries" which evaluates to "time_entries.json"

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {})
        'https://www.toggl.com/api/v8/time_entries'

        >>> t = TogglAPI('_SECRET_TOGGLE_API_TOKEN_')
        >>> t._make_url(section='time_entries', params = {'start_date' : '2010-02-05T15:42:46+02:00', 'end_date' : '2010-02-12T15:42:46+02:00'})
        'https://www.toggl.com/api/v8/time_entries?start_date=2010-02-05T15%3A42%3A46%2B02%3A00%2B02%3A00&end_date=2010-02-12T15%3A42%3A46%2B02%3A00%2B02%3A00'
        """

        url = 'https://www.toggl.com/api/v8/{}'.format(section)
        if len(params) > 0:
            url = url + '?{}'.format(urlencode(params))
        return url

    def _query(self, url, method):
        """Performs the actual call to Toggl API"""

        url = url
        headers = {'content-type': 'application/json'}

        if method == 'GET':
            return requests.get(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        elif method == 'POST':
            return requests.post(url, headers=headers, auth=HTTPBasicAuth(self.api_token, 'api_token'))
        else:
            raise ValueError('Undefined HTTP method "{}"'.format(method))

    ## Time Entry functions
    def get_time_entries(self, start_date, end_date):
        """Get Time Entries JSON object from Toggl"""

        url = self._make_url(section='time_entries', params={'start_date': start_date+self.timezone, 'end_date': end_date+self.timezone})
        r = self._query(url=url, method='GET')
        return r.json()