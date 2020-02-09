import json

def detail_transaksi(display_name, order_id, created_at, payment_status, order_status, operator, nominal, phone_number, price, label, text_action):
    transaksi_json = {
  "type": "bubble",
  "body": {
    "layout": "vertical",
    "type": "box",
    "contents": [
      {
        "type": "box",
        "layout": "horizontal",
        "contents": [
          {
            "color": "#aaaaaa",
            "text": display_name,
            "type": "text",
            "wrap": True,
            "margin": "none",
            "size": "xs"
          },
          {
            "color": "#0b5b67",
            "text": "laporkan masalah",
            "type": "text",
            "wrap": True,
            "margin": "none",
            "size": "xs",
            "align": "end",
            "decoration": "underline",
            "action": {
              "type": "postback",
              "label": "action",
              "data": "laporkan masalah {}".format(order_id),
              "displayText": "masalah {}".format(order_id)
            }
          }
        ]
      },
      {
        "color": "#0b5b67",
        "text": "Detail Transaksi",
        "type": "text",
        "weight": "bold",
        "size": "sm"
      },
      {
        "weight": "bold",
        "text": order_id,
        "align": "center",
        "type": "text",
        "wrap": True,
        "margin": "md",
        "size": "xl"
      },
      {
        "layout": "vertical",
        "spacing": "sm",
        "margin": "xs",
        "type": "box",
        "contents": [
          {
            "layout": "horizontal",
            "margin": "none",
            "type": "box",
            "contents": [
              {
                "color": "#aaaaaa",
                "text": created_at,
                "align": "center",
                "type": "text",
                "size": "xs"
              }
            ]
          },
          {
            "margin": "md",
            "type": "separator"
          },
          {
            "layout": "horizontal",
            "margin": "xl",
            "type": "box",
            "contents": [
              {
                "flex": 0,
                "weight": "bold",
                "color": "#0b5b67",
                "text": "Status",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "layout": "horizontal",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Pembayaran",
                "type": "text",
                "flex": 0,
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": payment_status,
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "layout": "horizontal",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Pemesanan (Pulsa)",
                "type": "text",
                "flex": 0,
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": order_status,
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "margin": "xxl",
            "type": "separator"
          },
          {
            "layout": "horizontal",
            "margin": "xxl",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Operator",
                "type": "text",
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": operator,
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "layout": "horizontal",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Nominal",
                "type": "text",
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": nominal,
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "layout": "horizontal",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Nomor Tujuan",
                "type": "text",
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": phone_number,
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          },
          {
            "layout": "horizontal",
            "type": "box",
            "contents": [
              {
                "color": "#555555",
                "text": "Harga",
                "type": "text",
                "size": "sm"
              },
              {
                "color": "#111111",
                "text": "Rp {}".format(price),
                "align": "end",
                "type": "text",
                "size": "sm"
              }
            ]
          }
        ]
      },
      {
        "margin": "xxl",
        "type": "separator"
      },
      {
        "action": {
          "text": text_action,
          "type": "message",
          "label": label
        },
        "margin": "lg",
        "style": "primary",
        "type": "button",
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