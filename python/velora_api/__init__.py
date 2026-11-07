"""Old name of the nookara package. Use ``import nookara``; this one still works and warns."""
import sys
import warnings

import nookara
from nookara import *  # noqa: F401,F403
from nookara import __all__, __version__  # noqa: F401
from nookara import (_compat, _origin, _version, botpayments, botprogram, client, e2ee, ember, endpoints, instance,  # noqa: F401
                     instance_endpoints, instance_gateway, realtime, scopes, signing)

warnings.warn("velora_api is deprecated, use nookara", DeprecationWarning, stacklevel=2)

for _name, _module in {"_compat": _compat, "_origin": _origin, "_version": _version, "botpayments": botpayments,
                       "botprogram": botprogram, "client": client, "e2ee": e2ee, "bonfire": ember, "ember": ember,
                       "endpoints": endpoints, "instance": instance, "instance_endpoints": instance_endpoints,
                       "instance_gateway": instance_gateway, "realtime": realtime, "scopes": scopes, "signing": signing}.items():
    sys.modules[__name__ + "." + _name] = _module


def __getattr__(name):
    return getattr(nookara, name)
