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

Docs: https://nookara.cc/guides/velora-api
