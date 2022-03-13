# from ast import Try
from logging import exception
import ccxt
import json
import config
# https://docs.ccxt.com/en/latest/manual.html

# TODO parameters
#   [x] symbol
#   [x] side
#   [x] % profit
#   [x] stop_loss
#   [x] quantity OR
#   [] % equity OR
#   [] % fiat_amt
#   [] pass phrase / password
#   [] demo trade & set_sandbox_mode
# [] VALIDATE EXCHANGE passed, just after validate data
# TODO order()
#   [] single line json
#   [] add cryptopro with single line json
# [] TODO use shrimpy to link accounts? https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076


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

        # Validate data
        try:
            validate_data()
        except Exception as e:
            return_response('error', str(e), 'data validation failed.')

        # Connect Exchange
        try:
            exchange = connect_exchange(data)

        except Exception as e:
            return return_response('error', str(e), "Determine account failed")
        print("version: {}".format(ccxt.__version__))
        # return fetch_balance(exchange)
        return order(exchange, data)
        # print("test order...")
        # order(exchange, data)
        # print('list ohlc...')
        # list_ohlc(exchange)
        # print('test balance...')
        # return order(exchange)
        # return get_account_balance()
        # return test_binance()

    except Exception as e:
        print('### error in request params: {}'.format(str(e)))
        return return_response('error', str(e), 'Error in request params')


def validate_data(data):
    if 'account' not in data.keys():
        raise Exception('Account info missing or invalid.')
    if 'exchange' not in data.keys():
        raise Exception('Exchange info missing or invalid')
    if 'account_type' not in data.keys():
        raise Exception('Account info missing or invalid')
    print("Account: {}".format(data['account']))  # REMOVE ME
    print("Scan account info...")
    # Scan accounts....
    # Account
    if config.accounts[data['account']] is None:
        raise Exception('Invalid account')
    # Exchange
    if config.accounts[data['account']][data['exchange']] is None:
        raise Exception('Account exchange is missing of invalid')
    # Account Type
    if config.accounts[data['account']][data['exchange']][data['account_type']] is None:
        raise Exception('Account exchange account_type is missing of invalid')
    if 'symbol' not in data.keys():
        raise Exception('Symbol not specified')
    if 'price' not in data.keys():
        raise Exception('Price not specified')
    if 'pct_profit' not in data.keys():
        raise Exception('percent profit not specified')
    if 'stop_loss' not in data.keys():
        raise Exception('stop_loss not specified')
    if 'side' not in data.keys():
        raise Exception('side (buy/sell) not specified')


def connect_exchange(data):
    try:
        json_data = {
            'apiKey': config.accounts[data['account']][data['exchange']][data['account_type']]['api_key'],
            'secret': config.accounts[data['account']][data['exchange']][data['account_type']]['secret'],
        }
        if 'binanceus' in config.accounts[data['account']]:
            print("binance us...")
            exchange = ccxt.binanceus(json_data)
        elif 'coinbasepro' in config.accounts[data['account']]:
            print("Coinbase Pro ...")
            exchange = ccxt.coinbasepro(json_data)
        else:
            raise Exception('Unknown exchange')
        print("exchange connected...")
    except Exception as e:
        return return_response('error', str(e), 'Account determination failed.')
    return exchange


def fetch_balance(exchange):
    print("### remove me - sandbox activated.")
    exchange.set_sandbox_mode = True

    try:
        balance = exchange.fetchBalance()
        # print(balance)
        print('balance retrieved')
        return return_response('success', balance, 'balanced retrieved')
    except Exception as e:
        print('error in balance ' + str(e))
        return return_response('error', str(e), 'Account balance failed')


def order(exchange, data):
    print("order...")
    try:
        # build order vars
        if 'qty' in data.keys():
            qty = float(data['qty'])
        else:
            qty = 0
        symbol = data['symbol']
        # exchange.market(symbol)
        exchange.load_markets()
        side = data['side']
        price = float(data['price'])
        print("price " + str(price))
        pct_profit = (float(data['pct_profit']) / 100)
        stop_loss = (float(data['stop_loss']) / 100)
        if side.lower() == 'buy':  # TODO ternary
            pct_profit = float(1 + pct_profit)
            stop_loss = float(1 - stop_loss)
        else:
            pct_profit = float(1 - pct_profit)
            stop_loss = float(1 + stop_loss)

        print("setting params <test> ...")
        params = {
            'test': True,  # test if it's valid, but don't actually place it
        }        # Build order
        print("build json...")
        json_order = {
            'symbol': symbol,
            'side': side,
            'quantity': exchange.amount_to_precision(data['symbol'], qty),
            'price': price,  # exchange.price_to_precision(symbol, price),
            'stopPrice': exchange.price_to_precision(symbol, price * pct_profit),
            'stopLimitPrice': exchange.price_to_precision(symbol, price * stop_loss),
            'stopLimitTimeInForce': 'GTC',
        }
        # If provided, stopLimitTimeInForce is required
        # 'listClientOrderId': exchange.uuid(),  # A unique Id for the entire orderList
        # 'limitClientOrderId': exchange.uuid(),  # A unique Id for the limit order
        # 'limitIcebergQty': exchangea.amount_to_precision(symbol, limit_iceberg_quantity),
        # 'stopClientOrderId': exchange.uuid()  # A unique Id for the stop loss/stop loss limit leg
        # 'stopIcebergQty': exchange.amount_to_precision(symbol, stop_iceberg_quantity),
        # 'newOrderRespType': 'ACK',  # ACK, RESULT, FULL

        # Transmit order
        print("JSON Order: {}".format(json.dumps(json_order)))

        # params = {
        #     'test': True,
        #     'stopPrice': exchange.price_to_precision(symbol, price * pct_profit),
        #     'type': 'stopLimit'
        # }

        # order = exchange.create_order(
        #     symbol=symbol, type='STOP_LOSS_LIMIT', side=side, amount=qty, price=price, params=params)

        order = exchange.private_post_order_oco(json_order)
        # order = exchange.create_market_sell_order(symbol, .001)
        print('order response...')
        print(order)
        # limit_order = exchange.create_limit_buy_order(
        #     'ETH/BTC', '0.01', '0.014')

        return {
            'status': 'success',
            'message': 'order placed',
        }
    except Exception as e:
        print('### order error: {}'.format(str(e)))
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


def list_ohlc(exchange):
    # Test exchange info
    # for exchange in ccxt.exchanges:
    #     print(exchange)

    # exchange_binance = ccxt.binance()
    # exchange_binance.set_sandbox_mode(True)  # SANDBOX MODE
    # exchange_coinbasepro = ccxt.coinbasepro()

    # markets = exchange.load_markets()
    # print(markets)
    # for market in markets:
    #     if 'ETH' in market:
    #         print(market)
    # print 5 last prices
    ohlc_binance = exchange.fetch_ohlcv(
        'ETH/USDT', timeframe='1m', limit=5)
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


def return_response(status, msg, comments=''):
    return {
        'status': status,
        'message': msg,
        'comments': comments
    }


# https://testnet.binance.vision/ paper trading
# https://www.cryptomaton.org/2021/05/08/how-to-code-a-binance-trading-bot-that-detects-the-most-volatile-coins-on-binance/
# https://algotrading101.com/learn/binance-python-api-guide/
# ccxt
#   https://docs.ccxt.com/en/latest/manual.html
#   https://github.com/ccxt/ccxt/tree/master/python
#   https://medium.com/coinmonks/ccxt-cryptocurrency-trading-limit-orders-and-market-orders-tutorial-26a5697fe076

# https://github.com/binance/binance-signature-examples/blob/master/python/spot/spot.py
