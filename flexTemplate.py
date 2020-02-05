import re
from datetime import datetime, timedelta
def flex_template(waktu, status_pembayaran, order_status, operator, nominal, nomor_handphone, harga, order_id):
    bubble_string = """
    {
    "type": "bubble",
    "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
        {
            "type": "text",
            "size": "xs",
            "color": "#aaaaaa",
            "wrap": true,
            "margin": "none",
            "text": "{}"
        },
        {
            "type": "text",
            "text": "Detail Transaksi",
            "weight": "bold",
            "color": "#0b5b67",
            "size": "sm"
        },
        {
            "type": "text",
            "text": "{}",
            "weight": "bold",
            "size": "xl",
            "margin": "md",
            "wrap": true,
            "align": "center"
        },
        {
            "type": "box",
            "layout": "vertical",
            "margin": "xs",
            "spacing": "sm",
            "contents": [
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "{}",
                    "size": "xs",
                    "align": "center",
                    "color": "#aaaaaa"
                }
                ],
                "margin": "none"
            },
            {
                "type": "separator",
                "margin": "md"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Status",
                    "size": "sm",
                    "color": "#0b5b67",
                    "flex": 0,
                    "weight": "bold"
                }
                ],
                "margin": "xl"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Pembayaran",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Pemesanan (Pulsa)",
                    "size": "sm",
                    "color": "#555555",
                    "flex": 0
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            },
            {
                "type": "separator",
                "margin": "xxl"
            },
            {
                "type": "box",
                "layout": "horizontal",
                "margin": "xxl",
                "contents": [
                {
                    "type": "text",
                    "text": "Operator",
                    "size": "sm",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Nominal",
                    "size": "sm",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Nomor Tujuan",
                    "size": "sm",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            },
            {
                "type": "box",
                "layout": "horizontal",
                "contents": [
                {
                    "type": "text",
                    "text": "Harga",
                    "size": "sm",
                    "color": "#555555"
                },
                {
                    "type": "text",
                    "text": "{}",
                    "size": "sm",
                    "color": "#111111",
                    "align": "end"
                }
                ]
            }
            ]
        },
        {
            "type": "separator",
            "margin": "xxl"
        },
        {
            "type": "button",
            "action": {
            "type": "message",
            "label": "Beli Lagi",
            "text": "{} {}"
            },
            "style": "primary",
            "margin": "lg",
            "color": "#0b5b67"
        }
        ]
    },
    "styles": {
        "footer": {
        "separator": true
        }
    }
    }
    """.format(display_name, latest_transaction['order_id'], latest_transaction['created_at'], latest_transaction['payment_status'], latest_transaction['order_status'], latest_transaction['operator'], nominal, latest_transaction['phone_number'], price, latest_transaction['phone_number']), latest_transaction['nominal']
    message = FlexSendMessage(
        alt_text="Detail Transaksi", contents=json.loads(bubble_string))
    line_bot_api.reply_message(
        event.reply_token,
        message
    )