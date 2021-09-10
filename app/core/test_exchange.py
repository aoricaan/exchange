from unittest import TestCase, mock

from app.core.exchange import get_value_from_dof, get_value_from_fixer, get_value_from_banxico, exchange_rates_usd2mxn
from app.models.exchange_model import Exchange, Rates

with open('metadata/dof_mock.html', 'r') as f:
    DOF_MOCK = type('response', (), {
        "text": f.read()
    })

with open('metadata/banxico_mock.xml', 'r') as f:
    BANXICO_MOCK = type('response', (), {
        "text": f.read()
    })

FIXER_MOCK = type('response', (), {
    'json': lambda: {'success': True, 'timestamp': 1631249343, 'base': 'EUR', 'date': '2021-09-10',
                     'rates': {'USD': 1.182949, 'MXN': 23.556537}}})


def mock_exchange(url, *_, **__):
    if url == 'https://www.banxico.org.mx/tipcamb/tipCamMIAction.do':
        return DOF_MOCK
    elif url == 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/oportuno':
        return BANXICO_MOCK
    return FIXER_MOCK


class Test(TestCase):

    @mock.patch('requests.get', side_effect=lambda *_, **__: DOF_MOCK)
    def test_get_value_from_dof(self, *_):
        response = get_value_from_dof()
        self.assertEqual(response, {
            'diario_oficial_de_la_federacion': Exchange(last_updated='2021-09-10T00:00:00', value=19.9383)})

    @mock.patch('requests.get', side_effect=lambda *_, **__: FIXER_MOCK)
    def test_get_value_from_fixer(self, *_):
        response = get_value_from_fixer()
        self.assertEqual(response, {'fixer': Exchange(last_updated='2021-09-09T23:49:03', value=19.913400324105265)})

    @mock.patch('requests.get', side_effect=lambda *_, **__: BANXICO_MOCK)
    def test_get_value_from_banxico(self, *_):
        response = get_value_from_banxico()
        self.assertEqual(response, {'banxico': Exchange(last_updated='2021-09-09T00:00:00', value=19.9318)})

    @mock.patch('requests.get', side_effect=mock_exchange)
    def test_exchange_rates_usd2mxn(self, *_):
        response = exchange_rates_usd2mxn()
        self.assertEqual(response,
                         Rates(rates={'diario_oficial_de_la_federacion': Exchange(last_updated='2021-09-10T00:00:00',
                                                                                  value=19.9383),
                                      'fixer': Exchange(last_updated='2021-09-09T23:49:03', value=19.913400324105265),
                                      'banxico': Exchange(last_updated='2021-09-09T00:00:00', value=19.9318)}))
