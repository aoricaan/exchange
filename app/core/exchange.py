import datetime

import requests
import xmltodict
from bs4 import BeautifulSoup

from app.core import ACCESS_KEY_FIXER, TOKEN_BMX
from app.models.exchange_model import Exchange, Rates


def get_value_from_dof():
    html = requests.get('https://www.banxico.org.mx/tipcamb/tipCamMIAction.do').text
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('body')[0].find_all('table')
    rows = tables[-2].find_all('tr')
    values = rows[2].find_all('td')
    values = [v.text.strip() for v in values]
    return {"diario_oficial_de_la_federacion": Exchange(
        last_updated=datetime.datetime.strptime(values[0], "%d/%m/%Y").isoformat(),
        value=float(values[-1])
    )}


def get_value_from_fixer():
    url = "http://data.fixer.io/api/latest"
    params = {"access_key": ACCESS_KEY_FIXER}
    response = requests.get(url, params=params).json()
    USD = response.get('rates', {}).get("USD")
    MXN = response.get('rates', {}).get("MXN")
    date = datetime.datetime.fromtimestamp(response.get('timestamp'))
    return {"fixer": Exchange(last_updated=date.isoformat(),
                              value=float(MXN / USD))}


def get_value_from_banxico():
    url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno'
    params = {"token": TOKEN_BMX}
    headers = {
        'Accept': 'application/xml',
        'Bmx-Token': TOKEN_BMX
    }
    response = requests.get(url, params=params, headers=headers)
    values = xmltodict.parse(response.text).get('series', {}).get('serie', {}).get('Obs', {})
    if not values:
        return None
    return {
        "banxico": Exchange(last_updated=datetime.datetime.strptime(values['fecha'], "%d/%m/%Y").isoformat(),
                            value=float(values['dato']))
    }


def exchange_rates_usd2mxn():
    rates = get_value_from_dof()
    rates.update(get_value_from_fixer())
    rates.update(get_value_from_banxico())
    return Rates(rates=rates)
