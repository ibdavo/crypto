from logging import exception
import ccxt
import config

# Binance
exchange_id = 'binance'
exchange_class = getattr(ccxt, exchange_id)
exchange = exchange_class({
    'apiKey': 'YY7esBK7WgJcnbHZB4E9lFaruKgPaBvJNCMZOYvtNveRMWiaaiFu4UvukYm5w4cc',
    'secret': 'XkMoQMP74FSFjbysonVqeGhS5Ruf0xkuo29sd3UH8V7WkvbdgHUjdWR0E118QUXV',
    'timeout': 30000,
    'enableRateLimite': True,
})

# API Key: YY7esBK7WgJcnbHZB4E9lFaruKgPaBvJNCMZOYvtNveRMWiaaiFu4UvukYm5w4cc
# Secret Key: XkMoQMP74FSFjbysonVqeGhS5Ruf0xkuo29sd3UH8V7WkvbdgHUjdWR0E118QUXV


def trade(request):
    try:
        # get data
        if request.args:
            data = request.args  # data is in query string params
            print('args input ...')
        else:
            data = request.json  # data is in body
            print('json input... ')  # +  json.dumps(data))

        if data is None:
            raise Exception('Request rejected, empty request.')

        return test_binance()
        # print(binance)

        # return get_account_balance()

    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'comments': '### Error in request params.'
        }


def order():
    try:
        limit_order = exchange.create_limit_buy_order(
            'ETH/BTC', '0.01', '0.014')
        return {
            'status': 'success',
            'message': 'order placed',
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'comments': '### Order error.'
        }


def get_account_balance():  # TODO pass exchange?
    try:
        account_balance = exchange.fetch_balance()  # binance.fetch_balance()
        # print('### balance ' + account_balance)
        return {
            'status': 'success',
            'message': account_balance,
            'comments': 'balance retrieved'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'comments': 'Account balance error.'
        }


def test_binance():
    # Test exchange info
    # for exchange in ccxt.exchanges:
    #     print(exchange)

    exchange_binance = ccxt.binance()
    # exchange_binance.set_sandbox_mode(True)  # SANDBOX MODE
    exchange_coinbasepro = ccxt.coinbasepro()

    markets = exchange_binance.load_markets()
    for market in markets:
        if 'BTC' in market:
            print(market)

    ohlc_binance = exchange_binance.fetch_ohlcv(
        'BTC/USDT', timeframe='1m', limit=5)
    for candle in ohlc_binance:
        print(candle)
    # unixtimestamp.com
    # ticker_binance = exchange_binance.fetch_ticker('BTC/USDT')
    # ticker_coinbase = exchange_coinbase.fetch_ticker('BTC/USD')
    # print(ticker_binance)
    # print(ticker_coinbase)

    # markets = exchange_binance.load_markets()
    # for market in markets:
    #     print(market)

    return {
        'status': 'test'
    }

# https://testnet.binance.vision/ paper trading
# https://algotrading101.com/learn/binance-python-api-guide/
# ccxt
#   https://docs.ccxt.com/en/latest/manual.html
#   https://github.com/ccxt/ccxt/tree/master/python
#   https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076

# https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py


# [] TODO use shrimpy to link accounts? https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076
