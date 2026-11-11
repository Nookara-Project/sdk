const BASE_URL = 'https://nookara.cc';
const VERSION = '__VERSION__';

export class APIError extends Error {
  constructor(status, payload, headers) {
    const isObj = payload && typeof payload === 'object';
    const code = isObj ? (payload.error ?? payload.message ?? 'api_error') : 'http_error';
    super(`Nookara API ${status}: ${/^[a-zA-Z0-9_ :.-]{1,100}$/.test(String(code)) ? code : 'api_error'}`);
    this.name = 'APIError';
    this.status = status;
    this.payload = payload;
    this.error = code;
    this.required_scope = isObj ? payload.required_scope ?? null : null;
    this.disabled_by_admin = isObj ? !!payload.disabled_by_admin : false;
    this.moved_to = isObj ? payload.moved_to ?? null : null;
    this.reason = isObj ? payload.reason ?? null : null;
    const value = isObj && payload.retry_after != null ? payload.retry_after : headers?.get?.('retry-after');
    const n = value == null ? NaN : Number(value);
    this.retry_after = Number.isFinite(n) ? Math.max(0, n) : null;
  }
}

export class ScopeError extends APIError {
  constructor(status, payload, headers) {
    super(status, payload, headers);
    this.name = 'ScopeError';
    const bit = this.required_scope;
    this.scope = typeof bit === 'number' ? Object.keys(SCOPES).find(k => SCOPES[k] === bit) ?? null : null;
  }
}

export class TransportError extends Error {
  constructor() {
    super('Nookara request failed; check connectivity before retrying writes');
    this.name = 'TransportError';
  }
}

function safePart(value) {
  const s = String(value);
  if (!s || s === '.' || s === '..') throw new TypeError('Path parameters cannot be empty or dot segments');
  return encodeURIComponent(s);
}

function multipart(data, files) {
  const form = new FormData();
  for (const [name, value] of Object.entries(data || {})) {
    if (value == null) continue;
    form.append(name, typeof value === 'object' ? JSON.stringify(value) : String(value));
  }
  for (const [name, value] of Object.entries(files || {})) {
    if (Array.isArray(value)) {
      const [filename, content, mime] = value;
      form.append(name, new Blob([content], { type: mime || 'application/octet-stream' }), filename);
    } else form.append(name, value, value.name || name);
  }
  return form;
}

export class Client {
  constructor(token = null, { baseUrl = BASE_URL, authScheme = 'Bearer', timeout = 30000, allowInsecure = false, origin = null, fetch: fetchFn = null } = {}) {
    let u;
    try { u = new URL(baseUrl); } catch { throw new TypeError('baseUrl must be an HTTP(S) origin'); }
    if (!['https:', 'http:'].includes(u.protocol) || u.username || u.password || u.search || u.hash) throw new TypeError('baseUrl must be an HTTP(S) origin without credentials or query');
    if (u.protocol !== 'https:' && !allowInsecure) throw new TypeError('HTTPS required; allowInsecure is for local tests only');
    if (!['Bearer', 'Bot'].includes(authScheme)) throw new TypeError('authScheme must be Bearer or Bot');
    if (token && /[\r\n]/.test(token)) throw new TypeError('Invalid token');
    Object.defineProperty(this, 'token', { value: token, enumerable: false, writable: true });
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.authScheme = authScheme;
    this.timeout = timeout;
    this.origin = origin;
    Object.defineProperty(this, '_fetch', { value: fetchFn || globalThis.fetch, enumerable: false });
  }

  async request(method, path, { query, json, data, files, auth = true, raw = false } = {}) {
    if (!path.startsWith('/') || path.startsWith('//') || path.includes('\\') || path.includes('#')) throw new TypeError('Use an origin-relative API path');
    if (json !== undefined && (data !== undefined || files !== undefined)) throw new TypeError('Use json OR form fields');
    const params = new URLSearchParams();
    for (const [k, v] of Object.entries(query || {})) {
      if (v == null) continue;
      if (Array.isArray(v)) v.forEach(x => params.append(k, String(x))); else params.append(k, String(v));
    }
    const qs = params.toString();
    const url = this.baseUrl + path + (qs ? (path.includes('?') ? '&' : '?') + qs : '');
    const headers = { Accept: 'application/json', 'User-Agent': `nookara-node/${VERSION}` };
    if (auth && this.token) headers.Authorization = `${this.authScheme} ${this.token}`;
    if (this.origin) headers.Origin = this.origin;
    let body;
    if (json !== undefined) { body = JSON.stringify(json); headers['Content-Type'] = 'application/json'; }
    else if (files !== undefined) body = multipart(data, files);
    else if (data !== undefined) { body = new URLSearchParams(data).toString(); headers['Content-Type'] = 'application/x-www-form-urlencoded'; }
    let res, bytes;
    try {
      res = await this._fetch(url, { method: method.toUpperCase(), headers, body, redirect: 'manual', signal: AbortSignal.timeout(this.timeout) });
      bytes = new Uint8Array(await res.arrayBuffer());
    } catch { throw new TransportError(); }
    const text = () => new TextDecoder().decode(bytes);
    if (res.status >= 300) {
      let payload;
      try { payload = JSON.parse(text()); } catch { payload = { error: 'http_error' }; }
      if (res.status === 403 && payload && ['insufficient_scope', 'scope_disabled'].includes(payload.error)) throw new ScopeError(res.status, payload, res.headers);
      throw new APIError(res.status, payload, res.headers);
    }
    if (raw) return bytes;
    if (!bytes.length) return null;
    const type = res.headers.get('content-type') || '';
    if (type.includes('json')) return JSON.parse(text());
    if (type.startsWith('text/')) return text();
    return bytes;
  }

  call(operationId, args = {}) {
    const route = ROUTES[operationId];
    if (!route) throw new TypeError(`Unknown operation: ${operationId}`);
    const [method, template, authKind, params] = route;
    const { query, json, data, files, raw, ...pathParams } = args;
    const names = new Set(params.map(p => p[0]));
    for (const k of Object.keys(pathParams)) if (!names.has(k)) throw new TypeError(`Unknown path parameter: ${k}`);
    let path = template;
    for (const [name, optional] of params) {
      const value = pathParams[name];
      if (value == null) {
        if (!optional) throw new TypeError(`Missing path parameter: ${name}`);
        path = path.replace(`/:${name}?`, '');
      } else path = path.replace(`:${name}${optional ? '?' : ''}`, safePart(value));
    }
    if (this.token && (authKind === 'bearer' || authKind === 'bot') && this.authScheme !== (authKind === 'bot' ? 'Bot' : 'Bearer')) throw new TypeError(`This route requires ${authKind} authentication`);
    return this.request(method, path, { query, json, data, files, raw, auth: authKind === 'bearer' || authKind === 'bot' });
  }

  product(productId) { return this.request('GET', `/products/${encodeURIComponent(productId)}`).then(d => d.product); }
  products_of(username) { return this.request('GET', '/products', { query: { seller: username } }).then(d => d.products); }
  add_to_cart(productId, { plan, quantity } = {}) { return this.request('POST', '/cart/items', { json: { product_id: productId, ...(plan != null ? { plan } : {}), ...(quantity != null ? { quantity } : {}) } }); }
  add_payment_to_cart(to, amount, { note } = {}) { return this.request('POST', '/cart/items', { json: { to, amount, ...(note != null ? { note } : {}) } }); }
  product_access(productId) { return this.request('GET', `/products/${encodeURIComponent(productId)}/access`); }
  quote_directly(items) { return this.request('POST', '/checkout/direct/quote', { json: { items } }); }
  async pay_directly(items, expectedTotal, { idempotency_key } = {}) {
    const key = idempotency_key || (await import('node:crypto')).randomUUID();
    return this.request('POST', '/checkout/direct', { json: { items, expected_total: expectedTotal, idempotency_key: key } });
  }
}

for (const id of Object.keys(ROUTES)) {
  if (!Client.prototype[id]) Client.prototype[id] = function (args) { return this.call(id, args); };
}

// ── desktop App sign-in (app links, PKCE): startAppLinkLogin -> open .url -> .finish(link) ──
const b64url = buf => Buffer.from(buf).toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
export async function startAppLinkLogin(appId, link, { baseUrl = BASE_URL, allowInsecure = false, fetch: fetchFn = null } = {}) {
  if (!/^app_[0-9a-f]{20}$/.test(String(appId))) throw new TypeError('Use the app ID from My Account > Apps');
  const { createHash, randomBytes } = await import('node:crypto');
  const verifier = b64url(randomBytes(48));
  const challenge = b64url(createHash('sha256').update(verifier).digest());
  const state = b64url(randomBytes(24));
  const client = new Client(null, { baseUrl, allowInsecure, fetch: fetchFn });
  const { code } = await client.request('POST', '/auth/ext-code', { auth: false, json: { app_id: appId, redirect_uri: link, code_challenge: challenge, code_challenge_method: 'S256', state } });
  const url = `${baseUrl.replace(/\/+$/, '')}/login?code=${encodeURIComponent(code)}`;
  const params = l => { try { return new URL(String(l)).searchParams; } catch { return new URLSearchParams(); } };
  return {
    appId, link, code, state, url,
    /** is this app link the answer to this sign-in? */
    matches: l => { const q = params(l); return q.get('nookara_code') === code && q.get('state') === state; },
    /** finish(link) with the link your app was opened with, or finish(null, { grant }) with the sign-in code the person pasted -> { token, scopes } */
    async finish(l, { grant } = {}) {
      if (l != null) {
        const q = params(l);
        if (q.get('nookara_code') !== code || q.get('state') !== state) throw new Error('That app link belongs to a different sign-in');
        grant = q.get('nookara_grant');
      }
      grant = String(grant ?? '').trim();
      if (!/^[A-Za-z0-9_-]{16,128}$/.test(grant)) throw new TypeError('Pass the app link your app was opened with, or the sign-in code');
      const r = await client.request('POST', '/auth/ext-code/exchange', { auth: false, json: { code, grant, code_verifier: verifier } });
      return { token: r.token, scopes: r.scopes };
    },
  };
}

export const scope_mask = (...names) => names.reduce((m, n) => { if (!(n in SCOPES)) throw new TypeError(`Unknown scope: ${n}`); return m | SCOPES[n]; }, 0);
export const scope_names = mask => Object.keys(SCOPES).filter(n => (Number(mask) & SCOPES[n]) === SCOPES[n] && SCOPES[n]);
export const has_scope = (mask, name) => (Number(mask) & SCOPES[name]) === SCOPES[name];
export { SCOPES, ROUTES, VERSION };
