"""Bot payments of 0.5.0: BotClient helpers, error types, idempotency passthrough and the polling helper."""
import json
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root / 'python' if (project_root / 'python').is_dir() else project_root))
import nookara
from nookara import (APIError, BotClient, BuyerError, Client, InvalidBotToken, InvalidPaymentRequest, MerchantUnavailable,
                        NotCancellable, OrderConflict, PaymentError, PaymentInProgress, PaymentNotFound, PaymentRateLimited,
                        PaymentTimeout, is_paid)

PENDING = {'id': 'bpr_1', 'order_id': 'ord-1', 'amount': 20, 'status': 'pending', 'pay_url': 'https://velora.ikelene.net/pay/bp_x',
           'buyer': {'id': '260', 'username': 'alice'}}


class Handler(BaseHTTPRequestHandler):
    seen = []
    replies = []

    def log_message(self, *args):
        pass

    def handle_any(self):
        length = int(self.headers.get('Content-Length', 0))
        type(self).seen.append((self.command, self.path, dict(self.headers), self.rfile.read(length)))
        status, body = type(self).replies.pop(0) if type(self).replies else (200, {})
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())
    do_GET = do_POST = handle_any


class HttpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = 'http://127.0.0.1:%d' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def setUp(self):
        Handler.seen, Handler.replies = [], []
        self.bot = BotClient('BOTTOKEN', base_url=self.base, allow_insecure=True)

    def test_create_sends_bot_auth_and_body(self):
        Handler.replies = [(201, PENDING)]
        result = self.bot.create_payment_request('alice', 20, 'ord-1', description='Pack', return_url='https://shop.example/done',
                                                 expires_in=900, metadata='cart=7')
        method, path, headers, body = Handler.seen[0]
        self.assertEqual((method, path), ('POST', '/bot/payment-requests'))
        self.assertEqual(headers['Authorization'], 'Bot BOTTOKEN')
        self.assertEqual(json.loads(body), {'buyer': 'alice', 'amount': 20, 'order_id': 'ord-1', 'description': 'Pack',
                                            'return_url': 'https://shop.example/done', 'expires_in': 900, 'metadata': 'cart=7'})
        self.assertEqual(result['pay_url'], PENDING['pay_url'])

    def test_optional_fields_are_left_out(self):
        Handler.replies = [(201, PENDING)]
        self.bot.create_payment_request(260, 5, 'o')
        self.assertEqual(json.loads(Handler.seen[0][3]), {'buyer': '260', 'amount': 5, 'order_id': 'o'})

    def test_idempotent_replay_is_returned_as_is(self):
        Handler.replies = [(200, dict(PENDING, idempotent_replay=True))]
        self.assertTrue(self.bot.create_payment_request('alice', 20, 'ord-1')['idempotent_replay'])

    def test_get_find_list_cancel_paths(self):
        Handler.replies = [(200, PENDING), (200, PENDING), (200, {'requests': [PENDING]}), (200, dict(PENDING, status='cancelled'))]
        self.assertEqual(self.bot.get_payment_request('bpr_1')['id'], 'bpr_1')
        self.assertEqual(self.bot.find_payment_request('ord 1/x')['order_id'], 'ord-1')
        self.assertEqual(self.bot.list_payment_requests('paid', limit=5), [PENDING])
        self.assertEqual(self.bot.cancel_payment_request('bpr_1')['status'], 'cancelled')
        paths = [(m, p) for m, p, _, _ in Handler.seen]
        self.assertEqual(paths, [('GET', '/bot/payment-requests/bpr_1'), ('GET', '/bot/payment-requests?order_id=ord+1%2Fx'),
                                 ('GET', '/bot/payment-requests?status=paid&limit=5'), ('POST', '/bot/payment-requests/bpr_1/cancel')])

    def test_find_returns_none_when_unknown(self):
        Handler.replies = [(404, {'error': 'not_found'})]
        self.assertIsNone(self.bot.find_payment_request('nope'))

    def test_error_codes_map_to_types(self):
        cases = [(401, 'invalid_bot_token', InvalidBotToken), (403, 'merchant_unavailable', MerchantUnavailable),
                 (403, 'bot_banned', MerchantUnavailable), (400, 'invalid_amount', InvalidPaymentRequest),
                 (400, 'invalid_return_url', InvalidPaymentRequest), (404, 'buyer_not_found', BuyerError),
                 (400, 'buyer_is_bot', BuyerError), (400, 'self_payment', BuyerError), (403, 'buyer_restricted', BuyerError),
                 (409, 'order_id_conflict', OrderConflict), (409, 'payment_in_progress', PaymentInProgress),
                 (409, 'not_cancellable', NotCancellable), (404, 'not_found', PaymentNotFound),
                 (429, 'too_many_open_requests', PaymentRateLimited), (429, 'something_new', PaymentRateLimited),
                 (500, 'boom', PaymentError)]
        for status, code, cls in cases:
            Handler.replies = [(status, {'error': code, 'min': 1, 'max': 10000})]
            with self.assertRaises(cls) as caught:
                self.bot.create_payment_request('alice', 20, 'ord-1')
            self.assertIsInstance(caught.exception, APIError)
            self.assertEqual((caught.exception.status, caught.exception.error), (status, code))
        self.assertEqual(caught.exception.payload['max'], 10000)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.bot = BotClient('T')

    def test_local_validation_before_any_request(self):
        with patch.object(Client, 'request') as request:
            for args in [('alice', 0, 'o'), ('alice', 1.5, 'o'), ('alice', True, 'o'), ('alice', 5, 'has space'), ('alice', 5, ''),
                         ('alice', 5, 'x' * 101), ('', 5, 'o'), (None, 5, 'o')]:
                with self.assertRaises(ValueError):
                    self.bot.create_payment_request(*args)
            with self.assertRaises(ValueError):
                self.bot.get_payment_request('../x')
            with self.assertRaises(ValueError):
                self.bot.list_payment_requests('refunded')
            request.assert_not_called()

    def test_bot_client_basics(self):
        with self.assertRaises(ValueError):
            BotClient('')
        self.assertEqual(self.bot.auth_scheme, 'Bot')
        self.assertNotIn('T', repr(self.bot).replace('BotClient', ''))
        self.assertIs(nookara.BotClient, BotClient)

    def test_is_paid(self):
        self.assertTrue(is_paid({'status': 'paid'}))
        self.assertFalse(is_paid({'status': 'pending'}))
        self.assertFalse(is_paid(None))

    def test_generated_endpoint_methods_exist(self):
        for name in ('post_bot_payment_requests', 'get_bot_payment_requests', 'get_bot_payment_requests_by_id',
                     'post_bot_payment_requests_by_id_cancel'):
            self.assertTrue(hasattr(self.bot, name), name)


class WaitTests(unittest.TestCase):
    def setUp(self):
        self.bot = BotClient('T')
        self.now = [0.0]
        self.sleeps = []

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now[0] += seconds

    def wait(self, replies, **kwargs):
        with patch.object(Client, 'request', side_effect=replies):
            return self.bot.wait_for_payment('bpr_1', sleep=self.sleep, clock=lambda: self.now[0], **kwargs)

    def test_returns_when_paid(self):
        paid = dict(PENDING, status='paid', transaction_id='9')
        result = self.wait([PENDING, PENDING, paid], timeout=100, poll=2)
        self.assertEqual(result['transaction_id'], '9')
        self.assertEqual(len(self.sleeps), 2)
        self.assertGreater(self.sleeps[1], self.sleeps[0])

    def test_returns_other_final_states_without_raising(self):
        for status in ('declined', 'expired', 'cancelled'):
            self.assertEqual(self.wait([dict(PENDING, status=status)])['status'], status)

    def test_timeout_carries_last_request(self):
        with self.assertRaises(PaymentTimeout) as caught:
            self.wait([PENDING] * 50, timeout=10, poll=3)
        self.assertEqual(caught.exception.request['status'], 'pending')
        self.assertLessEqual(self.now[0], 10)

    def test_rate_limit_backs_off_and_continues(self):
        limited = APIError(429, {'error': 'rate_limited', 'retry_after': 7})
        replies = [nookara.botpayments.payment_error(limited), dict(PENDING, status='paid')]
        self.assertTrue(is_paid(self.wait(replies, timeout=100, poll=1)))
        self.assertEqual(self.sleeps[0], 7)

    def test_other_errors_propagate(self):
        with self.assertRaises(InvalidBotToken):
            self.wait([nookara.botpayments.payment_error(APIError(401, {'error': 'invalid_bot_token'}))])


if __name__ == '__main__':
    unittest.main()
