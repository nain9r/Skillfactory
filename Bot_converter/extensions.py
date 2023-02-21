import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, sym, amount):
        base_key = exchanges[base]
        sym_key = exchanges[sym]
        amount = float(amount)

        if base_key == sym_key:
            raise APIException(f'Вы пытаетесь конвертировать {base} в {base}!')

        r = requests.get(f'https://anyapi.io/api/v1/exchange/convert?base={base_key}&to={sym_key}&amount={amount}'
                         f'&apiKey=jpe1gbfg5hodnpsds3n4lgeu35u22ju0o60q84l425k8bcjm4e9b75g')
        resp = json.loads(r.content)
        price = resp['rate'] * amount
        price = round(price, 3)
        message = f" {amount} {base} в {sym} : {price} "
        return message
