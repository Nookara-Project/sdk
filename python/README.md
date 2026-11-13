# Nookara for Python

```sh
pip install nookara
pip install "nookara[realtime]"   # websockets
pip install "nookara[signing]"    # cryptography, for signed messages and encrypted DMs
```

```python
from nookara import Client, Ember, Instance, login_app
```

0.9.0 removed the old Velora and Bonfire names: code that says `import velora_api`, `Bonfire` or `login_with_velora` needs the new names in Changes in 0.9.0.

**What's in it:** sign-in, profiles, friends, DMs, group chats, notifications, storage, credits, Ember chat and bots, bot payments and carts, Products, cart and direct pay, claims and reports, Nookara Drive, Forums, Devices and Apps, as one named method per route.

**Who can call what.** Some routes only work for a website sign-in or one of Nookara's own apps, and the server refuses anything else. Each method's entry in `catalogue.json` has a `surface`:

| surface | Who can call it |
|---|---|
| (none) | Follows the route's own auth and scopes, the normal case for your App |
| `any` | Any signed-in token: `add_to_cart`, `product_access` |
| `app` | An App with Transfer Credits: `quote_directly`, `pay_directly`. Up to 100 credits a day per App per person |
| `website` | Website sign-in only: your Products, sales, purchases, reading the cart, paying at checkout, reports and claims, managing Apps. Listed so the reference is complete, your App can't call them |
| `drive` | Nookara Drive's own app only, or Nookara for Windows |
| `forums` | Nookara Forums' own app only, for anything that changes something. Reading needs no token |
| `devices` | Nookara for Windows or a website sign-in |

To charge someone from your App, send them to checkout with `add_to_cart`, or use `pay_directly` if they gave you Transfer Credits.

## About this client

Nookara is the identity and platform API: accounts, direct messages, groups, friends,
credits, instance tickets, signing keys and hosting. **Ember** is the chat system. Every
Ember server is an **instance** at its own web address (the main community is
`https://chat.ikelene.net`; Nookara-hosted ones are `https://e-<slug>.nookara.cc`;
you can also self-host). One instance holds one community. This package talks to both.

It supports Python 3.10+ and exposes every documented REST operation as a named
method, plus a generic request method. REST needs only the Python standard
library. The optional `realtime` extra installs `websockets`; the optional
`signing` extra installs `cryptography` for message signing and verification.

## Install

Use the commands at the top of this page. From a source checkout, run `python -m pip install ".[realtime]"`
inside the folder containing `pyproject.toml`. `requirements.txt` installs the
optional websocket dependency only, not the Nookara package itself.

## Sign in, and what scopes mean now

Create an app in [My Account > Apps](https://nookara.cc/me#apps) with `http://localhost` as an
authorized URL (no port: it covers any port) and the scopes you need, then sign in with its ID:

```python
from nookara import Client, login_app

token, origin = login_app("app_0123456789abcdef0123")
nookara = Client(token, origin=origin)   # an app's token only works from its authorized URLs
print(nookara.scope_names())           # what the person actually allowed
print(nookara.ember_instances())       # the Ember servers saved on this account
```

The browser shows a consent screen. **Scopes are requested, never required**: the person
can untick any of them (the risky ones start unticked), so a token can come back with
fewer scopes than you asked for. Ask only for what you use, then check:

```python
nookara.has_scope("MEDIA_UPLOAD")     # True / False  (names, labels such as "Upload Media", or bits)
nookara.granted_scopes()              # the usable mask (approved and not switched off by an admin)
nookara.require_scope("CHAT")         # raises ScopeError with a clear message
```

A call without the scope raises `ScopeError` (a subclass of `APIError`) with `scope`,
`label` and `disabled_by_admin`, so you can show "log in again to use this" instead of
crashing. `login_app()` never asks for a password. To print the URL yourself use
`login_app(..., on_url=print)`. `login(project_name=..., scopes=...)` is the legacy login with a
permissions integer: it and the tokens it made stop working on 3 December 2026.
Do not print the returned token. For an existing token use `Client(os.environ["NOOKARA_TOKEN"])`.

| Scope | Bit | Default on the consent screen | Ember instance scope |
|---|---|---|---|
| View Basic Profile | 1 | on | |
| View Sensitive Info | 2 | off | |
| Project Auth | 4 | on | |
| Modify Settings | 8 | off | |
| Read Storage / Write Storage | 16 / 32 | on / off | |
| Read Instant Messages / Send Instant Messages | 64 / 128 | on | |
| View Friends / Manage Friends | 256 / 512 | on / off | |
| Spend Credits | 1024 | off | |
| Chat Messaging | 2048 | on | `chat` (needed to sign in to an instance) |
| Upload Media | 4096 | on | `media` (uploads) |
| View Subscriptions | 8192 | on | |
| Nookara Voice | 16384 | on | `voice` |
| Sign Messages | 32768 | off | `sign` (signed messages) |

`nookara.SCOPES`, `SCOPE_LABELS`, `DEFAULT_OFF`, `INSTANCE_SCOPES`,
`scope_mask()`, `scope_names()` and `has_scope()` give you the same table in code.

## Ember servers (instances)

```python
from nookara import Client, Instance

nookara = Client(token)                              # needs Chat (2048)
chat = Instance("https://chat.ikelene.net")
info = chat.discover()                              # /.well-known/bonfire, no login
print(info["name"], info["accounts_mode"], info["build"]["version"], info["read_only"])
chat.login_with_nookara(nookara, sign="auto")         # Nookara-login instances
# chat.login("name", "password")                    # local-account instances
# chat.register("name", "password")

print(chat.scopes)                                  # instance scopes of this session: chat, voice, media, sign
channel = chat.channel_id("#general")
for message in chat.messages(channel, limit=20)["messages"]:
    print(message["author"]["username"], message["body"])
chat.send_message(channel, "Hello from Python!")
```

`login_with_nookara` asks Nookara for a short ticket made for that one instance and
trades it at `POST /api/v1/auth/velora`. Your Nookara token never leaves Nookara. The
ticket carries the instance scopes the person allowed (`chat`, `voice`, `media`, `sign`);
`sign="auto"` signs only when Sign Messages was allowed, `sign=True` raises `ScopeError`
if not. The instance session lasts 30 days from last use.

Discovery helpers: `accounts_mode`, `features`, `build` (version, commit, build_id),
`read_only`, `instance_info()` (`GET /api/v1/instance/info`, admins also get runtime, stats
and `update`) and `update_available()`. `Client.server_latest()` returns the official
build instances compare with.

Useful methods: `servers()` / `joined_communities()`, `channels()`, `members()`,
`send_message()`, `edit_message()`, `delete_message()`, `react()`, `pin()`, `search()`,
`join()`, `invites()`, `create_invite(expires_in=, max_uses=)`, `delete_invite()`,
`join_invite(code)`, `invite_info(code)`, `join_requests()`, `accept_join_request(uid)`,
`create_channel()`, `set_channel_permissions()`, `kick()`, `webhooks()`,
`create_webhook()`, `bots()`, `create_bot()`, `backups()`, `create_backup()`, `settings()`,
`identities(ids)`, `set_notify()`. Every route also has a named method
(`get_api_v1_servers_by_sid`) and `instance.call(...)`. IDs are strings; users look like
`v:123`, `l:7`, `b:3`.

### Your servers as one object

```python
from nookara import Ember

ember = Ember(nookara, sign="auto")
ember.join_default()                              # the official server, once per account
for item in ember.communities():                  # one entry per saved server
    print(item["instance"], (item["community"] or {}).get("name"), item["error"])
ember.add("https://e-camp.nookara.cc")     # saved on the account, follows the person between devices
```

A server that is down, banned, in local-account mode, or where Chat was declined is
reported in `error` (`unreachable`, `local_accounts`, `chat_scope_missing`, an API code);
it never stops the others.

### Uploads and media import

```python
uploaded = chat.upload("picture.png", cid=channel)                 # needs the media scope
saved = chat.import_media("https://example.com/cat.png", cid=channel)   # the instance fetches an https URL
chat.send_message(channel, "A picture", attachments=[uploaded, saved])
```

A session without the `media` scope raises `ScopeError` before anything is sent.
Uploads also need the community's `allow_uploads` and the channel's Attach permission.

### Signing and verifying

```python
chat.login_with_nookara(nookara, sign=True)           # account key from Nookara, kept in memory
sent = chat.send_message(channel, "Signed")
ok, reason = chat.verify_message(sent["message"])   # you check it, not the instance's `verified` flag
```

Signing is optional on every Nookara-login instance and never required. It needs the
Sign Messages scope and the `signing` extra. Signatures follow protocol section 8, including
`url:` entries for link-only GIFs. `verify_message` reads the public key from Nookara and
checks owner, revocation time and the Ed25519 signature.

### Webhooks need no login

```python
from nookara import execute_webhook
execute_webhook("https://chat.ikelene.net/api/v1/webhooks/ID/TOKEN", "Build finished")
```

### Bots

An **instance bot** is created on one instance (`chat.create_bot("pingbot")` returns the
token once) and uses a bot token. REST is Discord-style at `/bot/v1` with numeric ids, the
bot gateway is `/bot/gateway`:

```python
bot = Instance("https://chat.ikelene.net", bot_token=os.environ["EMBER_BOT_TOKEN"])
async with bot.bot_gateway() as gateway:
    async for event in gateway:                    # {"type": "MESSAGE_CREATE", "data": {...}}
        ...
bot.bot_send("NUMERIC_CHANNEL_ID", "pong")
```

A **Nookara developer bot** lives on your Nookara account and can be listed in the bot
gallery (Discovery > Bots) so others add it to their servers. Each instance makes its own
bot account for it, but the token is the same. A bot program serves all of them:

```python
from nookara import BotProgram

async with BotProgram(os.environ["NOOKARA_BOT_TOKEN"]) as bot:   # GET /bonfire/bots/self/installs
    async for event in bot:                                      # {"instance", "type", "data", "seq"}
        if event["type"] == "MESSAGE_CREATE" and event["data"]["content"] == "!ping":
            await bot.send(event["instance"], event["data"]["channel_id"], "pong")
```

It opens one gateway per install, re-reads the install list every 5 minutes, and keeps
going when one instance fails. Gallery owner calls: `list_gallery()`, `save_gallery_listing()`,
`submit_to_gallery()`, `gallery_status()`, `withdraw_from_gallery()`, `gallery_ticket()` and
`Instance.add_gallery_bot(ticket)`.

### User gateway

```python
chat.login_with_nookara(nookara)
async with chat.gateway() as gateway:
    async for event in gateway:
        if event["type"] == "chat_message":
            print(event["message"]["body"])
    # or: @gateway.on("chat_message") ... then: await gateway.run()
await_ack = await gateway.send_message(channel, "hi")   # waits for chat_ack
```

It reconnects with capped backoff and jitter (1s to 30s), pings every 25 s, and stops on
close codes 4001 and 4003. There is no replay: after `gateway_ready` follows a drop,
refetch history over REST and dedupe by id.

### Other Nookara-side Ember helpers

`Client`: `instance_token(url)`, `signing_key()`, `ember_instances()`,
`set_ember_instances(urls)`, `sync_ember_instances(urls)`, `ember_default_instance()`,
`ember_default_joined()`, `ember_instance_prefs()`, `ember_directory(q)`,
`ember_profiles(ids)`, `ember_key(kid)`, `ember_jwks()`, `ember_scopes()`,
`ember_import_platforms()` / `start_ember_import()` (Discord and Fluxer bundles),
and hosting: `hosting_plans()`, `hosting_servers()`,
`create_hosting_server(slug, name, plan, weeks=)`, `buy_hosting_weeks(slug, weeks)`,
`backup_hosting_server(slug)`, `hosting_backups()`, `upload_hosting_backup(...)`,
`delete_hosting_server(slug)`. Plus is prepaid in weeks and never renews by itself; it is
free for Nookara Pro. Examples are in `examples/ember_*.py`.

## Nookara REST methods

Nookara-hosted chat servers (`/chat/servers`, `/chat/channels` and so on) are
legacy and read-only now (writes answer `server_read_only` with `moved_to`). Direct
messages, groups, friends, storage, credits and presence are unchanged.

```python
nookara.send_dm("someone", "Hello from Python!")
nookara.set_activity("My game", state="In the menu", ttl=600)
nookara.clear_activity()
```

The old `servers()`, `server()`, `messages()` and `send_message()` helpers on `Client`
still call the legacy routes (they now emit a `DeprecationWarning`); use `Instance` for
new work.

Group chats have reactions, edits and pins, and DMs have pins (0.6.3):

```python
nookara.patch_groups_by_room_messages_by_id(room="grp_x", id="a1b2c3", json={"message": "fixed"})  # your own message
nookara.delete_groups_by_room_messages_by_id(room="grp_x", id="a1b2c3")                             # your own message
nookara.put_groups_by_room_messages_by_id_reactions_by_emoji(room="grp_x", id="a1b2c3", emoji="\N{THUMBS UP SIGN}")
nookara.delete_groups_by_room_messages_by_id_reactions_by_emoji(room="grp_x", id="a1b2c3", emoji="\N{THUMBS UP SIGN}")
nookara.put_groups_by_room_messages_by_id_pin(room="grp_x", id="a1b2c3")    # any member, 50 per group
nookara.get_groups_by_room_pins(room="grp_x")["messages"]
nookara.put_im_by_id_pin(id=123)                                            # either person, 50 per conversation
nookara.get_im_with_by_username_pins(username="someone")["messages"]
```

The realtime client gets `room_message_edited`, `room_message_reactions`, `room_message_deleted`, `room_pins_update`,
`im_deleted` and `im_pins_update`.

`send_dm(username, message)` requires Send Instant Messages (128). Storage uses Read (16) /
Write (32); its values are strings. Use `json.dumps()` / `json.loads()` for structured data.

Every operation in the downloadable catalogues (Nookara on `Client`, instances on `Instance`)
has a named method. For example:

```python
chat.post_api_v1_servers_by_sid_roles(
    sid="YOUR_SERVER_SID", json={"name": "Member", "permissions": 257}
)
chat.call("get_api_v1_servers_by_sid", sid="YOUR_SERVER_SID")
nookara.call("get_bonfire_hosting_plans")
nookara.request("GET", "/bonfire/instances")
```

Use `query={...}` for queries, `json={...}` for JSON, or `data={...}, files={...}` for
multipart. Path parameters are URL encoded; optional parameters may be omitted. The API
checks token scopes, server/channel roles, rank and privacy separately. File values can
also be `(filename, bytes_or_file_object, mime_type)`. This client buffers multipart data
with a 64 MiB limit; server limits can be smaller.

## Errors

```python
from nookara import APIError, ScopeError, TransportError

try:
    chat.upload("picture.png")
except ScopeError as exc:
    print("Log in again and keep this permission ticked:", exc.label or exc.error)
except APIError as exc:
    print(exc.status, exc.error, exc.retry_after, exc.moved_to)
except TransportError:
    print("Network error. Check whether a write completed before retrying.")
```

The library does not retry requests automatically. Handle 429 using Retry-After or
`retry_after` when present, with backoff. Error payloads are available as `exc.payload`.
Some endpoints return empty 204, text or binary responses; use `raw=True` for bytes.
Redirects are rejected so credentials are never forwarded.

## Realtime user client (Nookara)

```python
import asyncio
import os
from nookara import RealtimeClient

async def main():
    async with RealtimeClient(os.environ["NOOKARA_TOKEN"]) as socket:
        await socket.set_activity("My Python app", state="Connected")
        async for event in socket:
            if event.get("type") in ("im_received", "presence_update"):
                print(event)

asyncio.run(main())
```

This is Nookara's own socket: presence, direct messages, groups, calls. Entering the context
waits for `auth_success`, checks `tos_required`, starts the reader and sends `chat_hello`
when the Chat scope is granted. Its `chat_*` frames only concern legacy Nookara-hosted
servers; Ember chat uses the instance gateway above. `rpc()` is only for frames with nonce
replies. On disconnect, reconnect, authenticate, refetch REST state and rebuild presence.
There is no durable websocket replay.

This package transports voice signaling but does not implement WebRTC, audio
capture/playback or a desktop UI. See the voice guide for a WebRTC implementation,
including two peer connections and subscription snapshots.

## Legacy Nookara bots and webhooks

These Nookara-hosted routes are read-only now; use the instance bots and webhooks above.

```python
bot = Client(os.environ["NOOKARA_BOT_TOKEN"], auth_scheme="Bot")
me = bot.get_chat_api_v1_users_me()
```

## Game servers (Ember Link, Minecraft)

On a Ember instance the game plugin connects out to the instance
(`bonfire server https://chat.example` in the game console); an admin picks it from the
connected list:

```python
for server in chat.game_connected()["instances"]:          # waiting to be linked (Manage server)
    print(server["iid"], server["pairing_tag"], server["motd"])
chat.game_link(iid, cid=GAME_CHANNEL_CID)
print(chat.game_status(GAME_CHANNEL_CID))
```

`Client.game_*` still exist for the legacy Nookara routes. Console commands may require the
website or the Ember app (`console_needs_bonfire`).

## Bot payments (0.5.0)

A bot can ask a Nookara user for credits. The bot authenticates with its **bot token**; the buyer
opens the returned `pay_url`, signs in with their normal login (no scopes, no app authorization)
and presses Pay. The credits go to the bot's owner. There is no webhook, so you poll.

```python
from nookara import BotClient, is_paid, OrderConflict, BuyerError, PaymentError

bot = BotClient(os.environ["BOT_TOKEN"])
request = bot.create_payment_request("alice", 20, "ord-1001", description="Premium pack",
                                     return_url="https://shop.example/done", expires_in=900)
print(request["pay_url"])                         # send the buyer here, do not log it publicly
final = bot.wait_for_payment(request["id"], timeout=900, poll=3)   # PaymentTimeout when still pending
if is_paid(final) and final["amount"] == 20:      # fulfil ONLY when paid; check amount and buyer id
    ...
```

`get_payment_request(id)`, `find_payment_request(order_id)` (None if unknown),
`list_payment_requests(status=None, limit=None)` and `cancel_payment_request(id)` complete the set.
Repeating `create_payment_request` with the same order id, buyer and amount returns the existing request
(`idempotent_replay` is true); a different buyer or amount raises `OrderConflict`. Errors are
`PaymentError` subclasses (still `APIError`): `InvalidBotToken`, `MerchantUnavailable`,
`InvalidPaymentRequest`, `BuyerError`, `OrderConflict`, `PaymentInProgress`, `NotCancellable`,
`PaymentNotFound` and `PaymentRateLimited`; `error.error` keeps the server code. Run this on a server:
**never put a bot token in a Scratch/PenguinMod project, web page or app** (the PenguinMod extension has no
payment blocks for that reason). See `examples/bot_payments.py` and the Bot payments section of the guide.

Bot presence: a bot is online in a community while it holds an authenticated `/bot/gateway` connection.
Member objects from `Instance.members(...)` carry `presence` (`"online"` or `"offline"` for bots, `null` for
people) and the instance websocket (`InstanceGateway`) delivers `chat_presence` events; the library passes these through unchanged.
`Client.bot_installs()` includes staff test installs with `test: true` (not counted as real installs; skip them).

## Notifications (0.5.7)

Friend requests, credits, store sales, badges, membership, hosting and messages from the Nookara team are
notifications (the bell on the site and in Ember). System DMs are gone: those messages are notifications now.

```python
page = nookara.notifications(unread=True, limit=20)      # {"notifications": [...], "next_cursor": ..., "unread": n}
for n in page["notifications"]:
    print(n["category"], n["title"], n["body"])          # plain text, **bold** is the only markup
nookara.mark_notifications_read([n["id"] for n in page["notifications"]])   # or mark_notifications_read(all=True)
print(nookara.unread_notifications())
for category in nookara.notification_settings():          # locked ones (system, moderation) are always on
    print(category["key"], category["list"], category["email"], category["locked"])
nookara.set_notification_settings({"friends": {"email": False}})
```

`mark_notifications_unread(ids)` and `delete_notification(id)` complete the set; the generated methods are
`get_account_notifications`, `get_account_notifications_unread_count`, `post_account_notifications_read`,
`post_account_notifications_unread`, `delete_account_notifications_by_id`, `get_account_notification_settings`
and `patch_account_notification_settings`. Live changes arrive on the user websocket:

```python
async with RealtimeClient(os.environ["NOOKARA_TOKEN"]) as socket:
    async for event in socket.notification_events():     # notification_new / notifications_updated
        print(event["type"], event["unread"])
```

`notification_new` carries `notification` (same shape as the list) and `unread`; `notifications_updated` carries
`unread` and one of `read` (ids or `"all"`), `unread_ids` or `deleted`. The older `/notifications` routes still
exist for the Scratch extension. Staff can send with `post_admin_notifications_send`.

## Bot aliases (0.5.8)

A bot can post a message under another name and avatar. The message still belongs to the bot (mentions,
moderation and reports use the real bot); clients show the alias with a mask icon and the tooltip
"Posted by BOT as ALIAS". Only bot tokens may set an alias; a user or session token gets `403 alias_bots_only` (`APIError`), also for `alias=None` and on the gateway `chat_send`.

```python
from nookara import Instance, make_alias

bot = Instance("https://chat.ikelene.net", bot_token=os.environ["BOT_TOKEN"])
sent = bot.bot_send("CHANNEL_ID", "Welcome in!", alias={"name": "Narrator", "avatar_url": "https://example.com/n.png"})
print(sent["alias"])                        # {"name": "Narrator", "avatar_url": "https://example.com/n.png"}
bot.bot_edit("CHANNEL_ID", sent["id"], alias=make_alias("Storyteller"))   # change it
bot.bot_edit("CHANNEL_ID", sent["id"], alias=None)                        # clear it
```

`name` is 1-32 characters with no line breaks and `avatar_url` is optional (`None` or `""` = no avatar), `https://` only, at most 500
characters, no `user:pass@`, no whitespace; leaving `alias` out of `bot_edit` keeps the current one; `make_alias` checks both before the request (`ValueError`). `alias=` is also accepted by
`BotProgram.send(...)` (through its fields), `Instance.send_message`, `Instance.edit_message` and
`InstanceGateway.send_message`. Messages are plain dicts in this library, so read `message["alias"]`, which is
`None` or `{"name", "avatar_url", "unmarked"}`; `message["author"]` is always the real bot.

Unmarked aliases: when an Ember server's owner turns on Server settings > Danger zone > Advanced > "Allow unmarked aliases"
(`advanced.unmarked_aliases`, owner only) and the bot has the "Use unmarked aliases" role permission (4096) or Administrator,
its aliases come back with `"unmarked": True` and, when the name matched exactly one member of that server, `"member_id"`
(a principal on the client API, a numeric id on the bot API). Clients then show the alias like a normal member message. Nothing
changes in this library: the fields are just more dict keys, and `message["author"]` is still the real bot.

## Complete reference

https://nookara.cc/guides/velora-api

The catalogue records the live API on 2026-10-19. Staff-only routes are left out. Not every
input has a strict JSON Schema and not every privileged operation is tested live. The
server remains authoritative. Internal bridge/payment integration credentials and
deployment callbacks are not public client APIs.

## Changes in 0.9.7

Display names (Nookara 2026-11): people can pick a name that shows instead of their username. The username stays their handle (mentions, links, sign-in). Profiles (`lookup`, `lookup_many`), `/account/me`'s `account`, live `user_update` events and Ember server members / authors carry `display_name` (None on Nookara when they have none; Ember servers repeat the username then).

```python
import nookara

me = nookara.Client(token)
me.set_display_name("Nat ✿")       # 1-32 characters; None / "" clears it
print(me.display_name())            # "Nat ✿"
p = me.lookup("ikelene")
print(nookara.shown_name(p))        # display name, else the username
me.clear_display_name()
```

Refusals come back as `APIError` with `display_name_too_long`, `display_name_bad_characters`, `display_name_at`, `display_name_reserved` (reads as Nookara, the system or staff) or `display_name_impersonation` (a staff member's name).
## Changes in 0.9.6

Desktop and phone apps can sign in through their own app link (Nookara 2026-11): add a link like `myapp://signed-in` under My Account > Apps > Desktop app links, register that scheme with the system, then:

```python
import webbrowser, nookara

pending = nookara.start_app_link_login("app_...", "myapp://signed-in")
webbrowser.open(pending.url)
# ...later, when the system opens your app with myapp://signed-in?nookara_code=...&nookara_grant=...&state=...
token, scopes = pending.finish(link_your_app_was_opened_with)
# or, if the link didn't open: pending.finish(grant=code_the_person_pasted)
```

It uses PKCE (`code_challenge` on `POST /auth/ext-code`, `code_verifier` on `POST /auth/ext-code/exchange`), so another program that catches the link gets nothing. `login_app()` now sends PKCE too, which makes its token a desktop one: it works from your program with no Origin header (from a web page, still only on the App's sites).

## Changes in 0.9.5

Three new App scopes (they sit above the old 16 bits, so only a registered App's token can hold them):

| Scope | Bit | What it opens |
|---|---|---|
| `NOTIFY_SEND` (Send Notifications) | 262144 | `send_notification(title, body=None, link=None)`, `POST /account/notifications/send` |
| `NOTIFY_READ` (Read Notifications) | 524288 | `notifications()`, `unread_notifications()`, `mark_notifications_read()`, `delete_notification()` and the older `/notifications` routes |
| `BLOCKS_READ` (View Blocked People) | 1048576 | `blocked_people()`, `GET /account/blocks` |
| `BLOCKS_MANAGE` (Block and Unblock, includes View) | 2097152 | `block(username)`, `unblock(username)` |

An App token now needs these for notifications and blocks; Friends no longer reaches blocks for Apps. `SCOPES` also lists `FILES_READ` and `FILES_WRITE`.

## Changes in 0.9.4

Personal emojis (needs Chat): emojis that belong to your Nookara account and work on every Ember server, in DMs and in group chats (25 for free accounts, 100 with Pro). `personal_emojis()` is `GET /chat/personal-emojis` and answers `{emojis: [{eid, name, animated, url, created_at}], max, pro_max}`. `add_personal_emoji(file, name=None)` uploads a PNG, JPG, GIF or WebP up to 2 MB and returns the emoji; `rename_personal_emoji(eid, name)` and `delete_personal_emoji(eid)` do what they say. In a message they are the same `<:name:eid>` or `<a:name:eid>` as server emojis. `emoji_info(eid)` (`GET /chat/emojis/:eid/info`) now also answers for personal emojis with `{emoji, server: None, personal: {owner: {username, pfp}}}`. Errors: `too_many_emojis`, `file_too_large` (413), `invalid_emoji`, `name_required`, `not_found` (404), `upload_suspended` (403).

Server stickers on Ember servers: `Instance.stickers()` lists the server's stickers (`{stickers: [{tid, name, animated, url}], max: 30}`), `all_stickers()` lists them for every server you are in, and with Manage server `add_sticker(file, name=None)` (PNG, GIF, WebP or APNG up to 512 KB), `rename_sticker(tid, name)` and `delete_sticker(tid)`. Send one with `send_sticker(cid, tid)` or `send_message(cid, '', sticker=tid)` (the instance gateway's `send_message` takes `sticker=` too); a sticker only works in channels of its own server (`unknown_sticker` otherwise). Messages carry `sticker: {tid, name, url, animated}`, or `{tid, name: None, url: None, animated: False, deleted: True}` after the sticker was deleted, and the server sends `chat_stickers_update {server, stickers}` when they change. Errors: `too_many_stickers`, `file_too_large` (413), `images_only`, `no_file`, `name_required`, `unknown_sticker`.

## Changes in 0.9.3

Who can see a channel (needs Chat): `channel_viewers(cid)` is `GET /chat/channels/:cid/viewers` and answers `{"all": True}` when nothing limits who sees the channel, or `{"all": False, "ids": [...]}` with the user ids of the server members who can (you must be able to see the channel yourself, else 404).

## Changes in 0.9.2

Ember Beta status (needs Chat): `ember_beta()` is `GET /chat/beta` and answers `{beta, membership, product}`; `beta` is true only with a live active or trialing Ember Beta membership. `refresh_ember_beta()` is `POST /chat/beta/refresh`, the same answer without the 30 second cache.

## Changes in 0.9.1

New routes for Ember's Inbox, each with a `Client` helper and a one-method-per-route name (all need Chat unless noted):

| Helper | Route |
|---|---|
| `inbox_mentions(before=, limit=)` | `GET /chat/inbox/mentions`: the last 30 days of messages in your servers that mention you, newest first, with `channel_name`, `server_name`, `server_icon` and `unread` |
| `saved_messages(before=, limit=)` | `GET /chat/saved`: `{saved, has_more}`; entries can be `missing` (original gone) or `hidden` (a DM without Read Instant Messages) |
| `save_message(kind, message_id)` / `save_message("group", snapshot=...)` | `POST /chat/saved`: returns the saved id. `kind` is `channel`, `dm` (needs Read Instant Messages) or `group`. At most 500 (`too_many_saved`) |
| `unsave_message(saved_id)` | `DELETE /chat/saved/:id` |
| `saved_ids(kind, ids)` | `POST /chat/saved/check`: `{message id: saved id}` |
| `translate(text, to="en", source=None)` | `POST /chat/translate`: `{text, from, to}`; 3000 characters, 40 a minute |
| `cancel_friend_request(username)` | `DELETE /friends/request/:id` (Manage Friends) after finding the id in `outgoing` of `GET /friends/requests`; `True` when a pending request was taken back |

```python
for item in nookara.saved_messages()["saved"]:
    print(item["kind"], item.get("message") or "gone")
sid = nookara.save_message("channel", 123456)
nookara.unsave_message(sid)
print(nookara.translate("Bonjour!", "en")["text"])
```

## Changes in 0.9.0

**Breaking:** the Velora and Bonfire names are removed from the API. Rename them as below; there are no
aliases. Wire formats, routes and error codes don't change.

| Before | Now |
|---|---|
| `import velora_api` (and `velora_api.client` and the other modules) | `import nookara` |
| `Bonfire`, `velora_api.bonfire` | `Ember`, `nookara.ember` |
| `BONFIRE_APP_MASK`, `BONFIRE_APP_SCOPES` | `EMBER_APP_MASK`, `EMBER_APP_SCOPES` |
| `Instance.login_with_velora`, `register_with_velora`, `import_from_velora` | `login_with_nookara`, `register_with_nookara`, `import_from_nookara` |
| `Client.bonfire_instances`, `set_bonfire_instances`, `sync_bonfire_instances`, `bonfire_default_instance`, `bonfire_default_joined`, `bonfire_instance_prefs`, `bonfire_profiles`, `bonfire_key`, `bonfire_user_keys`, `bonfire_jwks`, `bonfire_payout`, `bonfire_import_platforms`, `bonfire_import_guilds`, `bonfire_import_job`, `bonfire_directory`, `bonfire_session`, `bonfire_scopes`, `start_bonfire_import` | the same with `ember` in place of `bonfire` |
| `velora_url=` (`Instance`, `BotProgram`) | `nookara_url=` |
| `velora_client=` / `velora=` keywords (`login_with_nookara`, `enable_signing`, `verify_message`, `Ember`) | pass the client as the first argument |
| `Instance.velora_origin`, `Ember.velora` | `nookara_origin`, `Ember.nookara` |

- Installing 0.9.0 over an older version removes the `velora_api` folder, so old imports fail with `ModuleNotFoundError`.
- The one-method-per-route names still follow the URL, so routes under `/bonfire/...` keep names like `get_bonfire_instances`.
- New: `RealtimeClient(token, origin=...)`. Nookara's socket only takes an app's token with one of the app's authorized URLs as the Origin, so pass the `origin` that `login_app` gave you.
- Examples use `NOOKARA_TOKEN` and `NOOKARA_BOT_TOKEN`, and sign in with `login_app`.

## Changes in 0.6.1

- Fix `bad_signature` when sending signed messages after the move to Nookara: `enable_signing()` now signs with the issuer the instance announces (`/.well-known/bonfire` `velora.issuer`, falling back to `https://velora.ikelene.net`) instead of the base URL you logged in through. `Instance.issuer()` returns it, and `verify_message()` accepts the announced issuer first, then the other known Nookara origins.

## Changes in 0.6.0

- Velora is now Nookara: the default base URL is `https://nookara.cc` (and `wss://nookara.cc/` for realtime). `velora.ikelene.net` keeps working for now; pass `base_url=` / `url=` to keep using it. The import name `velora_api` is unchanged, and a thin `nookara` package re-exports it (`import nookara`).

## Changes in 0.5.10

- DM files no longer go to catbox.moe. `upload_dm_file(path, destination="temp" | "account")` uploads to Nookara's
  temporary storage (`POST /chat/media/temp`, links at `https://nookara.cc/t/<id>/<name>`, the expiry resets
  on every load) or to your account storage (`POST /chat/media/account`). `upload_destinations()` /
  `get_chat_media_destinations()` says what's available and how much account space is left.
  `post_chat_media_external()` still works and now uploads to temporary storage too.

## Changes in 0.5.9

- Realtime: Nookara sends `user_update {user, changed, previous_username?, v}` on the user socket whenever someone you can see
  changes their profile (picture, banner, colour, pronouns, bio, website, country, username). It arrives through
  `async for event in socket` like any other frame; patch cached copies by `user["id"]`. No API change.

## Changes in 0.5.8

- Bot aliases: `alias=` on `Instance.bot_send`, `Instance.bot_edit` (`alias=None` clears), `Instance.send_message`,
  `Instance.edit_message` and `InstanceGateway.send_message`, plus `make_alias(name, avatar_url=None)` which checks
  the limits. `bot_edit` now takes `content` as optional so an alias can be changed alone. Nothing else changed.

## Changes in 0.5.7

- Notifications: new generated methods for `/account/notifications` (list, unread count, read, unread, delete),
  `/account/notification-settings` (GET, PATCH) and the staff `POST /admin/notifications/send`, helpers
  `notifications()`, `unread_notifications()`, `mark_notifications_read()`, `mark_notifications_unread()`,
  `delete_notification()`, `notification_settings()`, `set_notification_settings()`, and
  `RealtimeClient.notification_events()` with `NOTIFICATION_EVENT_TYPES` (`notification_new`, `notifications_updated`).
- System DMs (`from_system` messages) are no longer created; those messages are notifications now.

## Changes in 0.5.1

- New `get_chat_media_limits()`: the real upload limits (`server_mb` for files sent in a conversation, `saved_mb` for files kept
  on your Nookara account). `get_chat_unfurl()` can now return `payment` cards for Nookara payment links. Nothing else changed.

## Changes in 0.5.0

- New `BotClient` (bot token) with bot payment helpers: `create_payment_request`,
  `get_payment_request`, `find_payment_request`, `list_payment_requests`, `cancel_payment_request`,
  `wait_for_payment`, `is_paid`, plus the `PaymentError` family. The four `/bot/payment-requests`
  routes are also generated methods (`post_bot_payment_requests`, ...).
- Docs for bot presence and staff test installs (`test: true`). No behaviour changes elsewhere.

## Changes in 0.4.0

- Scopes are only requested: `login(scopes=...)` sends them as an optional request, the new
  `scopes` module and `Client.granted_scopes()/has_scope()/require_scope()` report what the
  person allowed, and calls without a scope raise `ScopeError` (an `APIError` subclass).
- Instance scopes (`chat`, `voice`, `media`, `sign`) from the ticket: `Instance.scopes`,
  `has_scope()`, `sign="auto"`, early `ScopeError` for uploads.
- New: `Bonfire` (your saved servers), `BotProgram` (a bot on every instance it is
  installed on), `verify_message`, invites, join requests, media import, channel and role
  helpers, game/bridge/admin helpers, instance info and build, Nookara helpers for profiles,
  keys, JWKS, scopes, import jobs, default server and push preferences.
- 458 Nookara and 169 instance operations as named methods.
- Legacy `Client.servers()/server()/messages()/send_message()` warn that Nookara-hosted chat is read-only.

## Encrypted direct messages

DMs are end-to-end encrypted, so `Client.send_dm` no longer sends plain text. A client makes its own keys and asks the person to approve it in Ember:

```python
from velora_api import EncryptedDMs

dms = EncryptedDMs(client, key_file="nookara-dms.json")  # pip install "nookara[signing]"
if not dms.linked():
    code = dms.request_link()
    print("In Ember: Settings > Privacy > Approve a device, and enter", code)
    dms.wait_for_approval(code)
dms.send("alice", "Hello!")
for m in dms.messages("alice"):
    print(m["from"], dms.open(m))
```

Before linking, the Direct Messages permission only gets locked messages and who/when. `key_file` holds your private keys: protect it like a password. People can unlink your client any time. Someone aged 13-15 can't give this permission to other people's Apps.
