"""Charge a Nookara user from a bot (server side only).

    BOT_TOKEN=... python bot_payments.py alice 20

Never put the bot token in a Scratch/PenguinMod project, a web page or an app: anyone who has it can create
payment requests as your bot. The credits land in the balance of the bot's owner.
"""
import os
import sys

from velora_api import BotClient, BuyerError, OrderConflict, PaymentError, PaymentTimeout, is_paid

bot = BotClient(os.environ["BOT_TOKEN"])
buyer, amount = sys.argv[1], int(sys.argv[2])
order_id = "demo-" + buyer + "-1001"

try:
    request = bot.create_payment_request(buyer, amount, order_id, description="Premium pack",
                                         return_url="https://shop.example/done", expires_in=900)
except BuyerError as error:
    sys.exit("Cannot charge this buyer: " + error.error)
except OrderConflict:
    sys.exit("order_id already used for something else; pick a new one")
except PaymentError as error:
    sys.exit("Payment API error: " + error.error)

print("Send the buyer to:", request["pay_url"])

try:
    final = bot.wait_for_payment(request["id"], timeout=900, poll=3)
except PaymentTimeout as error:
    bot.cancel_payment_request(request["id"])
    sys.exit("No answer in time; cancelled")

if is_paid(final) and final["amount"] == amount:
    print("Paid, transaction", final["transaction_id"], "from buyer id", final["buyer"]["id"])
else:
    print("Not paid:", final["status"], final.get("reason", ""))
