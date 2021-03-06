import requests

#TODO Add live flight methods

API_KEY = 'YOUR_SECRET_API_KEY'


class ExceptionHandling(Exception):
    pass


class BadRequest(ExceptionHandling):
    pass


class InvalidAPI(ExceptionHandling):
    pass


class TooManyRequests(ExceptionHandling):
    pass


class InternalError(ExceptionHandling):
    pass


def error_handling(r,api):
    if r.status_code == 400:
        raise BadRequest('Input validation failed')
    if r.status_code == 403:
        raise InvalidAPI('Error: {} is an invalid API Key'.format(api))
    if r.status_code == 429:
        raise TooManyRequests('Error: {} has made to many requests in the last minute'.format(api))
    if r.status_code == 500:
        raise InternalError('Internal server error. Has been logged with Skyscanner')
    else:
        return r.text


def get_dates_cache(market,currency,locale,origin,destination,outbound,inbound,api):
    if inbound != '':
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, destination, outbound, inbound, api
        )
    else:
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsedates/v1.0/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, destination, outbound, api
        )

    r = requests.get(q_url)
    result = error_handling(r,api)
    return result


def get_routes_cache(market, currency, locale, origin, desitination, outbound, inbound, api):
    query_url = 'http://partners.api.skyscanner.net/apiservices/browseroutes' \
                '/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}'.format(market,
                                                              currency, locale,
                                                              origin, desitination,
                                                              outbound, inbound, api)
    r = requests.get(query_url)
    result = error_handling(r,api)
    return result


def get_quotes_cache(market,currency,locale,origin,desitination,outbound,inbound,api):
    if inbound != '':
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, desitination, outbound, inbound, api
        )
    else:
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, desitination, outbound, api
        )

    r = requests.get(q_url)
    result = error_handling(r,api)
    return result

def get_cache_grid(market,currency,locale,origin,destination,outbound,inbound,api):
    if inbound != '':
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsegrid/v1.0/{}/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, destination, outbound, inbound, api
        )
    else:
        q_url = 'http://partners.api.skyscanner.net/apiservices/browsegrid/v1.0/{}/{}/{}/{}/{}/{}?apiKey={}'.format(
            market, currency, locale, origin, destination, outbound, api
        )

    r = requests.get(q_url)
    result = error_handling(r,api)

    return result


class Skyscanflightcache(object):

    def __init__(self,market='GB',currency='GBP',locale='en-GB',api_key=API_KEY):

        self.market = market
        self.currency = currency
        self.locale = locale
        if api_key == '':
            self.api_key = input('Enter API Key').strip()
        else:
            self.api_key = api_key

    def browse_routes(self, origin, destination, outbound_date, inbound_date):
        results = get_routes_cache(self.market, self.currency, self.locale, origin, destination, outbound_date,
                                   inbound_date, self.api_key)
        return results

    def browse_qoutes(self,origin,destination,outbound_date,inbound_date=''):
        results = get_quotes_cache(self.market,self.currency,self.locale,origin,destination,outbound_date,
                         inbound_date,self.api_key)
        return results

    def browse_cache_grid(self,origin,destination,outbound_date,inbound_date=''):
        results = get_cache_grid(self.market,self.currency,self.locale,origin,destination,outbound_date,
                                 inbound_date,self.api_key)
        return results

    def browse_dates(self,origin,destination,outbound_date,inbound_date=''):
        results = get_dates_cache(self.market,self.currency,self.locale,origin,destination,outbound_date,inbound_date,
                                  self.api_key)
        return results

