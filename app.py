# -*- coding: utf-8 -*-

#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.

from __future__ import unicode_literals

import re
import datetime
import errno
import json
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort, send_from_directory
from werkzeug.middleware.proxy_fix import ProxyFix

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    LineBotApiError, InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    MemberJoinedEvent, MemberLeftEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton,
    ImageSendMessage)
# chatbot
from chatbot import bot_reply, context_chat
# feature
from feature import cek_provider
# endpoint
from endpoint import get_chat_info, update_all, update_nominal, update_number, get_product_by, post_user, get_midtrans_url, get_alltransactions_by, get_latesttransaction_by, get_security_code
# flex template
from flexTemplate import detail_transaksi, daftar_operator, daftar_pulsa_awal, daftar_pulsa_akhir




app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1, x_proto=1)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None or channel_access_token is None:
    print('Specify LINE_CHANNEL_SECRET and LINE_CHANNEL_ACCESS_TOKEN as environment variables.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')


# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except LineBotApiError as e:
        print("Got exception from LINE Messaging API: %s\n" % e.message)
        for m in e.error.details:
            print("  %s: %s" % (m.property, m.message))
        print("\n")
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """
    Handle Message Event from LINE Callback
    """
    text = event.message.text
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    display_name = profile.display_name
    user_status = profile.status_message
    # add user into backend database
    add_user = post_user(user_id, display_name)
    # Pattern nomor dan nominal pulsa
    nomor_pattern = r"08\d{9,11}"
    nominal_pattern = r"\d+\s?ribu|\d+.?000"
    nomor = re.findall(nomor_pattern, text)
    nominal = re.findall(nominal_pattern, text)
    ###### RESPONSE FLOW FOR BUYING PULSA (INPUT AND CONFIRMING) ######
    if len(nomor) == 1 and len(nominal) == 1:
        nomor_kode = nomor[0][:4]
        data_provider = cek_provider(nomor_kode)
        nominal = nominal[0].replace(" ", "").replace(
            "ribu", '000').replace(".", "").replace(",", "")
        if data_provider is not False:
            # Update chat status
            status = update_all(user_id, nomor[0], nominal, True, True, data_provider["provider"])
            bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                    data_provider["provider"], nominal, nomor[0])
            # Create confirm template
            confirm_template = ConfirmTemplate(text=bot_message, actions=[
                MessageAction(label= 'Yakin', text='yakin'),
                MessageAction(label= 'Batal', text='gajadi')
            ])
            template_message = TemplateSendMessage(
                alt_text='Konfirmasi Pembelian', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)

        else:
            bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"
            template_message = TextSendMessage(text=bot_message)
            line_bot_api.reply_message(event.reply_token, template_message)

    elif len(nomor) == 1:
        # Cek provider dari nomor tersebut
        nomor_kode = nomor[0][:4]
        data_provider = cek_provider(nomor_kode)
        # GET Nominal status
        status = get_chat_info(user_id)
        ### Cek apakah user sudah ngasih info nominal ###
        if status['status_nominal'] and data_provider is not False:
            # Update nomor ke backend
            update = update_number(user_id, nomor[0], True, data_provider['provider'])
            bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                data_provider["provider"], status['nominal'], nomor[0])
            # Create confirm template
            confirm_template = ConfirmTemplate(text=bot_message, actions=[
                MessageAction(label= 'Yakin', text='yakin'),
                MessageAction(label= 'Batal', text='gajadi')
            ])
            template_message = TemplateSendMessage(
                alt_text='Konfirmasi Pembelian', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)
        
        elif data_provider is not False:
            # Update nomor ke backend
            update = update_number(user_id, nomor[0], True, data_provider['provider'])
            bot_message = "Silahkan dipilih pulsa {}nya kak".format(data_provider["provider"])
            reply_message = TextSendMessage(text=bot_message)
            # GET Produk filter by provider
            list_product = get_product_by(data_provider["provider"])
            # Create Flex Carousel Template
            bubble_string = daftar_pulsa_awal(list_product)
            # Convert dict into string
            json_input = json.dumps(bubble_string)
            message = FlexSendMessage(
                alt_text="Daftar Produk", contents=json.loads(json_input))
            line_bot_api.reply_message(
                event.reply_token,[reply_message, message]
            )

        else:
            bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"
            template_message = TextSendMessage(text=bot_message)
            line_bot_api.reply_message(event.reply_token, template_message)
    
    elif len(nominal) == 1:
        # Format nominal jadi angka doang
        nominal = nominal[0].replace(" ", "").replace(
            "ribu", '000').replace(".", "").replace(",", "")
        # Update nominal ke backend
        update = update_nominal(user_id, nominal, True)
        nominal = '{:,}'.format(int(nominal))
        nominal = nominal.replace(',', '.')
        if update['status_number']:
            nomor_user = update['phone_number']
            nomor_kode = nomor_user[:4]
            data_provider = cek_provider(nomor_kode)
            bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                data_provider["provider"], nominal, nomor_user)
            # Create confirm template
            confirm_template = ConfirmTemplate(text=bot_message, actions=[
                MessageAction(label= 'Yakin', text='yakin'),
                MessageAction(label= 'Batal', text='gajadi')
            ])
            template_message = TemplateSendMessage(
                alt_text='Konfirmasi Pembelian', template=confirm_template)
            line_bot_api.reply_message(event.reply_token, template_message)
            
        else:
            bot_message = "Beli pulsa {} ke nomor apa ya kak?".format(nominal)
            template_message = TextSendMessage(text=bot_message)
            line_bot_api.reply_message(event.reply_token, template_message)

    # List Product by operator #    
    elif text == "telkomsel":
        bot_message = "Berikut daftar pulsa {}nya kak".format('telkomsel')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('telkomsel')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )

    elif text == "indosat":
        bot_message = "Berikut daftar pulsa {}nya kak".format('indosat')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('indosat')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )
    
    elif text == "xl":
        bot_message = "Berikut daftar pulsa {}nya kak".format('xl')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('xl')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )
    
    elif text == "three":
        bot_message = "Berikut daftar pulsa {}nya kak".format('three')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('three')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )
    
    elif text == "axis":
        bot_message = "Berikut daftar pulsa {}nya kak".format('axis')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('axis')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )
    
    elif text == "smartfren":
        bot_message = "Berikut daftar pulsa {}nya kak".format('smartfren')
        reply_message = TextSendMessage(text=bot_message)
        # GET Produk filter by provider
        list_product = get_product_by('smart')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_awal(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,[reply_message, message]
        )
    elif text == "yakin":
    # Check if user already send Phone Number and Nominal info
        status = get_chat_info(user_id)
        if status["status_number"] and status["status_nominal"]:
            # POST Transaction ke Backend Tukulsa #
            nomor = status['phone_number']
            nomor_kode = nomor[:4]
            nominal = status['nominal']
            data_provider = cek_provider(nomor_kode)
            operator = data_provider["provider"]
            if operator == "xl":
                product_code = "xld{}".format(nominal)
            else:
                product_code = "h{}{}".format(operator, nominal)
            midtrans_url = get_midtrans_url(user_id, nomor, product_code)['link_payment']
            ######################################
            bot_message_1 = "Silahkan klik tombol di bawah untuk melakukan pembayaran"
            buttons_template = ButtonsTemplate(text = bot_message_1, actions=[
                URIAction(label='Bayar', uri=midtrans_url),
                MessageAction(label="Cek Status", text="cek status pembelian")
            ])
            template_message = TemplateSendMessage(
                alt_text='Konfirmasi Pembayaran', template=buttons_template)
            bot_message_2 = "Untuk cek status transaksi, bisa chat 'cek status pembelian' kapan aja atau bisa klik tombol cek status di bawah"
            message_2 = TextSendMessage(text=bot_message_2)
            reset = update_all(user_id, "", "", False, False, "")
            line_bot_api.reply_message(event.reply_token, [message_2, template_message])
        elif status['status_number']:
            bot_message = "kamu belum ngasih tau nominal pulsanya"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
        elif status['status_nominal']:
            bot_message = "kamu belum ngasih tau nomor hp yang dituju"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
        else:
            bot_message = "kamu belum ngasih tau nomor sama nominal pulsa yang mau dibeli"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
    elif text == "gajadi":
        status = get_chat_info(user_id)
        if status['status_number'] and status['status_nominal']:
            bot_message = "Pembelian pulsa {} {} ke {} dibatalkan ya ka".format(status['operator'], status['nominal'], status['phone_number'])
            # Reset status #
            reset = update_all(user_id, "", "", False, False, "")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=bot_message))
        else:
            bot_message = "Batal apa ya ka? \nKak {}, sedang tidak dalam proses transaksi".format(display_name)
            bot_message_2 = "Biar yakin, bisa dicek status transaksi dengan chat 'cek status transaksi' kapan aja"
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=bot_message), TextSendMessage(text=bot_message_2)])
    else:
        # chatbot
        context = bot_reply(text)
        if context == "complaint":
            reply_message = context_chat[context]
            # Tambahin reply isinya status transaksi terakhir
            message = TextSendMessage(text=reply_message)
            line_bot_api.reply_message(event.reply_token, message)
        elif context == "cek produk":
            reply_message = context_chat[context]
            # Generate Flex from flexTemplate
            bot_message = TextSendMessage(text=reply_message)
            bubble_string = daftar_operator()
            # Convert dict into string
            json_input = json.dumps(bubble_string)
            message = FlexSendMessage(
                alt_text="Daftar Produk", contents=json.loads(json_input))
            line_bot_api.reply_message(
                event.reply_token,[bot_message, message]
            )
        elif context == "cek riwayat":
            reply_message = context_chat[context].format(display_name)
            # Get Transaction from Backend
            latest_transaction = get_latesttransaction_by(user_id)
            price = '{:,}'.format(latest_transaction['price'])
            price = price.replace(',', '.')
            nominal = '{:,}'.format(latest_transaction['nominal'])
            nominal = nominal.replace(',', '.')
            # Define each variable
            order_id = latest_transaction['order_id']
            created_at = latest_transaction['created_at']
            payment_status = latest_transaction['payment_status']
            order_status = latest_transaction['order_status']
            operator = latest_transaction['operator']
            phone_number = latest_transaction['phone_number']
            # Make Flex Message
            if latest_transaction['payment_status'] == 'LUNAS' and latest_transaction['order_status'] == 'SUKSES':
                text_action = "{} {}".format(phone_number, nominal)
                label = "Beli Lagi"
                bubble_string = detail_transaksi(display_name, order_id, created_at, payment_status, order_status, operator, nominal, phone_number, price, label, text_action )
                # Convert dict into string
                json_input = json.dumps(bubble_string)
                message = FlexSendMessage(
                    alt_text="Detail Transaksi", contents=json.loads(json_input))
                line_bot_api.reply_message(
                    event.reply_token,
                    message
                )
            else:
                text_action = "cek status pembelian"
                label = "Cek Status"
                bubble_string = detail_transaksi(display_name, order_id, created_at, payment_status, order_status, operator, nominal, phone_number, price, label, text_action)
                # Convert dict into string
                json_input = json.dumps(bubble_string)
                message = FlexSendMessage(
                    alt_text="Detail Transaksi", contents=json.loads(json_input))
                line_bot_api.reply_message(
                    event.reply_token,
                    message
                )
        elif context == "admin login":
            code = get_security_code(user_id)['code']
            bot_message = context_chat[context].format(display_name)
            line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=bot_message), TextSendMessage(text=code)])
        else:
            reply_message = context_chat[context]
            # Tambahin display name ke dalam message
            formatted_message = reply_message.format(display_name)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=formatted_message))
    # Other LINE Feature
    # if text == 'profile':
    #     if isinstance(event.source, SourceUser):
    #         profile = line_bot_api.get_profile(event.source.user_id)
    #         line_bot_api.reply_message(
    #             event.reply_token, [
    #                 TextSendMessage(text='Display name: ' +
    #                                 profile.display_name),
    #                 TextSendMessage(text='Status message: ' +
    #                                 str(profile.status_message))
    #             ]
    #         )
    #     else:
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text="Bot can't use profile API without user ID"))
    # elif text == 'quota':
    #     quota = line_bot_api.get_message_quota()
    #     line_bot_api.reply_message(
    #         event.reply_token, [
    #             TextSendMessage(text='type: ' + quota.type),
    #             TextSendMessage(text='value: ' + str(quota.value))
    #         ]
    #     )
    # elif text == 'quota_consumption':
    #     quota_consumption = line_bot_api.get_message_quota_consumption()
    #     line_bot_api.reply_message(
    #         event.reply_token, [
    #             TextSendMessage(text='total usage: ' +
    #                             str(quota_consumption.total_usage)),
    #         ]
    #     )
    # elif text == 'push':
    #     line_bot_api.push_message(
    #         event.source.user_id, [
    #             TextSendMessage(text='PUSH!'),
    #         ]
    #     )
    # elif text == 'multicast':
    #     line_bot_api.multicast(
    #         [event.source.user_id], [
    #             TextSendMessage(text='THIS IS A MULTICAST MESSAGE'),
    #         ]
    #     )
    # elif text == 'broadcast':
    #     line_bot_api.broadcast(
    #         [
    #             TextSendMessage(text='THIS IS A BROADCAST MESSAGE'),
    #         ]
    #     )
    # elif text.startswith('broadcast '):  # broadcast 20190505
    #     date = text.split(' ')[1]
    #     print("Getting broadcast result: " + date)
    #     result = line_bot_api.get_message_delivery_broadcast(date)
    #     line_bot_api.reply_message(
    #         event.reply_token, [
    #             TextSendMessage(
    #                 text='Number of sent broadcast messages: ' + date),
    #             TextSendMessage(text='status: ' + str(result.status)),
    #             TextSendMessage(text='success: ' + str(result.success)),
    #         ]
    #     )
    # elif text == 'bye':
    #     if isinstance(event.source, SourceGroup):
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text='Leaving group'))
    #         line_bot_api.leave_group(event.source.group_id)
    #     elif isinstance(event.source, SourceRoom):
    #         line_bot_api.reply_message(
    #             event.reply_token, TextSendMessage(text='Leaving group'))
    #         line_bot_api.leave_room(event.source.room_id)
    #     else:
    #         line_bot_api.reply_message(
    #             event.reply_token,
    #             TextSendMessage(text="Bot can't leave from 1:1 chat"))
    # elif text == 'image':
    #     url = request.url_root + '/static/sepulsa.png'
    #     app.logger.info("url=" + url)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         ImageSendMessage(url, url)
    #     )
    # elif text == 'confirm':
    #     confirm_template = ConfirmTemplate(text='Do it?', actions=[
    #         MessageAction(label='Yes', text='Yes!'),
    #         MessageAction(label='No', text='No!'),
    #     ])
    #     template_message = TemplateSendMessage(
    #         alt_text='Confirm alt text', template=confirm_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    # elif text == 'buttons':
    #     buttons_template = ButtonsTemplate(
    #         title='My buttons sample', text='Hello, my buttons', actions=[
    #             URIAction(label='Go to line.me', uri='https://line.me'),
    #             PostbackAction(label='ping', data='ping'),
    #             PostbackAction(label='ping with text',
    #                            data='ping', text='ping'),
    #             MessageAction(label='Translate Rice', text='米')
    #         ])
    #     template_message = TemplateSendMessage(
    #         alt_text='Buttons alt text', template=buttons_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    # elif text == 'carousel':
    #     carousel_template = CarouselTemplate(columns=[
    #         CarouselColumn(text='hoge1', title='fuga1', actions=[
    #             URIAction(label='Go to line.me', uri='https://line.me'),
    #             PostbackAction(label='ping', data='ping')
    #         ]),
    #         CarouselColumn(text='hoge2', title='fuga2', actions=[
    #             PostbackAction(label='ping with text',
    #                            data='ping', text='ping'),
    #             MessageAction(label='Translate Rice', text='米')
    #         ]),
    #     ])
    #     template_message = TemplateSendMessage(
    #         alt_text='Carousel alt text', template=carousel_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    # elif text == 'image_carousel':
    #     image_carousel_template = ImageCarouselTemplate(columns=[
    #         ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
    #                             action=DatetimePickerAction(label='datetime',
    #                                                         data='datetime_postback',
    #                                                         mode='datetime')),
    #         ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
    #                             action=DatetimePickerAction(label='date',
    #                                                         data='date_postback',
    #                                                         mode='date'))
    #     ])
    #     template_message = TemplateSendMessage(
    #         alt_text='ImageCarousel alt text', template=image_carousel_template)
    #     line_bot_api.reply_message(event.reply_token, template_message)
    # elif text == 'imagemap':
    #     pass
    # elif text == 'flex':
    #     bubble = BubbleContainer(
    #         direction='ltr',
    #         hero=ImageComponent(
    #             url='https://example.com/cafe.jpg',
    #             size='full',
    #             aspect_ratio='20:13',
    #             aspect_mode='cover',
    #             action=URIAction(uri='http://example.com', label='label')
    #         ),
    #         body=BoxComponent(
    #             layout='vertical',
    #             contents=[
    #                 # title
    #                 TextComponent(text='Brown Cafe', weight='bold', size='xl'),
    #                 # review
    #                 BoxComponent(
    #                     layout='baseline',
    #                     margin='md',
    #                     contents=[
    #                         IconComponent(
    #                             size='sm', url='https://example.com/gold_star.png'),
    #                         IconComponent(
    #                             size='sm', url='https://example.com/grey_star.png'),
    #                         IconComponent(
    #                             size='sm', url='https://example.com/gold_star.png'),
    #                         IconComponent(
    #                             size='sm', url='https://example.com/gold_star.png'),
    #                         IconComponent(
    #                             size='sm', url='https://example.com/grey_star.png'),
    #                         TextComponent(text='4.0', size='sm', color='#999999', margin='md',
    #                                       flex=0)
    #                     ]
    #                 ),
    #                 # info
    #                 BoxComponent(
    #                     layout='vertical',
    #                     margin='lg',
    #                     spacing='sm',
    #                     contents=[
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text='Place',
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text='Shinjuku, Tokyo',
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5
    #                                 )
    #                             ],
    #                         ),
    #                         BoxComponent(
    #                             layout='baseline',
    #                             spacing='sm',
    #                             contents=[
    #                                 TextComponent(
    #                                     text='Time',
    #                                     color='#aaaaaa',
    #                                     size='sm',
    #                                     flex=1
    #                                 ),
    #                                 TextComponent(
    #                                     text="10:00 - 23:00",
    #                                     wrap=True,
    #                                     color='#666666',
    #                                     size='sm',
    #                                     flex=5,
    #                                 ),
    #                             ],
    #                         ),
    #                     ],
    #                 )
    #             ],
    #         ),
    #         footer=BoxComponent(
    #             layout='vertical',
    #             spacing='sm',
    #             contents=[
    #                 # callAction, separator, websiteAction
    #                 SpacerComponent(size='sm'),
    #                 # callAction
    #                 ButtonComponent(
    #                     style='link',
    #                     height='sm',
    #                     action=URIAction(label='CALL', uri='tel:000000'),
    #                 ),
    #                 # separator
    #                 SeparatorComponent(),
    #                 # websiteAction
    #                 ButtonComponent(
    #                     style='link',
    #                     height='sm',
    #                     action=URIAction(
    #                         label='WEBSITE', uri="https://example.com")
    #                 )
    #             ]
    #         ),
    #     )
    #     message = FlexSendMessage(alt_text="hello", contents=bubble)
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         message
    #     )
    # elif text == 'flex_update_1':
    #     bubble_string = """
    #     {
    #       "type": "bubble",
    #       "body": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #           {
    #             "type": "image",
    #             "url": "https://line-objects-dev.com/flex/bg/eiji-k-1360395-unsplash.jpg",
    #             "position": "relative",
    #             "size": "full",
    #             "aspectMode": "cover",
    #             "aspectRatio": "1:1",
    #             "gravity": "center"
    #           },
    #           {
    #             "type": "box",
    #             "layout": "horizontal",
    #             "contents": [
    #               {
    #                 "type": "box",
    #                 "layout": "vertical",
    #                 "contents": [
    #                   {
    #                     "type": "text",
    #                     "text": "Brown Hotel",
    #                     "weight": "bold",
    #                     "size": "xl",
    #                     "color": "#ffffff"
    #                   },
    #                   {
    #                     "type": "box",
    #                     "layout": "baseline",
    #                     "margin": "md",
    #                     "contents": [
    #                       {
    #                         "type": "icon",
    #                         "size": "sm",
    #                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    #                       },
    #                       {
    #                         "type": "icon",
    #                         "size": "sm",
    #                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    #                       },
    #                       {
    #                         "type": "icon",
    #                         "size": "sm",
    #                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    #                       },
    #                       {
    #                         "type": "icon",
    #                         "size": "sm",
    #                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gold_star_28.png"
    #                       },
    #                       {
    #                         "type": "icon",
    #                         "size": "sm",
    #                         "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/review_gray_star_28.png"
    #                       },
    #                       {
    #                         "type": "text",
    #                         "text": "4.0",
    #                         "size": "sm",
    #                         "color": "#d6d6d6",
    #                         "margin": "md",
    #                         "flex": 0
    #                       }
    #                     ]
    #                   }
    #                 ]
    #               },
    #               {
    #                 "type": "box",
    #                 "layout": "vertical",
    #                 "contents": [
    #                   {
    #                     "type": "text",
    #                     "text": "¥62,000",
    #                     "color": "#a9a9a9",
    #                     "decoration": "line-through",
    #                     "align": "end"
    #                   },
    #                   {
    #                     "type": "text",
    #                     "text": "¥42,000",
    #                     "color": "#ebebeb",
    #                     "size": "xl",
    #                     "align": "end"
    #                   }
    #                 ]
    #               }
    #             ],
    #             "position": "absolute",
    #             "offsetBottom": "0px",
    #             "offsetStart": "0px",
    #             "offsetEnd": "0px",
    #             "backgroundColor": "#00000099",
    #             "paddingAll": "20px"
    #           },
    #           {
    #             "type": "box",
    #             "layout": "vertical",
    #             "contents": [
    #               {
    #                 "type": "text",
    #                 "text": "SALE",
    #                 "color": "#ffffff"
    #               }
    #             ],
    #             "position": "absolute",
    #             "backgroundColor": "#ff2600",
    #             "cornerRadius": "20px",
    #             "paddingAll": "5px",
    #             "offsetTop": "10px",
    #             "offsetEnd": "10px",
    #             "paddingStart": "10px",
    #             "paddingEnd": "10px"
    #           }
    #         ],
    #         "paddingAll": "0px"
    #       }
    #     }
    #     """
    #     message = FlexSendMessage(
    #         alt_text="hello", contents=json.loads(bubble_string))
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         message
    #     )
    # elif text == 'quick_reply':
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(
    #             text='Quick reply',
    #             quick_reply=QuickReply(
    #                 items=[
    #                     QuickReplyButton(
    #                         action=PostbackAction(label="label1", data="data1")
    #                     ),
    #                     QuickReplyButton(
    #                         action=MessageAction(label="label2", text="text2")
    #                     ),
    #                     QuickReplyButton(
    #                         action=DatetimePickerAction(label="label3",
    #                                                     data="data3",
    #                                                     mode="date")
    #                     ),
    #                     QuickReplyButton(
    #                         action=CameraAction(label="label4")
    #                     ),
    #                     QuickReplyButton(
    #                         action=CameraRollAction(label="label5")
    #                     ),
    #                     QuickReplyButton(
    #                         action=LocationAction(label="label6")
    #                     ),
    #                 ])))
    # elif text == 'link_token' and isinstance(event.source, SourceUser):
    #     link_token_response = line_bot_api.issue_link_token(
    #         event.source.user_id)
    #     line_bot_api.reply_message(
    #         event.reply_token, [
    #             TextSendMessage(text='link_token: ' +
    #                             link_token_response.link_token)
    #         ]
    #     )
    # elif text == 'insight_message_delivery':
    #     today = datetime.date.today().strftime("%Y%m%d")
    #     response = line_bot_api.get_insight_message_delivery(today)
    #     if response.status == 'ready':
    #         messages = [
    #             TextSendMessage(text='broadcast: ' + str(response.broadcast)),
    #             TextSendMessage(text='targeting: ' + str(response.targeting)),
    #         ]
    #     else:
    #         messages = [TextSendMessage(text='status: ' + response.status)]
    #     line_bot_api.reply_message(event.reply_token, messages)
    # elif text == 'insight_followers':
    #     today = datetime.date.today().strftime("%Y%m%d")
    #     response = line_bot_api.get_insight_followers(today)
    #     if response.status == 'ready':
    #         messages = [
    #             TextSendMessage(text='followers: ' + str(response.followers)),
    #             TextSendMessage(text='targetedReaches: ' +
    #                             str(response.targeted_reaches)),
    #             TextSendMessage(text='blocks: ' + str(response.blocks)),
    #         ]
    #     else:
    #         messages = [TextSendMessage(text='status: ' + response.status)]
    #     line_bot_api.reply_message(event.reply_token, messages)
    # elif text == 'insight_demographic':
    #     response = line_bot_api.get_insight_demographic()
    #     if response.available:
    #         messages = ["{gender}: {percentage}".format(gender=it.gender, percentage=it.percentage)
    #                     for it in response.genders]
    #     else:
    #         messages = [TextSendMessage(text='available: false')]
    #     line_bot_api.reply_message(event.reply_token, messages)
    # else:
    #     line_bot_api.reply_message(
    #         event.reply_token, TextSendMessage(text=event.message.text))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title='Location', address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )


@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )


# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url +
                            os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url +
                            os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    app.logger.info("Got Follow event:" + event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='Got follow event'))


@handler.add(UnfollowEvent)
def handle_unfollow(event):
    app.logger.info("Got Unfollow event:" + event.source.user_id)


@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))


@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    display_name = profile.display_name
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
    elif event.postback.data == "yakin":
    # Check if user already send Phone Number and Nominal info
        status = get_chat_info(user_id)
        if status["status_number"] and status["status_nominal"]:
            # POST Transaction ke Backend Tukulsa #
            nomor = status['phone_number']
            nomor_kode = nomor[:4]
            nominal = status['nominal']
            data_provider = cek_provider(nomor_kode)
            operator = data_provider["provider"]
            if operator == "xl":
                product_code = "xld{}".format(nominal)
            else:
                product_code = "h{}{}".format(operator, nominal)
            midtrans_url = get_midtrans_url(user_id, nomor, product_code)['link_payment']
            ######################################
            bot_message_1 = "Silahkan klik tombol di bawah untuk melakukan pembayaran"
            buttons_template = ButtonsTemplate(text = bot_message_1, actions=[
                URIAction(label='Bayar', uri=midtrans_url),
                PostbackAction(label="Cek Status", data="cek status")
            ])
            template_message = TemplateSendMessage(
                alt_text='Konfirmasi Pembayaran', template=buttons_template)
            bot_message_2 = "Untuk cek status transaksi, bisa chat 'cek status pembelian' kapan aja atau bisa klik tombol cek status di atas"
            message_2 = TextSendMessage(text=bot_message_2)
            reset = update_all(user_id, "", "", False, False, "")
            line_bot_api.reply_message(event.reply_token, [template_message, message_2])
        elif status['status_number']:
            bot_message = "kamu belum ngasih tau nominal pulsanya"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
        elif status['status_nominal']:
            bot_message = "kamu belum ngasih tau nomor hp yang dituju"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
        else:
            bot_message = "kamu belum ngasih tau nomor sama nominal pulsa yang mau dibeli"
            line_bot_api.reply_message(event.reply_token, TextSendMessage(bot_message))
    elif event.postback.data == "gajadi":
        status = get_chat_info(user_id)
        if status['status_number'] and status['status_nominal']:
            bot_message = "Pembelian pulsa {} {} ke {} dibatalkan ya ka".format(status['operator'], status['nominal'], status['phone_number'])
            # Reset status #
            reset = update_all(user_id, "", "", False, False, "")
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=bot_message))
        else:
            bot_message = "Batal apa ya ka? \nKak {}, sedang tidak dalam proses transaksi. \nBiar yakin, bisa dicek status transaksi dengan chat 'cek status transaksi' kapan aja".format(display_name)
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text=bot_message))

    elif event.postback.data == "cek status":
        reply_message = "Berikut adalah status transaksi yang terbaru ya kak"
        latest_transaction = get_latesttransaction_by(user_id)
        text_latest_trx = '''Status Transaksi ({}) : \nPulsa : {} \nHarga : Rp {} \nNomor : {} \nStatus pembayaran: {} \nStatus pemesanan (pulsa) : {}'''.format(latest_transaction['created_at'], latest_transaction['label'], latest_transaction['price'], latest_transaction['phone_number'], latest_transaction['payment_status'], latest_transaction['order_status'])
        line_bot_api.reply_message(event.reply_token, [TextSendMessage(text=reply_message), TextSendMessage(text=text_latest_trx)])
    # GET Postback from list product
    elif event.postback.data == "Telkomsel":
        # GET Produk filter by provider
        list_product = get_product_by('telkomsel')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )
    elif event.postback.data == "Indosat":
        # GET Produk filter by provider
        list_product = get_product_by('indosat')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )
    elif event.postback.data == "XL":
        # GET Produk filter by provider
        list_product = get_product_by('xl')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )
    elif event.postback.data == "Three":
        # GET Produk filter by provider
        list_product = get_product_by('three')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )
    elif event.postback.data == "AXIS":
        # GET Produk filter by provider
        list_product = get_product_by('axis')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )
    elif event.postback.data == "Smart":
        # GET Produk filter by provider
        list_product = get_product_by('smart')
        # Create Flex Carousel Template
        bubble_string = daftar_pulsa_akhir(list_product)
        # Convert dict into string
        json_input = json.dumps(bubble_string)
        message = FlexSendMessage(
            alt_text="Daftar Produk", contents=json.loads(json_input))
        line_bot_api.reply_message(
            event.reply_token,message
        )

@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


@handler.add(MemberJoinedEvent)
def handle_member_joined(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got memberJoined event. event={}'.format(
                event)))


@handler.add(MemberLeftEvent)
def handle_member_left(event):
    app.logger.info("Got memberLeft event")


@app.route('/static/<path:path>')
def send_static_content(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', type=int,
                            default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    # create tmp dir for download content
    make_static_tmp_dir()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
