"""Your Ember servers as one object: the saved instance list of a Nookara account.

A person's Ember servers (``chat.ikelene.net``, Nookara-hosted ``e-<slug>.nookara.cc`` ones, self-hosted
ones) are saved on their Nookara account so they follow them between devices. ``Ember`` reads that list,
signs in to each instance with a ticket made for that one instance, and gives you ``Instance`` objects and the
joined communities. Servers that are down, read-only or in local-account mode are reported, never fatal.

    nookara = Client(token)                # needs Chat (2048)
    ember = Ember(nookara, sign="auto")
    for entry in ember.communities():
        print(entry["instance"], entry["community"]["name"], entry["error"])
"""
from __future__ import annotations

from ._origin import normalize_origin
from .client import APIError, ScopeError, TransportError
from .instance import Instance


class Ember:
    """The Ember servers of one Nookara account."""

    def __init__(self, nookara, *, sign=False, timeout=30, allow_insecure=False, instance_factory=None):
        self.nookara = nookara
        self.sign = sign
        self.timeout, self.allow_insecure = timeout, allow_insecure
        self._factory = instance_factory or (lambda url: Instance(url, timeout=timeout, allow_insecure=allow_insecure,
                                                                  nookara_url=nookara.base_url))
        self._instances = {}

    def urls(self):
        """The saved instance addresses in the account's order."""
        return [item["url"] for item in self.nookara.ember_instances()]

    def entries(self):
        """Saved list entries: ``{url, position, added_at, muted, push, auto_join}``."""
        return self.nookara.ember_instances()

    def add(self, url):
        """Remember a server on the account (this is what "joining a server" in the apps starts with)."""
        return self.nookara.sync_ember_instances([normalize_origin(url, allow_insecure=self.allow_insecure)])

    def remove(self, url):
        origin = normalize_origin(url, allow_insecure=self.allow_insecure)
        keep = [u for u in self.urls() if u != origin]
        self._instances.pop(origin, None)
        return self.nookara.set_ember_instances(keep)

    def directory(self, q=None, page=None):
        """Search the public directory of servers that chose to be listed."""
        return self.nookara.ember_directory(q, page)

    def instance(self, url):
        """A signed-in ``Instance`` for one server of the list (cached). Raises ``APIError`` / ``ScopeError`` /
        ``ValueError`` (local-account servers cannot use a Nookara ticket)."""
        origin = normalize_origin(url, allow_insecure=self.allow_insecure)
        inst = self._instances.get(origin)
        if inst is None:
            inst = self._factory(origin)
            if inst.accounts_mode == "local":
                raise ValueError(origin + " uses its own accounts; sign in with Instance.login()")
            inst.login_with_nookara(self.nookara, sign=self.sign)
            self._instances[origin] = inst
        return inst

    def communities(self, urls=None):
        """Every joined community across the list. Each item is ``{instance, community, instance_info, error}``;
        ``community`` is None when you are not a member (or the server failed) and ``error`` says why:
        ``unreachable``, ``read_only`` is not an error (see ``instance_info["read_only"]``), ``local_accounts``,
        ``chat_scope_missing`` (you declined Chat) or an API error code."""
        out = []
        for url in (urls if urls is not None else self.urls()):
            item = {"instance": url, "community": None, "instance_info": None, "error": None}
            try:
                inst = self.instance(url)
                item["instance_info"] = inst.info
                joined = inst.joined_communities()
                item["community"] = joined[0] if joined else None
            except ScopeError:
                item["error"] = "chat_scope_missing"
            except APIError as exc:
                item["error"] = str(exc.error)
            except TransportError:
                item["error"] = "unreachable"
            except ValueError as exc:
                item["error"] = "local_accounts" if "own accounts" in str(exc) else "invalid_instance"
            out.append(item)
        return out

    def join_default(self):
        """Join the official server once and tell Nookara, as the Ember apps do: it is added to every account
        and ``auto_join`` stays true until a client confirms. Returns the community or None when nothing to do."""
        listing = self.nookara.get_bonfire_instances()
        default = listing.get("default_instance")
        entry = next((i for i in listing["instances"] if i["url"] == default), None)
        if not default or not entry or not entry.get("auto_join"):
            return None
        inst = self.instance(default)
        joined = inst.join()
        self.nookara.ember_default_joined(default)
        return joined

    def close(self):
        for inst in self._instances.values():
            try:
                inst.logout()
            except (APIError, TransportError):
                pass
        self._instances.clear()
