import requests
import asyncio
import sys
# from datetime import datetime
import json
import traceback
import time
import websocket
from PlvLogger import Logger
# import _thread
import threading
import hmac
import hashlib
import aiohttp


class GeneralBybit:
    _main_url = r'https://api.bybit.com'

    def _syns_request_template(self, end_point, par=None, method='get'):
        def_name = sys._getframe().f_code.co_name
        match method.lower():
            case 'get':
                req = requests.get(self._main_url + end_point, params=par)
            case 'post':
                req = requests.post(self._main_url + end_point, params=par)
            case 'delete':
                req = requests.delete(self._main_url + end_point, params=par)
            case _:
                mes_to_log = f'{def_name} {end_point} Неизвестный метод {method}'
                Logger('GeneralBybit', type_log='w').logger.error(mes_to_log)
                raise mes_to_log
        if not req.ok:
            mes_to_log = f'{def_name} {end_point} response status != 200'
            Logger(f'GeneralBybit', type_log='w').logger.error(mes_to_log)
            raise mes_to_log
        return req.json()

    async def _async_request_template(self, end_point, method, par):
        def_name = sys._getframe().f_code.co_name
        async with aiohttp.ClientSession() as session:
            if method == 'get':
                async with session.get(self._main_url + end_point, params=par) as response:
                    result = await response.json()
                    if isinstance(result, dict):
                        if result.get('retMsg') == 'OK':
                            if result.get('result'):
                                return result.get('result')
                            return result
                    mes_to_log = f'{def_name} {end_point} status: {result}'
                    Logger(f'GeneralBybit', type_log='w').logger.warning(mes_to_log)
                    return None


class SyncBybitPublic(GeneralBybit):
    def __init__(self, category):
        self.category = category
        self._logger = Logger(f'SyncBybitPublic', type_log='w').logger
        self.headers = {}

    def __setattr__(self, key, value):
        if key == 'category' and value not in ['spot', 'der', 'linear', 'inverse', 'option']:
            self._logger.error(f'Неизвестный тип рынка {self.category}')
            raise TypeError(f"Неверный category {self.category}")
        if key == 'category' and value == 'der':
            value = 'linear'
        object.__setattr__(self, key, value)

    def get_instruments_info(self):
        """
        https://bybit-exchange.github.io/docs/v5/market/instrument
        """
        end_point = '/v5/market/instruments-info'
        params = {
            'category': self.category,
            'status': 'Trading'
        }
        return self._syns_request_template(end_point=end_point, method='get', par=params)

    def get_symbols_in_trading(self):
        result = self.get_instruments_info().get('result')
        if result:
            return [el.get('symbol') for el in result.get('list') if el.get('status') == 'Trading']
        return None

    def get_ticker(self, symbol):
        """
            https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        end_point = '/v5/market/tickers'
        params = {
            'category': self.category,
            'symbol': symbol
        }
        return self._syns_request_template(end_point=end_point, method='get', par=params)


class AsyncBybitPublic(GeneralBybit):
    def __init__(self, category):
        self.category = category
        self._logger = Logger('AsyncBybitPublic', type_log='w').logger
        self.headers = {}

    def __setattr__(self, key, value):
        if key == 'category' and value not in ['spot', 'der', 'linear', 'inverse', 'option']:
            self._logger.error(f'Неизвестный тип рынка {self.category}')
            raise TypeError(f"Неверный category {self.category}")
        if key == 'category' and value == 'der':
            value = 'linear'
        object.__setattr__(self, key, value)

    async def get_instruments_info(self):
        """
        https://bybit-exchange.github.io/docs/v5/market/instrument
        """
        end_point = '/v5/market/instruments-info'
        params = {
            'category': self.category,
            'status': 'Trading'
        }
        return await self._async_request_template(end_point=end_point, method='get', par=params)

    async def get_ticker(self, symbol):
        """
            https://bybit-exchange.github.io/docs/v5/market/tickers
        """
        end_point = '/v5/market/tickers'
        params = {
            'category': self.category,
            'symbol': symbol
        }
        return await self._async_request_template(end_point=end_point, method='get', par=params)

    async def get_dict_tickers(self, lst_symbol):
        def_name = sys._getframe().f_code.co_name
        all_results = []
        for i in range(0, len(lst_symbol), 10):
            tasks = [asyncio.create_task(self.get_ticker(symbol)) for symbol in lst_symbol[i:i + 10]]
            try:
                done, _ = await asyncio.wait_for(asyncio.wait(tasks), 5)
                results = [task.result() for task in done if task.done()]
                all_results.extend(results)
            except asyncio.TimeoutError:
                mes_to_log = f"{def_name} Timeout for batch starting at index {i}"
                self._logger.error(mes_to_log)
                print(mes_to_log)
                raise mes_to_log
        dict_res = {}
        for coin in all_results:
            if coin.get('list'):
                dict_res[coin['list'][0]['symbol']] = coin['list'][0]['lastPrice']
            else:
                def_name = sys._getframe().f_code.co_name
                mes_to_log = f'{def_name} Ошибка запроса {coin}'
                self._logger.error(mes_to_log)
                raise mes_to_log
        return dict_res


class SyncBybitPrivate(GeneralBybit):
    def __init__(self, category, api_key, api_secret):
        self._logger = Logger('SyncBybitPrivate', type_log='w').logger
        self.category = category
        self.api_key = api_key
        self.api_secret = api_secret

    def __setattr__(self, key, value):
        if key == 'category' and value not in ['spot', 'linear', 'option']:
            raise TypeError(f"Неверный category {self.category}")
        if key == 'category' and value == 'der':
            value = 'linear'
        object.__setattr__(self, key, value)

    def __create_signature(self, params):
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        return hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    def get_wallet_balance(self, account_type='UNIFIED', coin=None):
        """
            https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        end_point = '/v5/account/wallet-balance'
        params = {
            'api_key': self.api_key,
            'timestamp': str(int(time.time() * 1000)),
            'accountType': account_type,
        }
        if coin:
            params['coin'] = coin
        params['sign'] = self.__create_signature(params)
        return self._syns_request_template(end_point=end_point, method='get', par=params)

    def get_transaction_log(self, start_time=None, end_time=None, account_type='UNIFIED', limit=20):
        """
           https://bybit-exchange.github.io/docs/v5/account/transaction-log
        """
        end_point = '/v5/account/transaction-log'
        params = {
            'api_key': self.api_key,
            'timestamp': str(int(time.time() * 1000)),
            'accountType': account_type,
            'category': self.category,
            'limit': limit
        }
        if start_time:
            params['startTime'] = start_time
        if end_time:
            params['endTime'] = end_time
        params['sign'] = self.__create_signature(params)
        return self._syns_request_template(end_point=end_point, method='get', par=params)


class AsyncBybitPrivate(GeneralBybit):
    def __init__(self, category, api_key, api_secret):
        self._logger = Logger('AsyncBybitPrivate', type_log='w').logger
        self.category = category
        self.api_key = api_key
        self.api_secret = api_secret

    def __setattr__(self, key, value):
        if key == 'category' and value not in ['spot', 'linear', 'option']:
            raise TypeError(f"Неверный category {self.category}")
        if key == 'category' and value == 'der':
            value = 'linear'
        object.__setattr__(self, key, value)

    def __create_signature(self, params):
        query_string = '&'.join([f"{key}={value}" for key, value in sorted(params.items())])
        return hmac.new(self.api_secret.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    async def get_account_info(self):
        """
            https://bybit-exchange.github.io/docs/v5/account/account-info
        """
        end_point = '/v5/account/info'
        params = {
            'api_key': self.api_key,
            'timestamp': str(int(time.time() * 1000)),
        }
        params['sign'] = self.__create_signature(params)
        return await self._async_request_template(end_point=end_point, method='get', par=params)

    async def get_wallet_balance(self, account_type='UNIFIED', coin=None):
        """
            https://bybit-exchange.github.io/docs/v5/account/wallet-balance
        """
        end_point = '/v5/account/wallet-balance'
        params = {
            'api_key': self.api_key,
            'timestamp': str(int(time.time() * 1000)),
            'accountType': account_type,
        }
        if coin:
            params['coin'] = coin
        params['sign'] = self.__create_signature(params)
        return await self._async_request_template(end_point=end_point, method='get', par=params)

    async def get_transaction_log(self, start_time=None, end_time=None, account_type='UNIFIED', limit=50):
        """
        https://bybit-exchange.github.io/docs/v5/account/transaction-log
        Получение лога транзакций с поддержкой пагинации.
        """
        end_point = '/v5/account/transaction-log'
        all_logs = []  # Список для сбора всех логов
        cursor = None  # Инициализация курсора для пагинации

        # Цикл для обработки пагинации
        while True:
            params = {
                'api_key': self.api_key,
                'timestamp': str(int(time.time() * 1000)),  # Генерируем новый timestamp для каждого запроса
                'accountType': account_type,
                'category': self.category,
                'limit': limit
            }

            if start_time:
                params['startTime'] = start_time
            if end_time:
                params['endTime'] = end_time
            if cursor:
                params['cursor'] = cursor

            params['sign'] = self.__create_signature(params)  # Генерируем новую подпись для каждого запроса

            response = await self._async_request_template(end_point=end_point, method='get', par=params)
            if response is None:
                break
            # Добавляем полученные логи в общий список
            all_logs.extend(response.get('list', []))
            # Обновляем курсор для следующего запроса
            cursor = response.get('nextPageCursor')
            if not cursor:
                break  # Выход из цикла, если больше нет страниц для загрузки
        return all_logs


# Websockets
class SyncBybitWebsocketPublic:
    _dict_urls = {
        'spot': 'wss://stream.bybit.com/v5/public/spot',
        'der': 'wss://stream.bybit.com/v5/public/linear',
        'der_auth': 'wss://stream.bybit.com/v5/private',
        'spot_auth': 'wss://stream.bybit.com/v5/private'
    }

    def __init__(self, trade_type, queue, topics):
        if trade_type not in self._dict_urls:
            raise ValueError(f"trade_type '{trade_type}' is not valid.")
        self.trade_type = trade_type
        self._logger = Logger('SyncBybitWebsocketPublic', type_log='w').logger
        self.queue = queue
        self.topics = topics
        self.websocket_app = None
        self.heartbeat_thread = None
        self._is_running = None
        self.reconnect_delay = 20  # Задержка перед повторным подключением
        self.count_reconnect = 0

        self.connect()

    def connect(self):
        self._is_running = True
        print('connect')
        self.websocket_app = websocket.WebSocketApp(
            url=self._dict_urls.get(self.trade_type),
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
            on_open=self.on_open,
        )
        self.websocket_app.run_forever()

    def __del__(self):
        self.stop()

    def send_heartbeat(self, _wsapp):
        while self._is_running:  # Проверьте, что соединение должно быть открыто
            try:
                if _wsapp.sock and _wsapp.sock.connected:  # Проверьте, что сокет существует и соединение открыто
                    _wsapp.send(json.dumps({"req_id": "100001", "op": "ping"}))
                else:
                    msg = "send_heartbeat, WebSocket is not connected."
                    self._logger.warning(msg)
                    print(msg)
                    break  # Выход из цикла, если соединение закрыто
                time.sleep(20)
            except websocket.WebSocketConnectionClosedException:
                msg = "WebSocket connection is closed, stopping heartbeat."
                self._logger.warning(msg)
                print(msg)
                break

    def on_open(self, _wsapp):
        print("Connection opened")
        self.heartbeat_thread = threading.Thread(target=self.send_heartbeat, args=(_wsapp,))
        self.heartbeat_thread.daemon = True
        self.heartbeat_thread.start()
        data = {
            "op": "subscribe",
            "args": self.topics
        }
        _wsapp.send(json.dumps(data))

    @staticmethod
    def on_close(_wsapp, close_status_code, close_msg):
        if close_status_code is not None and close_msg is not None:
            print(f"Close connection by server, status {close_status_code}, close message {close_msg}")

    def on_error(self, _wsapp, error):
        def_name = sys._getframe().f_code.co_name
        mes_to_log = f'{def_name} Error: {error}'
        # mes_to_log = f'{def_name} Error: {error}, traceback: {traceback.format_exc()}'
        self._logger.error(mes_to_log)
        print(mes_to_log)
        if self.count_reconnect <= 3:
            self.count_reconnect += 1
            self.reconnect()
        else:
            # self.queue.put('exit')
            exit()

    def reconnect(self):
        if self._is_running:
            mes_to_log = f'SyncBybitWebsocketPublic Reconnect {self.count_reconnect}'
            self._logger.warning(mes_to_log)
            print(mes_to_log)
            time.sleep(self.reconnect_delay)
            self.stop()
            self.connect()
        else:
            mes_to_log = f'reconnect not self._is_running'
            self._logger.error(mes_to_log)
            raise mes_to_log


    def stop(self):
        self._is_running = False
        if self.websocket_app:
            self.websocket_app.close()
        if self.heartbeat_thread or hasattr(self, 'heartbeat_thread'):
            self.heartbeat_thread.join()

    def on_message(self, _wsapp, message):
        parsed = json.loads(message)
        parsed['trade_type'] = self.trade_type
        print(len(parsed), parsed)
        self.queue.put(parsed)
