import requests
import json
import datetime
import sys
import pandas as pd
from geopy.distance import geodesic

import config


def get_country_data(region='europe'):
    r = requests.get(f'{config.url_countries_base}/region/{region}')
    if r.status_code != 200:
        sys.exit("Error while connecting to REST Countries API")
    else:
        country_data = json.loads(r.text)
        return country_data


def get_ex_rates_data(cur_code):
    r = requests.get(f'{config.url_currencies_base}/exchange-rates?currency={cur_code}')
    if r.status_code != 200:
        sys.exit("Error while connecting to Coinbase Digital Currency API")
    else:
        currency_data = json.loads(r.text)
        return currency_data


def get_country_name(country):
    return country['name']


def get_native_name(country):
    return country['nativeName']


def get_country_code(country):
    return country['alpha2Code']


def get_area(country):
    return country['area']


def get_population(country):
    return country['population']


def get_capital(country):
    return country['capital']


def get_official_language(country):
    languages = country['languages']
    languages_list = []
    for lang in languages:
        languages_list.append(lang['name'])
    return "|".join(languages_list)


def get_domain_name(country):
    list_of_domains = country['topLevelDomain']
    if '' in list_of_domains:
        return "N/A"
    else:
        return "|".join(list_of_domains)


def get_timezones(country):
    list_of_timezones = country['timezones']
    return "|".join(list_of_timezones)


def is_in_regional_block(country):
    list_of_blocks = country['regionalBlocs']
    acronyms_list = []
    for blocks in list_of_blocks:
        acronyms_list.append(blocks['acronym'])

    if config.regional_block in acronyms_list:
        return "Y"
    else:
        return "N"


def get_country_to_compare(countries, to_compare="Poland"):
    for country in countries:
        if get_country_name(country) == to_compare:
            return country


def get_distance(country, to_compare):
    origin = tuple(to_compare['latlng'])
    distance = tuple(country['latlng'])
    return round(geodesic(origin, distance).kilometers, 2)


def currency_symbol(country):
    currencies = country['currencies']
    currency_symbols = []
    for cur in currencies:
        if cur['symbol'] is not None:
            currency_symbols.append(cur['symbol'])
        else:
            currency_symbols.append("N/A")
    return "|".join(currency_symbols)


def currency_name(country):
    currencies = country['currencies']
    currency_names = []
    for cur in currencies:
        if cur['name'] is not None:
            currency_names.append(cur['name'])
        else:
            currency_names.append("N/A")
    return "|".join(currency_names)


def get_currency_codes(country):
    currencies = country['currencies']
    currency_codes = []
    for cur in currencies:
        currency_codes.append(cur['code'])
    return currency_codes


def get_exchange_rate(ex_rates, to_cur):
    if to_cur not in ex_rates['data']['rates'].keys():
        return "N/A"
    else:
        ex_rate = round(1/float(ex_rates['data']['rates'][to_cur]), 4)
        return str(ex_rate)


result_countries = []
current_time = datetime.datetime.now()

list_of_countries = get_country_data(config.region)
ex_rates = get_ex_rates_data(config.currency_ex_rates)
country_to_compare = get_country_to_compare(list_of_countries, config.country_to_compare)

for country in list_of_countries:
    currency_codes = get_currency_codes(country)
    rates = []

    for code in currency_codes:
        rates.append(get_exchange_rate(ex_rates, code))

    country_dict = {
        'country_name': get_country_name(country),
        'country_name_native': get_native_name(country),
        'country_code': get_country_code(country),
        'area': get_area(country),
        'population': get_population(country),
        'capital': get_capital(country),
        'official_language': get_official_language(country),
        'domain': get_domain_name(country),
        'timezone': get_timezones(country),
        f'{config.regional_block}_member': is_in_regional_block(country),
        f'distance_km_to_{config.country_to_compare}': get_distance(country, country_to_compare),
        'currency_symbol': currency_symbol(country),
        'currency_name': currency_name(country),
        f'{config.currency_ex_rates}_exchange_rate': "|".join(rates),
        'time_generated': current_time
    }

    result_countries.append(country_dict)

df = pd.DataFrame(result_countries)
df.to_csv('countries_info.csv', index=False)
