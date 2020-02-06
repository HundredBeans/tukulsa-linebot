import json

def detail_transaksi(display_name, order_id, created_at, payment_status, order_status, operator, nominal, phone_number, price, label, text_action):
    transaksi_json = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                    {
                        "type": "text",
                        "size": "xs",
                        "color": "#aaaaaa",
                        "wrap": True,
                        "margin": "none",
                        "text": display_name
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
                        "text": order_id,
                        "weight": "bold",
                        "size": "xl",
                        "margin": "md",
                        "wrap": True,
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
                                "text": created_at,
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
                                "text": payment_status,
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
                                "text": order_status,
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
                                "text": operator,
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
                                "text": nominal,
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
                                "text": phone_number,
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
                                "text": "Rp {}".format(price),
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
                        "label": label,
                        "text": text_action
                        },
                        "style": "primary",
                        "margin": "lg",
                        "color": "#0b5b67"
                    }
                    ]
                },
                "styles": {
                    "footer": {
                    "separator": True
                    }
                }
                }
    return transaksi_json

def daftar_operator():
    operator_json = {
  "type": "carousel",
  "contents": [
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/telkomsel.png",
            "size": "5xl",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetBottom": "30px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "telkomsel"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/indosat.png",
            "size": "5xl",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetBottom": "30px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "indosat"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/xl.png",
            "size": "xxl",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetBottom": "10px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "xl"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/three.png",
            "size": "lg",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetTop": "15px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "three"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/axis.png",
            "size": "xxl",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetBottom": "10px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "axis"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    },
    {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "image",
            "url": "https://developer.mobilepulsa.net/assets/images/products/smartfren.png",
            "size": "5xl",
            "aspectMode": "fit",
            "aspectRatio": "1:1",
            "gravity": "center",
            "offsetBottom": "30px"
          },
          {
            "type": "box",
            "layout": "horizontal",
            "contents": [
              {
                "type": "box",
                "layout": "vertical",
                "contents": [
                  {
                    "type": "button",
                    "action": {
                      "type": "message",
                      "label": "Daftar Pulsa",
                      "text": "smartfren"
                    },
                    "style": "primary",
                    "color": "#0b5b67"
                  }
                ],
                "spacing": "xs"
              }
            ],
            "position": "absolute",
            "offsetBottom": "0px",
            "offsetStart": "0px",
            "offsetEnd": "0px",
            "paddingAll": "20px"
          }
        ],
        "paddingAll": "0px"
      }
    }
  ]
}
    return operator_json

def detail_pulsa(image, operator, nominal, price, valid_to, raw_nominal):
    list_json = {
      "type": "bubble",
      "header": {
        "type": "box",
        "layout": "vertical",
        "contents": [
          {
            "type": "text",
            "text": "Copyright © 2020 Tukulsa",
            "color": "#0b5b67",
            "size": "xxs"
          }
        ]
      },
      "hero": {
        "type": "image",
        "url": image,
        "size": "full",
        "aspectRatio": "20:13",
        "aspectMode": "fit"
      },
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "md",
        "contents": [
          {
            "type": "text",
            "text": "{} {}".format(operator, nominal),
            "size": "xl",
            "weight": "bold",
            "align": "start"
          },
          {
            "type": "box",
            "layout": "vertical",
            "spacing": "sm",
            "contents": [
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "Harga",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "size": "sm"
                  },
                  {
                    "type": "text",
                    "text": "Rp {}".format(price),
                    "size": "sm",
                    "align": "end"
                  }
                ]
              },
              {
                "type": "box",
                "layout": "baseline",
                "contents": [
                  {
                    "type": "text",
                    "text": "Masa Berlaku",
                    "weight": "bold",
                    "margin": "sm",
                    "flex": 0,
                    "size": "sm"
                  },
                  {
                    "type": "text",
                    "text": "{} Hari".format(valid_to),
                    "size": "sm",
                    "align": "end"
                  }
                ]
              }
            ]
          },
          {
            "type": "box",
            "layout": "vertical",
            "contents": [
              {
                "type": "spacer",
                "size": "xxl"
              },
              {
                "type": "button",
                "style": "primary",
                "color": "#0b5b67",
                "action": {
                  "type": "message",
                  "label": "Pilih",
                  "text": raw_nominal
                }
              }
            ]
          }
        ]
      }
    }
    
    return list_json

def daftar_pulsa_awal(list_product):
    list_json = []
    for product in list_product[:9]:
        price = '{:,}'.format(int(product['price']))
        price = price.replace(',', '.')
        if len(product['nominal']) > 8:
            nominal = product['nominal']
        else:
            nominal = '{:,}'.format(int(product['nominal']))
            nominal = nominal.replace(',', '.')
        detail_product = detail_pulsa(product['image'], product['operator'], nominal, price, product['valid_to'], product['nominal'])
        list_json.append(detail_product)
    lainnya = {
      "type": "bubble",
      "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "button",
            "flex": 1,
            "gravity": "center",
            "action": {
              "type": "postback",
              "label": "Lihat Lainnya",
              "data": list_product[0]['operator']
            }
          }
        ]
      }
    }
    list_json.append(lainnya)
    pulsa_json = {
  "type": "carousel",
  "contents": list_json
}
    return pulsa_json

def daftar_pulsa_akhir(list_product):
    list_json = []
    for product in list_product[9:]:
        price = '{:,}'.format(int(product['price']))
        price = price.replace(',', '.')
        if len(product['nominal']) > 8:
            nominal = product['nominal']
        else:
            nominal = '{:,}'.format(int(product['nominal']))
            nominal = nominal.replace(',', '.')
        detail_product = detail_pulsa(product['image'], product['operator'], nominal, price, product['valid_to'], product['nominal'])
        list_json.append(detail_product)
    pulsa_json = {
  "type": "carousel",
  "contents": list_json
}
    return pulsa_json