import base64
import hashlib
import re

import pytest

import nookara
from nookara import client as C


def test_app_link_login_uses_pkce_and_state(monkeypatch):
    calls = []

    def fake_request(self, method, path, json=None, auth=True, **kw):
        calls.append((method, path, json, auth))
        if path == "/auth/ext-code":
            return {"code": "c0de"}
        if path == "/auth/ext-code/exchange":
            want = base64.urlsafe_b64encode(hashlib.sha256(json["code_verifier"].encode()).digest()).rstrip(b"=").decode()
            assert want == calls[0][2]["code_challenge"]
            return {"token": "apptok", "scopes": 5}
        raise AssertionError(path)

    monkeypatch.setattr(C.Client, "request", fake_request)
    p = nookara.start_app_link_login("app_" + "a" * 20, "myapp://signed-in")
    start = calls[0][2]
    assert start["redirect_uri"] == "myapp://signed-in" and start["code_challenge_method"] == "S256"
    assert re.fullmatch(r"[A-Za-z0-9_-]{43}", start["code_challenge"]) and start["state"] == p.state
    assert p.url.endswith("/login?code=c0de") and calls[0][3] is False
    link = "myapp://signed-in?nookara_code=c0de&nookara_grant=" + "g" * 32 + "&state=" + p.state
    assert p.matches(link)
    with pytest.raises(ValueError):
        p.finish("myapp://signed-in?nookara_code=c0de&nookara_grant=" + "g" * 32 + "&state=other")
    assert p.finish(link) == ("apptok", 5)
    assert p.finish(grant="g" * 32) == ("apptok", 5)
    with pytest.raises(ValueError):
        p.finish(grant="x")
    with pytest.raises(ValueError):
        nookara.start_app_link_login("nope", "myapp://x")
