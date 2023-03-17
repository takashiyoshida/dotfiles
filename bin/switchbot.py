#!/usr/bin/env python

import argparse
import base64
import hashlib
import hmac
import json
import os
import requests
import time


def main():
    parser = argparse.ArgumentParser(prog="switchbot.py")
    parser.add_argument(
        "-t",
        "--token",
        required=False,
        default="",
        help="SwitchBot API token",
        dest="token",
    )
    parser.add_argument(
        "-s",
        "--secret",
        required=False,
        default="",
        help="SwitchBot API secret",
        dest="secret",
    )
    parser.add_argument(
        "-n",
        "--nonce",
        required=False,
        default="",
        help="Nonce",
        dest="nonce",
    )
    subparsers = parser.add_subparsers(dest="command", help="sub-command help")
    devices_parser = subparsers.add_parser("devices", help="get SwitchBot device list")

    args = parser.parse_args()

    if args.token == "" and "SWITCHBOT_TOKEN" in os.environ:
        args.token = os.environ["SWITCHBOT_TOKEN"]
    if args.secret == "" and "SWITCHBOT_SECRET" in os.environ:
        args.secret = os.environ["SWITCHBOT_SECRET"]

    for key, value in vars(args).items():
        print(f"{key}: {value}")

    if args.command == "devices":
        try:
            ts = int(round(time.time() * 1000))
            string_to_sign = "{}{}{}".format(args.token, ts, args.nonce)
            string_to_sign = string_to_sign.encode("utf-8")
            secret = bytes(args.secret, "utf-8")

            sign = base64.b64encode(
                hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
            )

            response = requests.get(
                url="https://api.switch-bot.com/v1.1/devices",
                headers={
                    "Authorization": args.token,
                    "sign": sign,
                    "t": str(ts),
                    "nonce": args.nonce,
                },
            )
            print(
                "Response HTTP status code: {status_code}".format(
                    status_code=response.status_code
                )
            )
            print("Response HTTP response body:")
            print(json.dumps(json.loads(response.content), indent=2))
        except requests.exceptions.RequestException as e:
            print("HTTP request failed: {e}".format(e=e))

    pass


if __name__ == "__main__":
    main()
