# Nookara for Node

```sh
npm install nookara
```

Needs Node 18 or newer. No dependencies.

```js
import { Client, scope_mask } from 'nookara';      // or: const { Client } = require('nookara');

const nookara = new Client(process.env.NOOKARA_TOKEN);
const me = await nookara.get_account_me();
```

Every route is one method, with the same name as the Python SDK. Path parameters go in the same object as `query`, `json`, `data` and `files`:

```js
await nookara.get_products_by_id({ id: 'prod_123' });
await nookara.post_friends_request({ json: { username: 'someone' } });
```

Bots use `new Client(token, { authScheme: 'Bot' })`. A registered App's token only works from its authorized web addresses, so pass `{ origin: 'https://your.app' }` when calling from a server.

## Taking payments

```js
// send someone to checkout. No credits permission needed
const { checkout_url } = await nookara.add_to_cart('prod_123');

// or, if they gave your App Transfer Credits: up to 100 credits a day per App per person
const { total } = await nookara.quote_directly([{ product_id: 'prod_123' }]);
await nookara.pay_directly([{ product_id: 'prod_123' }], total);
```

## Who can call what

Some routes only work for a website sign-in or one of Nookara's own apps, and the server refuses anything else. The comment on each method says so, and `ROUTES` has the details.

| In the comment | Who can call it |
|---|---|
| (nothing) | Follows the route's own auth and scopes, the normal case for your App |
| `[any]` | Any signed-in token: `add_to_cart`, `product_access` |
| `[app]` | An App with Transfer Credits: `quote_directly`, `pay_directly` |
| `[website]` | Website sign-in only: your Products, sales, purchases, reading the cart, paying at checkout, reports and claims, managing Apps |
| `[drive]` | Nookara Drive's own app only, or Nookara for Windows |
| `[forums]` | Nookara Forums' own app only, for anything that changes something. Reading needs no token |
| `[devices]` | Nookara for Windows or a website sign-in |

## Errors

`APIError` has `status`, `error`, `payload` and `retry_after`. `ScopeError` means the person didn't allow a permission, so ask them to sign in again. `TransportError` means the network failed, and a failed write may already have reached the server. Nothing is retried for you, and redirects are refused so a token can't follow one somewhere else.

## Not in this package yet

The Python SDK also has sign-in helpers, websockets and the bot gateway, message signing, encrypted DMs and Ember instance clients. Here you bring a token you already have, and this package covers REST only. Staff routes are left out.

Guide: https://nookara.cc/guides/node-sdk. Every route: https://nookara.cc/guides/velora-api

## Changes in 0.1.7

Ember server permission numbers to names and back, same as Python 0.9.11. Unknown bits come out as `BIT_<n>`; a number past 2^53 comes back as a BigInt. Calculator and the full list: https://nookara.cc/docs/ember-permissions

```js
import { ember_permission_names, ember_permission_mask, has_ember_permission } from 'nookara';

ember_permission_names(257);                // ['SEND', 'ATTACH']
ember_permission_mask('SEND', 'ATTACH');    // 257
has_ember_permission(server.perms, 'KICK'); // ADMIN counts as everything
```

## Changes in 0.1.6

Clone locks. `lock_my_emojis(true)` turns on Lock my emojis and stickers (the chat setting `lock_emojis`): nobody else can clone your personal emojis and stickers to a server or add them to their own. Ember servers have the matching setting `emojis.allow_cloning`. An exact copy of a locked one is refused with `clone_locked` or `cloning_disabled` (403). Pass where a copied picture came from with `{ source }`, and ask first with `clone_check` (bytes or a SHA-256, no sign-in needed). Personal emojis are here too now, the same as Python.

```js
await me.lock_my_emojis(true);
console.log(await me.clone_check(fs.readFileSync('wave.png'))); // { locked: false }
await me.add_personal_emoji(['wave.png', bytes, 'image/png'], 'wave', { source: 'https://camp.example/uploads/emojis/e1.png' });
const { emojis } = await me.personal_emojis();
```

## Changes in 0.1.5

Personal stickers: stickers that belong to your Nookara account and can be sent anywhere (Ember servers, DMs, group chats). 10 for free accounts, 50 with Pro. A sticker is sent as a normal message whose whole text is its `send` link; Ember shows it as a sticker, other apps as a picture.

```js
import fs from 'node:fs';
import { Client, personal_sticker_text, parse_personal_sticker } from 'nookara';
const me = new Client(token);
const s = await me.add_personal_sticker(['wave.png', fs.readFileSync('wave.png'), 'image/png'], 'wave'); // too_many_stickers, file_too_large, invalid_sticker ...
const { stickers, max } = await me.personal_stickers();
const text = personal_sticker_text(s);   // https://nookara.cc/uploads/stickers/s....png#wave: send this as the whole message
console.log(parse_personal_sticker(text)); // { sid, name: 'wave', url, animated: false }
console.log(await me.personal_sticker_info(s.sid)); // { sticker, owner: { username, pfp } }
await me.rename_personal_sticker(s.sid, 'hi');
await me.delete_personal_sticker(s.sid);
```

The route list also caught up with the Python SDK 0.9.8 + 0.9.9 (bot DM routes and the personal sticker routes), so those are callable as route methods too.

## Changes in 0.1.4

Display names: people can pick a name shown instead of their username (mentions and links keep the username). Profiles, `/account/me`'s `account` and Ember members carry `display_name` (null on Nookara when unset).

```js
import { Client, shown_name } from 'nookara';
const me = new Client(token);
await me.set_display_name('Nat');   // null or '' clears it; refusals: APIError .error display_name_too_long, _bad_characters, _at, _reserved, _impersonation
console.log(await me.display_name()); // 'Nat'
console.log(shown_name(await me.get_account_lookup_by_username({ username: 'someone' })));
await me.clear_display_name();
```

## Changes in 0.1.3

- `startAppLinkLogin(appId, link)` signs in a desktop App through its app link (My Account > Apps > Desktop app links), with PKCE. Open `.url` in the browser; when the system opens your app with `myapp://signed-in?nookara_code=...&nookara_grant=...&state=...`, call `.finish(thatLink)` (or `.finish(null, { grant })` with the sign-in code the person pasted) for `{ token, scopes }`. The token works with no Origin from your program, so `new Client(token)` is enough.

## Changes in 0.1.2

- Three new App scopes in `SCOPES`: `NOTIFY_SEND` (262144), `NOTIFY_READ` (524288), `BLOCKS_READ` (1048576) and `BLOCKS_MANAGE` (2097152).
- `post_account_notifications_send` (`POST /account/notifications/send`, App tokens with Send Notifications). Notification and block routes list the scope an App token needs.

## Changes in 0.1.1

- Route descriptions say Ember instead of the old Bonfire name. Method names are unchanged: they follow the URL, so routes under `/bonfire/...` keep names like `get_bonfire_instances`.
- The README links the new Node guide.
