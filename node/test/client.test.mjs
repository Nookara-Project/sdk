import test, { before, after } from 'node:test';
import assert from 'node:assert';
import http from 'node:http';
import { createRequire } from 'node:module';
import { createHash } from 'node:crypto';
import { startAppLinkLogin, shown_name, personal_sticker_text, parse_personal_sticker, Client, APIError, ScopeError, TransportError, ROUTES, SCOPES, scope_mask, scope_names, has_scope, VERSION, ember_permission_mask, ember_permission_names, has_ember_permission, EMBER_PERMISSIONS, EMBER_ALL_PERMISSIONS } from '../dist/index.mjs';

let server, base, last;
const STK = { sid: 's0123456789', name: 'wave', animated: false, url: 'https://nookara.cc/uploads/stickers/s0123456789.png', send: 'https://nookara.cc/uploads/stickers/s0123456789.png#wave', created_at: 1 };
const pkce = {};
const require_hash = v => createHash('sha256').update(String(v)).digest('base64url');
before(async () => {
  server = http.createServer((req, res) => {
    const chunks = [];
    req.on('data', c => chunks.push(c));
    req.on('end', () => {
      last = { method: req.method, url: req.url, headers: req.headers, body: Buffer.concat(chunks) };
      const send = (code, obj, headers = {}) => { res.writeHead(code, { 'content-type': 'application/json', ...headers }); res.end(JSON.stringify(obj)); };
      if (req.url.startsWith('/boom')) { res.writeHead(500); return res.end('<html>'); }
      if (req.url.startsWith('/redirect')) { res.writeHead(302, { location: 'http://example.test/' }); return res.end(); }
      if (req.url.startsWith('/scope')) return send(403, { error: 'insufficient_scope', required_scope: SCOPES.CHAT });
      if (req.url.startsWith('/limited')) return send(429, { error: 'rate_limited' }, { 'retry-after': '7' });
      if (req.url.startsWith('/text')) { res.writeHead(200, { 'content-type': 'text/plain' }); return res.end('hi'); }
      if (req.url.startsWith('/empty')) { res.writeHead(204); return res.end(); }
      if (req.url === '/auth/ext-code') return send(200, { code: 'c0de' });
      if (req.url.startsWith('/chat/clone-check')) return send(200, { locked: req.url.includes(createHash('sha256').update('locked').digest('hex')), auth: req.headers.authorization || null });
      if (req.url === '/chat/personal-emojis') return send(200, req.method === 'GET' ? { emojis: [], max: 25, pro_max: 100 } : { emoji: { eid: 'e0123456789', name: 'wave' } });
      if (req.url === '/chat/personal-stickers') return send(200, req.method === 'GET' ? { stickers: [STK], max: 10, pro_max: 50 } : { sticker: STK });
      if (req.url === `/chat/personal-stickers/${STK.sid}/info`) return send(200, { sticker: STK, owner: { username: 'nat', pfp: null } });
      if (req.url === `/chat/personal-stickers/${STK.sid}`) return send(200, { ok: true });
      if (req.url === '/account/me') return send(200, { account: { username: 'nat', display_name: 'Nat' } });
      if (req.url === '/account/update') { let b = {}; try { b = JSON.parse(last.body); } catch {} return b.display_name === 'Nookara' ? send(400, { error: 'display_name_reserved' }) : send(200, { success: true, display_name: b.display_name }); }
      let xb = {}; try { xb = JSON.parse(last.body); } catch {}
      if (req.url === '/auth/ext-code/exchange' && xb.code === 'c0de') { const b = xb; const ok = b.code === 'c0de' && b.grant === 'g'.repeat(32) && require_hash(b.code_verifier) === pkce.challenge; return ok ? send(200, { token: 'apptok', scopes: 5 }) : send(403, { error: 'bad_code_verifier' }); }
      send(200, { ok: true, product: { id: 'p' }, products: [1] });
    });
  });
  await new Promise(r => server.listen(0, '127.0.0.1', r));
  base = `http://127.0.0.1:${server.address().port}`;
});
after(() => server.close());
const client = (token = 'tok', opts = {}) => new Client(token, { baseUrl: base, allowInsecure: true, ...opts });

test('every route is a method, and every path parameter fills in', async () => {
  assert.ok(Object.keys(ROUTES).length > 500);
  const c = client();
  for (const [id, [method, tpl, auth, params]] of Object.entries(ROUTES)) {
    assert.equal(typeof c[id], 'function', id);
    const args = Object.fromEntries(params.map(p => [p[0], 'x y']));
    const scheme = auth === 'bot' ? client('t', { authScheme: 'Bot' }) : c;
    await scheme[id](args);
    assert.equal(last.method, method, id);
    assert.ok(!last.url.includes('/:'), `${id}: ${last.url}`);
    if (params.length && params.some(p => !p[1])) assert.ok(last.url.includes('x%20y'), `${id}: ${last.url}`);
  }
});
test('method names match the catalogue the Python SDK uses', async () => {
  const { readFile } = await import('node:fs/promises');
  const cat = JSON.parse(await readFile(new URL('../catalogue/catalogue.json', import.meta.url), 'utf8'));
  const want = cat.routes.filter(r => !r.staffOnly && r.group !== 'staff' && r.group !== 'maintenance').map(r => r.operationId).sort();
  assert.deepEqual(Object.keys(ROUTES).sort(), want);
  for (const name of ['post_checkout_direct', 'get_purchases', 'get_my_reports', 'get_drive_api_items', 'get_forums_api_home', 'get_devices', 'get_apps', 'get_account_dm_requests', 'get_products_sales']) assert.ok(ROUTES[name], name);
});
test('auth, query and json', async () => {
  const c = client();
  await c.request('POST', '/x', { query: { a: 1, b: null, c: [2, 3], d: true }, json: { é: 1 } });
  assert.equal(last.url, '/x?a=1&c=2&c=3&d=true');
  assert.equal(last.headers.authorization, 'Bearer tok');
  assert.equal(last.headers['content-type'], 'application/json');
  assert.equal(last.headers['user-agent'], `nookara-node/${VERSION}`);
  assert.deepEqual(JSON.parse(last.body), { é: 1 });
  await client('bot', { authScheme: 'Bot' }).request('GET', '/x');
  assert.equal(last.headers.authorization, 'Bot bot');
  await client(null).request('GET', '/x');
  assert.equal(last.headers.authorization, undefined);
  await client('t', { origin: 'https://app.test' }).request('GET', '/x');
  assert.equal(last.headers.origin, 'https://app.test');
});
test('public routes never send the token', async () => {
  const pub = Object.entries(ROUTES).find(([, r]) => r[2] === 'none' && !r[3].length);
  await client()[pub[0]]();
  assert.equal(last.headers.authorization, undefined);
});
test('a route for the other kind of token is refused before sending', () => {
  const botRoute = Object.entries(ROUTES).find(([, r]) => r[2] === 'bot');
  assert.throws(() => client().call(botRoute[0], Object.fromEntries(botRoute[1][3].map(p => [p[0], 'x']))), /requires bot/);
});
test('path parameters are checked', () => {
  assert.throws(() => client().call('nope'), /Unknown operation/);
  assert.throws(() => client().delete_bonfire_keys_by_kid({}), /Missing path parameter/);
  assert.throws(() => client().delete_bonfire_keys_by_kid({ kid: '..' }), /dot segments/);
  assert.throws(() => client().delete_bonfire_keys_by_kid({ kid: 'a', nope: 1 }), /Unknown path parameter/);
});
test('errors', async () => {
  const c = client();
  await assert.rejects(c.request('GET', '/scope'), e => e instanceof ScopeError && e instanceof APIError && e.scope === 'CHAT' && e.status === 403);
  await assert.rejects(c.request('GET', '/limited'), e => e instanceof APIError && e.retry_after === 7 && e.error === 'rate_limited');
  await assert.rejects(c.request('GET', '/boom'), e => e instanceof APIError && e.error === 'http_error');
  await assert.rejects(c.request('GET', '/redirect'), e => e instanceof APIError && e.status === 302);
  await assert.rejects(new Client('t', { baseUrl: 'http://127.0.0.1:1', allowInsecure: true }).request('GET', '/x'), TransportError);
});
test('response kinds', async () => {
  const c = client();
  assert.equal(await c.request('GET', '/text'), 'hi');
  assert.equal(await c.request('GET', '/empty'), null);
  assert.ok((await c.request('GET', '/x', { raw: true })) instanceof Uint8Array);
});
test('uploads', async () => {
  await client().request('POST', '/up', { data: { a: 'b', c: { d: 1 } }, files: { file: ['n.txt', new TextEncoder().encode('hello'), 'text/plain'] } });
  assert.match(last.headers['content-type'], /^multipart\/form-data/);
  const body = last.body.toString();
  assert.ok(body.includes('filename="n.txt"') && body.includes('hello') && body.includes('{"d":1}'));
});
test('helpers', async () => {
  const c = client();
  assert.deepEqual(await c.product('p/1'), { id: 'p' });
  assert.equal(last.url, '/products/p%2F1');
  await c.add_to_cart('p', { plan: 'yearly' });
  assert.deepEqual(JSON.parse(last.body), { product_id: 'p', plan: 'yearly' });
  await c.pay_directly([{ product_id: 'p' }], 5, { idempotency_key: 'k' });
  assert.equal(last.url, '/checkout/direct');
  assert.deepEqual(JSON.parse(last.body), { items: [{ product_id: 'p' }], expected_total: 5, idempotency_key: 'k' });
  await c.pay_directly([], 0);
  assert.ok(JSON.parse(last.body).idempotency_key);
  assert.equal(scope_names(scope_mask('CHAT')).includes('CHAT'), true);
  assert.equal(has_scope(SCOPES.CHAT, 'CHAT'), true);
  assert.throws(() => scope_mask('NOPE'));
});
test('bad settings and token safety', () => {
  assert.throws(() => new Client('t', { baseUrl: 'http://x.test' }), /HTTPS required/);
  assert.throws(() => new Client('t', { baseUrl: 'https://u:p@x.test' }), /credentials/);
  assert.throws(() => new Client('t', { authScheme: 'Basic' }), /authScheme/);
  assert.throws(() => new Client('a\nb'), /Invalid token/);
  assert.ok(!JSON.stringify(new Client('secret')).includes('secret'));
});
test('the CommonJS build works too', () => {
  const { Client: C, ROUTES: R } = createRequire(import.meta.url)('../dist/index.cjs');
  assert.equal(Object.keys(R).length, Object.keys(ROUTES).length);
  assert.equal(typeof new C('t').post_checkout_direct, 'function');
});

test('startAppLinkLogin: PKCE, state, and only the matching link finishes', async () => {
  const p = await startAppLinkLogin('app_' + 'a'.repeat(20), 'myapp://signed-in', { baseUrl: base, allowInsecure: true });
  const start = JSON.parse(last.body);
  pkce.challenge = start.code_challenge;
  assert.equal(start.redirect_uri, 'myapp://signed-in');
  assert.equal(start.code_challenge_method, 'S256');
  assert.match(start.code_challenge, /^[A-Za-z0-9_-]{43}$/);
  assert.equal(start.state, p.state);
  assert.ok(p.url.endsWith('/login?code=c0de'));
  const link = 'myapp://signed-in?nookara_code=c0de&nookara_grant=' + 'g'.repeat(32) + '&state=' + encodeURIComponent(p.state);
  assert.ok(p.matches(link));
  await assert.rejects(p.finish('myapp://signed-in?nookara_code=c0de&nookara_grant=' + 'g'.repeat(32) + '&state=other'), /different sign-in/);
  assert.deepEqual(await p.finish(link), { token: 'apptok', scopes: 5 });
  assert.equal(last.headers.authorization, undefined);
  assert.deepEqual(await p.finish(null, { grant: 'g'.repeat(32) }), { token: 'apptok', scopes: 5 });
  await assert.rejects(p.finish(null, { grant: 'x' }), TypeError);
  await assert.rejects(startAppLinkLogin('nope', 'myapp://x'), TypeError);
});

test('display names: set, clear, read, refusals, shown_name', async () => {
  const c = new Client('tok', { baseUrl: base, allowInsecure: true });
  assert.deepStrictEqual(await c.set_display_name('Nat'), { success: true, display_name: 'Nat' });
  assert.strictEqual(last.method, 'PATCH');
  assert.deepStrictEqual(JSON.parse(last.body), { display_name: 'Nat' });
  await c.clear_display_name();
  assert.deepStrictEqual(JSON.parse(last.body), { display_name: null });
  await c.set_display_name('');
  assert.deepStrictEqual(JSON.parse(last.body), { display_name: null });
  assert.strictEqual(await c.display_name(), 'Nat');
  await assert.rejects(c.set_display_name('Nookara'), e => e instanceof APIError && e.error === 'display_name_reserved');
  assert.strictEqual(shown_name({ username: 'nat', display_name: 'Nat' }), 'Nat');
  assert.strictEqual(shown_name({ username: 'nat', display_name: null }), 'nat');
  assert.strictEqual(shown_name(null), '');
});

test('personal stickers: list, add (multipart), rename, delete, info', async () => {
  const c = new Client('tok', { baseUrl: base, allowInsecure: true });
  const list = await c.personal_stickers();
  assert.strictEqual(last.method, 'GET');
  assert.deepStrictEqual([list.max, list.pro_max], [10, 50]);
  const s = await c.add_personal_sticker(['wave.png', new Uint8Array([137, 80, 78, 71]), 'image/png'], 'wave');
  assert.strictEqual(last.method, 'POST');
  assert.match(last.headers['content-type'], /multipart\/form-data/);
  assert.match(String(last.body), /name="file"; filename="wave.png"/);
  assert.match(String(last.body), /name="name"/);
  assert.strictEqual(s.sid, STK.sid);
  await c.rename_personal_sticker(STK.sid, 'hi');
  assert.deepStrictEqual([last.method, last.url, JSON.parse(last.body)], ['PATCH', '/chat/personal-stickers/s0123456789', { name: 'hi' }]);
  await c.delete_personal_sticker(STK.sid);
  assert.deepStrictEqual([last.method, last.url], ['DELETE', '/chat/personal-stickers/s0123456789']);
  assert.strictEqual((await c.personal_sticker_info(STK.sid)).owner.username, 'nat');
  assert.ok('get_chat_personal_stickers' in ROUTES);
});

test('personal sticker text both ways', () => {
  assert.strictEqual(personal_sticker_text(STK), STK.send);
  assert.strictEqual(personal_sticker_text({ url: STK.url, name: 'wave' }), STK.send);
  assert.deepStrictEqual(parse_personal_sticker(STK.send), { sid: STK.sid, name: 'wave', url: STK.url, animated: false });
  assert.strictEqual(parse_personal_sticker('https://cdn.nookara.cc/uploads/stickers/sabcdefabcd.gif').animated, true);
  for (const t of ['hi ' + STK.send, 'https://evil.example/uploads/stickers/s0123456789.png', 'https://nookara.cc/uploads/emojis/e0123456789.png', '', null]) assert.strictEqual(parse_personal_sticker(t), null);
});

test('clone locks: lock_my_emojis, clone_check (bytes or hash, no token), uploads send from', async () => {
  const c = new Client('tok', { baseUrl: base, allowInsecure: true });
  await c.lock_my_emojis(true);
  assert.deepStrictEqual([last.method, last.url, JSON.parse(String(last.body))], ['PATCH', '/chat/settings', { lock_emojis: true }]);
  const hit = await c.clone_check(new TextEncoder().encode('locked'));
  assert.strictEqual(hit.locked, true);
  assert.strictEqual(hit.auth, null);
  assert.match(last.url, /^\/chat\/clone-check\?sha256=[0-9a-f]{64}$/);
  assert.strictEqual((await c.clone_check(createHash('sha256').update('other').digest('hex'), 42)).locked, false);
  assert.match(last.url, /velora_id=42/);
  const e = await c.add_personal_emoji(['wave.png', new Uint8Array([137, 80]), 'image/png'], 'wave', { source: 'https://camp.example/uploads/emojis/e1.png' });
  assert.strictEqual(e.eid, 'e0123456789');
  assert.match(String(last.body), /name="from"/);
  assert.match(String(last.body), /camp\.example/);
  await c.add_personal_sticker(['wave.png', new Uint8Array([137, 80]), 'image/png'], 'wave');
  assert.doesNotMatch(String(last.body), /name="from"/);
  assert.strictEqual((await c.personal_emojis()).max, 25);
  assert.ok('get_chat_clone_check' in ROUTES);
});

test('ember permissions: names and back', () => {
  assert.deepEqual(ember_permission_names(257), ['SEND', 'ATTACH']);
  assert.deepEqual(ember_permission_names('0x101'), ['SEND', 'ATTACH']);
  assert.deepEqual(ember_permission_names(0), []);
  assert.equal(ember_permission_mask('SEND', 'ATTACH'), 257);
  assert.equal(ember_permission_mask(['send messages', 'Attach files']), 257);
  assert.equal(ember_permission_mask('administrator'), 512);
  assert.throws(() => ember_permission_mask('NOPE'));
  assert.throws(() => ember_permission_names('abc'));
  assert.deepEqual(ember_permission_names(4096 + 8192), ['UNMARKED_ALIASES', 'BIT_13']);
  assert.equal(ember_permission_mask('UNMARKED_ALIASES', 'BIT_13'), 12288);
  const big = (1n << 60n) | 1n;
  assert.equal(ember_permission_mask(ember_permission_names(big)), big);
  assert.equal(ember_permission_mask(ember_permission_names(big.toString())), big);
  const every = Object.values(EMBER_PERMISSIONS).reduce((a, b) => a | b, 0);
  assert.equal(ember_permission_mask(ember_permission_names(every)), every);
  assert.equal(EMBER_ALL_PERMISSIONS & EMBER_PERMISSIONS.VIEW, 0);
  assert.equal(has_ember_permission(257, 'SEND'), true);
  assert.equal(has_ember_permission(257, 'KICK'), false);
  assert.equal(has_ember_permission(512, 'KICK'), true);
  assert.equal(has_ember_permission(512, 'BIT_40'), false);
});
