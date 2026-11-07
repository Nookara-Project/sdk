"""Post to a Ember channel through a webhook URL. No account, no login.

Make the webhook in the channel settings (Webhooks) and keep the URL secret:

    BONFIRE_WEBHOOK_URL=https://chat.ikelene.net/api/v1/webhooks/ID/TOKEN python bonfire_webhook.py
"""
import os

from nookara import APIError, execute_webhook

try:
    execute_webhook(os.environ["BONFIRE_WEBHOOK_URL"], "Build finished", username="Build service")
except APIError as exc:
    print(exc.status, exc.error, exc.retry_after)
