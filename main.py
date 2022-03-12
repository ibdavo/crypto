from ast import Try
from logging import exception
import ccxt
import config

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
        try:
            exchange = determine_account(data)
            print('remove me')
            return_response('success', "test_account", 'Account test!')
        except Exception as e:
            return return_response('error', str(e), "Determine account failed")

        test_binance(exchange)
        return return_response('success', 'account determined')
        # return get_account_balance()
        # return get_accounts()
        # return test_binance()
        # print(binance)

        # return get_account_balance()

    except Exception as e:
        return return_response('error', str(e), 'Error in request params')

def determine_account(data):
    if 'account' not in data.keys():
        raise Exception('Account info missing or invalid.')
    if 'exchange' not in data.keys():
        raise Exception('Exchange info missing or invalid')
    if 'account_type' not in data.keys():
        raise Exception('Account info missing or invalid')
    print("Account: {}".format(data['account'])) 
    # print(config.accounts[data['account']])

    # Account
    if config.accounts[data['account']] is None:
        raise Exception('Invalid account')
    # Exchange
    if config.accounts[data['account']][data['exchange']] is None:
        raise Exception('Account exchange is missing of invalid')
    # Account Type
    if config.accounts[data['account']][data['exchange']][data['account_type']] is None:
        raise Exception('Account exchange account_type is missing of invalid')

    # api_key = config.accounts[data['account']][data['exchange']][data['account_type']][data["api_key"]]
    # secret = config.accounts[data['account']][data['exchange']][data['account_type']][data["secret"]]

    print(config.accounts[data['account']][data['exchange']][data['account_type']]['api_key'])
    print(config.accounts[data['account']][data['exchange']][data['account_type']]['api_key'])
    # print('secret: ' + secret)
    if 'binanceus' in config.accounts[data['account']]: 
        print("binance us...")
    # if config.accounts[data['account']][data['exchange']] == 'binanceus':
        try: 
            exchange = ccxt.binanceus({
                'apiKey' : config.accounts[data['account']][data['exchange']][data['account_type']]['api_key'],
                'secret': config.accounts[data['account']][data['exchange']][data['account_type']]['secret'],
            })
            
        except Exception as e:
            return return_response('error', str(e), 'Exchange init failed.')
    else:
        raise Exception('Unknown exchange')

    print("exchange:")    
    return exchange
    

def order(exchange):
    try:
        limit_order = exchange.create_limit_buy_order(
            'ETH/BTC', '0.01', '0.014')
        
        return {
            'status': 'success',
            'message': 'order placed',
        }
    except Exception as e:
        return return_response('error', str(e), 'Order error')

# def get_account_balance():  # TODO pass exchange?
#     try:
#         exchange = ccxt.binanceus({
#             'apiKey' : config.API_KEY_BINANCE,
#             'secret': config.SECRET_KEY_BINANCE,
#         })

#         account_balance = exchange.fetch_balance()  # binance.fetch_balance()
#         # print('### balance ' + account_balance)
#         for balance in account_balance:
#             print(balance)
#         return {
#             'status': 'success',
#             'message': account_balance,
#             'comments': 'balance retrieved'
#         }
#     except Exception as e:
#         return return_response('error', str(e), 'Account balance error.')

# def get_accounts():
#     try:
#         exchange = ccxt.binanceus({
#             'apiKey' : config.API_KEY_BINANCE,
#             'secret': config.SECRET_KEY_BINANCE,
#         })

#         accounts = exchange.account()
#         # balance = exchange.fetch_balance()
#         print(accounts)
#         return return_response('success', accounts, 'account status')
#     except Exception as e:
#         return return_response('error', str(e))


def test_binance(exchange):
    # Test exchange info
    # for exchange in ccxt.exchanges:
    #     print(exchange)

    # exchange_binance = ccxt.binance()
    # exchange_binance.set_sandbox_mode(True)  # SANDBOX MODE
    # exchange_coinbasepro = ccxt.coinbasepro()

    markets = exchange.load_markets()
    for market in markets:
        if 'BTC' in market:
            print(market)

    ohlc_binance = exchange.fetch_ohlcv(
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

def return_response(status, msg, comments = ''):
    return {
        'status' : status,
        'message': msg,
        'comments' : comments
    }

# https://testnet.binance.vision/ paper trading
# https://algotrading101.com/learn/binance-python-api-guide/
# ccxt
#   https://docs.ccxt.com/en/latest/manual.html
#   https://github.com/ccxt/ccxt/tree/master/python
#   https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076

# https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py


# [] TODO use shrimpy to link accounts? https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076
