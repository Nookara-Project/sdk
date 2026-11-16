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

  // display names (0.1.4): shown instead of the username; null / '' clears it. Refusals: APIError .error display_name_*
  set_display_name(name) { return this.request('PATCH', '/account/update', { json: { display_name: name || null } }); }
  clear_display_name() { return this.set_display_name(null); }
  async display_name() { const d = await this.request('GET', '/account/me'); return d?.account?.display_name || null; }

  // personal stickers (0.1.5): yours, sent anywhere as a message whose whole text is the sticker's `send` link
  personal_stickers() { return this.request('GET', '/chat/personal-stickers'); }
  add_personal_sticker(file, name, { source } = {}) { return this.request('POST', '/chat/personal-stickers', { data: uploadFields(name, source), files: { file } }).then(d => d.sticker); }
  rename_personal_sticker(sid, name) { return this.request('PATCH', `/chat/personal-stickers/${encodeURIComponent(sid)}`, { json: { name } }); }
  delete_personal_sticker(sid) { return this.request('DELETE', `/chat/personal-stickers/${encodeURIComponent(sid)}`); }
  personal_sticker_info(sid) { return this.request('GET', `/chat/personal-stickers/${encodeURIComponent(sid)}/info`); }
  // personal emojis (0.1.6, same as Python): yours, usable anywhere as <:name:eid>
  personal_emojis() { return this.request('GET', '/chat/personal-emojis'); }
  add_personal_emoji(file, name, { source } = {}) { return this.request('POST', '/chat/personal-emojis', { data: uploadFields(name, source), files: { file } }).then(d => d.emoji); }
  rename_personal_emoji(eid, name) { return this.request('PATCH', `/chat/personal-emojis/${encodeURIComponent(eid)}`, { json: { name } }); }
  delete_personal_emoji(eid) { return this.request('DELETE', `/chat/personal-emojis/${encodeURIComponent(eid)}`); }
  // link pills (0.1.8): what a link to a channel / message on a Nookara server is called ({ server, channel | null, joined })
  link_info(sid, cid) { return this.request('GET', `/chat/link-info/${encodeURIComponent(sid)}/${encodeURIComponent(String(cid).split('|').pop())}`); }
  // clone locks (0.1.6): Lock my emojis and stickers, and may a picture be copied?
  lock_my_emojis(on = true) { return this.request('PATCH', '/chat/settings', { json: { lock_emojis: !!on } }); }
  async clone_check(picture, velora_id) {
    const sha256 = typeof picture === 'string' ? picture : await sha256Hex(picture);
    return this.request('GET', '/chat/clone-check', { auth: false, query: { sha256, ...(velora_id != null ? { velora_id: String(velora_id) } : {}) } });
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

/** the name to show for a person: display_name when they have one, else username (profiles, /account/me's account, Ember members) */
export const shown_name = user => String(user?.display_name || '').trim() || user?.username || '';
// multipart fields for an emoji/sticker upload: name, and from (where a copied picture came from: its clone lock is checked)
const uploadFields = (name, source) => ({ ...(name ? { name } : {}), ...(source ? { from: source } : {}) });
// SHA-256 (hex) of bytes: a Uint8Array / ArrayBuffer / Buffer / Blob
async function sha256Hex(data) {
  const buf = typeof Blob !== 'undefined' && data instanceof Blob ? await data.arrayBuffer() : data;
  const d = await globalThis.crypto.subtle.digest('SHA-256', buf);
  return [...new Uint8Array(d)].map(b => b.toString(16).padStart(2, '0')).join('');
}
// a personal sticker message: its picture link on Nookara (Ember's stickerLink.js and Python's parse_personal_sticker use the same pattern)
const STICKER_LINK = /^https:\/\/(?:(?:cdn\.)?nookara\.cc|velora\.ikelene\.net)\/uploads\/stickers\/(s[0-9a-f]{10})\.(png|gif)(?:#(\w{1,32}))?$/;
/** the message text that sends a personal sticker (send it as the whole message) */
export const personal_sticker_text = sticker => sticker?.send || `${sticker.url}#${sticker.name}`;
/** { sid, name, url, animated } when a message's whole text is a personal sticker, else null */
export const parse_personal_sticker = text => {
  const t = String(text ?? '').trim();
  const m = STICKER_LINK.exec(t);
  return m ? { sid: m[1], name: m[3] || 'sticker', url: t.split('#')[0], animated: m[2] === 'gif' } : null;
};
// Ember server permission numbers (0.1.7, same as Python): a role's permissions, your server.perms, a channel's allow / deny.
// Calculator and the full list: https://nookara.cc/docs/ember-permissions. The table is generated from ember-server's src/perms.js.
// gen:start
const EMBER_PERMISSIONS = Object.freeze({"SEND":1,"MANAGE_CHANNELS":2,"MANAGE_SERVER":4,"MANAGE_ROLES":8,"KICK":16,"BAN":32,"MANAGE_MESSAGES":64,"MENTION_EVERYONE":128,"ATTACH":256,"ADMIN":512,"VIEW":1024,"MANAGE_USERS":2048,"UNMARKED_ALIASES":4096});
const EMBER_PERMISSION_LABELS = Object.freeze({"SEND":"Send messages","MANAGE_CHANNELS":"Manage channels","MANAGE_SERVER":"Manage server","MANAGE_ROLES":"Manage roles","KICK":"Kick members","BAN":"Ban members","MANAGE_MESSAGES":"Manage messages","MENTION_EVERYONE":"Mention @everyone, @here and all roles","ATTACH":"Attach files","ADMIN":"Administrator","VIEW":"View channel","MANAGE_USERS":"Manage users","UNMARKED_ALIASES":"Use unmarked aliases"});
const EMBER_ALL_PERMISSIONS = 7167;
const EMBER_CHANNEL_PERMISSIONS = 1281;
const EMBER_EVERYONE_DEFAULT = 257;
// gen:end
const EMBER_ALIASES = { SEND_MESSAGES: 'SEND', KICK_MEMBERS: 'KICK', BAN_MEMBERS: 'BAN', ATTACH_FILES: 'ATTACH', ADMINISTRATOR: 'ADMIN', VIEW_CHANNEL: 'VIEW', UNMARKED_ALIAS: 'UNMARKED_ALIASES' };
const EMBER_KNOWN = Object.values(EMBER_PERMISSIONS).reduce((m, b) => m | BigInt(b), 0n);
const emberBig = value => {
  if (typeof value === 'bigint') { if (value < 0n) throw new RangeError("Permissions can't be negative"); return value; }
  if (typeof value === 'number') { if (!Number.isSafeInteger(value) || value < 0) throw new RangeError(`Permissions must be a whole number, like 257: ${value}`); return BigInt(value); }
  const text = String(value ?? '').trim().replace(/_/g, '');
  if (text === '') return 0n;
  if (!/^(\d+|0x[0-9a-f]+|0b[01]+)$/i.test(text)) throw new RangeError(`Permissions must be a whole number, like 257: ${value}`);
  return BigInt(text.toLowerCase());
};
const emberOut = n => (n <= BigInt(Number.MAX_SAFE_INTEGER) ? Number(n) : n);
const emberBit = permission => {
  if (typeof permission === 'number' || typeof permission === 'bigint') {
    const b = BigInt(permission);
    if (b <= 0n || (b & (b - 1n))) throw new RangeError(`Not a single permission bit: ${permission}`);
    return b;
  }
  const text = String(permission).trim();
  let key = text.toUpperCase().replace(/[\s-]+/g, '_');
  key = EMBER_ALIASES[key] || key;
  if (key in EMBER_PERMISSIONS) return BigInt(EMBER_PERMISSIONS[key]);
  const byLabel = Object.keys(EMBER_PERMISSION_LABELS).find(k => EMBER_PERMISSION_LABELS[k].toLowerCase() === text.toLowerCase());
  if (byLabel) return BigInt(EMBER_PERMISSIONS[byLabel]);
  const extra = /^BIT_(\d{1,4})$/.exec(key);
  if (extra) return 1n << BigInt(extra[1]);
  throw new TypeError(`Unknown Ember permission: ${permission} (see https://nookara.cc/docs/ember-permissions)`);
};
/** names (or bits) -> the number: ember_permission_mask('SEND', 'ATTACH') === 257. An array works too. A number past 2^53 comes back as a BigInt. */
export const ember_permission_mask = (...permissions) => emberOut((permissions.length === 1 && Array.isArray(permissions[0]) ? permissions[0] : permissions).reduce((m, p) => m | emberBit(p), 0n));
/** the number (number, BigInt, or a string like '257' / '0x101') -> names, lowest bit first. Unknown bits come out as BIT_<n>. */
export const ember_permission_names = value => {
  const n = emberBig(value);
  const names = Object.keys(EMBER_PERMISSIONS).filter(k => (n & BigInt(EMBER_PERMISSIONS[k])) !== 0n);
  let rest = n & ~EMBER_KNOWN;
  for (let bit = 0; rest > 0n; bit++, rest >>= 1n) if (rest & 1n) names.push(`BIT_${bit}`);
  return names;
};
/** does this number allow the permission? ADMIN counts as every permission, like the server does. */
export const has_ember_permission = (value, permission) => {
  const n = emberBig(value), b = emberBit(permission);
  if ((n & BigInt(EMBER_PERMISSIONS.ADMIN)) && (b & EMBER_KNOWN)) return true;
  return (n & b) === b;
};
// Mentions, channels and message links in Ember text (0.1.8, same as Python 0.9.12). Discord's format: <@id> pings a
// person, <#cid> is a channel, <@&rid> a role, <:name:eid> a custom emoji; a plain "@name" is only text and pings nobody.
// Ids: a Nookara account number (<@42>), or on an Ember server the member's id there (<@v:42>, <@l:3>, <@b:7>).
const USER_TOKEN = /<@!?((?:[vlb]:)?\d{1,20})>/g, CHANNEL_TOKEN = /<#(c[0-9a-f]{10})>/g, ROLE_TOKEN = /<@&(r[0-9a-f]{10})>/g;
const EMOJI_TOKEN = /<(a?):([A-Za-z0-9_]{1,32}):(e[0-9a-f]{10})>/g;
const EMBER_HOME_HOSTS = ['ember.nookara.cc', 'nookara.cc', 'www.nookara.cc', 'velora.ikelene.net'];
const userIdOf = user => {
  const id = String((user && typeof user === 'object' ? user.id : user) ?? '').trim();
  if (!/^(?:[vlb]:)?\d{1,20}$/.test(id)) throw new TypeError(`Not a user id (a number, or v:/l:/b: and a number on an Ember server): ${user}`);
  return id;
};
const bareId = x => String((x && typeof x === 'object' ? x.cid : x) ?? '').split('|').pop().trim();
const uniq = a => [...new Set(a)];
/** the text that pings someone: mention(42) === '<@42>', mention({ id: 'v:42' }) === '<@v:42>' */
export const mention = user => `<@${userIdOf(user)}>`;
/** the text that links a channel: channel_mention('c0123456789') === '<#c0123456789>' (a channel object works too) */
export const channel_mention = channel => { const cid = bareId(channel); if (!/^c[0-9a-f]{10}$/.test(cid)) throw new TypeError(`Not a channel id: ${channel}`); return `<#${cid}>`; };
/** the text that pings a role: <@&rid> */
export const role_mention = role => { const rid = String((role && typeof role === 'object' ? role.rid : role) ?? '').trim(); if (!/^r[0-9a-f]{10}$/.test(rid)) throw new TypeError(`Not a role id: ${role}`); return `<@&${rid}>`; };
/** what a message's text points at: { users, channels, roles, emojis: [{ name, eid, animated }], everyone, here }. Only tokens count. */
export const parse_mentions = text => {
  const t = String(text ?? '');
  const seen = new Set(), emojis = [];
  for (const m of t.matchAll(EMOJI_TOKEN)) if (!seen.has(m[3])) { seen.add(m[3]); emojis.push({ name: m[2], eid: m[3], animated: m[1] === 'a' }); }
  return {
    users: uniq([...t.matchAll(USER_TOKEN)].map(m => m[1])), channels: uniq([...t.matchAll(CHANNEL_TOKEN)].map(m => m[1])),
    roles: uniq([...t.matchAll(ROLE_TOKEN)].map(m => m[1])), emojis, everyone: /(^|\s)@everyone\b/.test(t), here: /(^|\s)@here\b/.test(t),
  };
};
/** does this text ping that person (a <@id> token)? */
export const mentions_user = (text, user) => parse_mentions(text).users.includes(userIdOf(user));
const lookupName = (table, key, field) => {
  const v = typeof table === 'function' ? table(key) : table instanceof Map ? table.get(key) : table?.[key];
  return v && typeof v === 'object' ? (v.display_name || v[field]) : v;
};
/** tokens -> names for showing / logging: <@42> -> @name, <#cid> -> #channel, <@&rid> -> @role, <:name:eid> -> :name:.
 *  users / channels / roles: an object or Map of id -> name (or { display_name, username, name }), or a function. */
export const plain_text = (text, { users, channels, roles } = {}) => String(text ?? '')
  .replace(USER_TOKEN, (_, id) => `@${lookupName(users, id, 'username') || 'unknown-user'}`)
  .replace(CHANNEL_TOKEN, (_, cid) => `#${lookupName(channels, cid, 'name') || 'unknown'}`)
  .replace(ROLE_TOKEN, (_, rid) => `@${lookupName(roles, rid, 'name') || 'role'}`)
  .replace(EMOJI_TOKEN, (_, a, name) => `:${name}:`);
/** a link to a channel or one message that Ember opens in place (and shows as a pill when pasted). instance = an Ember server's address. */
export const message_link = (sid, cid, messageId = null, { instance = null, base = 'https://ember.nookara.cc' } = {}) => {
  const s = bareId(sid), c = bareId(cid);
  if (!/^s[0-9a-f]{10}$/.test(s) || !/^c[0-9a-f]{10}$/.test(c)) throw new TypeError('sid is s and 10 hex, cid is c and 10 hex');
  const at = instance ? `#/i/${encodeURIComponent(String(instance).replace(/\/$/, ''))}` : '#';
  return `${base.replace(/\/$/, '')}/${at}/s/${s}/${c}${messageId != null ? `/${BigInt(messageId)}` : ''}`;
};
/** { instance, sid, cid, message_id } for a link to an Ember channel / message (instance null on Nookara), else null */
export const parse_message_link = url => {
  let u;
  try { u = new URL(String(url ?? '').trim()); } catch { return null; }
  if (!/^https?:$/.test(u.protocol) || !EMBER_HOME_HOSTS.includes(u.hostname.toLowerCase()) || !['/', '/chat', '/chat/'].includes(u.pathname)) return null;
  let parts = u.hash.split('/');
  if (parts[0] !== '#') return null;
  parts = parts.slice(1);
  let instance = null;
  if (parts[0] === 'i') {
    try { instance = decodeURIComponent(parts[1] || ''); } catch { return null; }
    if (!/^https?:\/\/[^/|]+$/.test(instance)) return null;
    parts = parts.slice(2);
  }
  const [a, sid, cid, mid] = parts;
  if (a !== 's' || !/^s[0-9a-f]{10}$/.test(sid || '') || !/^c[0-9a-f]{10}$/.test(cid || '')) return null;
  if (mid && !/^\d{1,20}$/.test(mid)) return null;
  return { instance, sid, cid, message_id: mid || null };
};
export const scope_mask = (...names) => names.reduce((m, n) => { if (!(n in SCOPES)) throw new TypeError(`Unknown scope: ${n}`); return m | SCOPES[n]; }, 0);
export const scope_names = mask => Object.keys(SCOPES).filter(n => (Number(mask) & SCOPES[n]) === SCOPES[n] && SCOPES[n]);
export const has_scope = (mask, name) => (Number(mask) & SCOPES[name]) === SCOPES[name];
export { SCOPES, ROUTES, VERSION, EMBER_PERMISSIONS, EMBER_PERMISSION_LABELS, EMBER_ALL_PERMISSIONS, EMBER_CHANNEL_PERMISSIONS, EMBER_EVERYONE_DEFAULT };
