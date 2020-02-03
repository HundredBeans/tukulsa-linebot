import re
import requests


def cek_provider(nomor):
    daftar_operator = [
        {
            "prodvider": "telkomsel",
            "no_provider": 1,
            "nomor": ["0811", "0812", "0813", "0821", "0822", "0852", "0853", "0823", "0851"],
        },
        {
            "provider": "indosat",
            "no_provider": 2,
            "nomor": ["0814", "0815", "0816", "0855", "0856", "0857", "0858"],
        },
        {
            "provider": "xl",
            "no_provider": 3,
            "nomor": ["0817", "0818", "0819", "0859", "0877", "0878"],
        },
        {
            "provider": "axis",
            "no_provider": 4,
            "nomor": ["0838", "0831", "0832", "0833"],
        },
        {
            "provider": "three",
            "no_provider": 5,
            "nomor": ["0895", "0896", "0897", "0898", "0899"],
        },
        {
            "provider": "smartfren",
            "no_provider": 6,
            "nomor": ["0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"],
        }
    ]
    for operator in daftar_operator:
        if nomor in operator["nomor"]:
            return operator
    return False

# ##### FLOW INPUT NOMOR DAN NOMINAL ######
# nomor_pattern = r"08\d{9,11}"
# nominal_pattern = r"\d+\s?ribu|\d+.000"
# nomor = re.findall(nomor_pattern, text)
# nominal = re.findall(nominal_pattern, text)
# if len(nomor) == 1 and len(nominal) == 1:
#     # Cek nominal tersebut ada ngga, sama nomornya valid apa ngga
#     nomor_kode = nomor[0][:4]
#     data_provider = cek_provider(nomor_kode)
#     nominal = nominal[0].replace(" ", "").replace(
#         "ribu", '000').replace(".", "").replace(",", "")
#     if data_provider is not False:
#         # update_status = requests.post() # update status ke backend

#         ###### Buat Lokal #######
#         user_status["status_nomor"] = True
#         user_status["status_nominal"] = True
#         user_status["nomor"] = nomor[0]
#         user_status["nominal"] = nominal
#         #########################
#         bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
#             data_provider["provider"], nominal, nomor[0])
#     else:
#         bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"
#     print(bot_message)

# elif len(nomor) == 1:
#     # Cek provider dari nomor tersebut
#     nomor_kode = nomor[0][:4]
#     data_provider = cek_provider(nomor_kode)
#     ### Cek apakah user sudah ngasih info nominal ###
#     # user_info = requests.get()
#     if user_status["status_nominal"] and data_provider is not False:
#         # update_status_nomor = requests.post() # Update nomor ke backend

#         #### Buat Lokal ####
#         user_status["status_nomor"] = True
#         user_status["nomor"] = nomor[0]
#         ######################

#         bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
#             data_provider["provider"], user_status["nominal"], nomor[0])

#     elif data_provider is not False:
#         # update_status_nomor = requests.post() # Update nomor ke backend

#         #### Buat Lokal ####
#         user_status["status_nomor"] = True
#         user_status["nomor"] = nomor[0]
#         ######################

#         # Get product filter by provider
#         # Keluarin message action berupa carousel dari macem macem product tersebut
#         bot_message = "Silahkan dipilih nominal pulsanya kak"
#     else:
#         bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"

# elif len(nominal) == 1:
#     # Format nominal jadi angka doang
#     nominal = nominal[0].replace(" ", "").replace(
#         "ribu", '000').replace(".", "").replace(",", "")
#     # update status nominal
#     # update_status_nominal = requests.post()
    
#     ####### Buat Lokal #########
#     user_status["status_nominal"] = True
#     user_status["nominal"] = nominal
#     # cari info apakah user sudah masukin nomor sebelumnya
#     # user_info = requests.get()
#     if user_status["status_nomor"]:
#         bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
#             data_provider["provider"], nominal, user_status["nomor"])
    
#     else:
#         bot_message = "Beli pulsa {} ke nomor apa ya kak?".format(nominal)

# ### FLOW KONFIRMASI PEMBELIAN PULSA ###
# if text == "yakin 100%":
#     # Cek kalo user itu sudah ada data nomor dan nominal
#     # user_info = requests.get()

#     if user_status["status_nomor"] and user_status["status_nominal"]:
#         bot_message = "Silahkan klik tombol di bawah untuk melakukan pembayaran"
#         # Nembak requests ke mobile pulsa #
#         # Reset status nominal #
#         ####### Buat Lokal #######
#         user_status["status_nominal"] = False
#         user_status["nominal"] = ""
#         ###########################

#     else:
#         bot_message = "apanya yang yakin 100%?"

# elif text == "gajadi deh":
#     bot_message = "Oh yaudah gapapa kak"
#     # Reset status nominal #
#     ####### Buat Lokal #######
#     user_status["status_nominal"] = False
#     user_status["nominal"] = ""
#     ###########################


##################################### TESTING LOKAL ########################################
# User-Info Lokal
user_status = {
    "status_nomor":False,
    "status_nominal":False,
    "nomor":"",
    "nominal":""
}

def testing_flow():
    while True:
        if user_status["status_nomor"] == False and user_status["status_nominal"] == False:
            print("status nomor dan nominal adalah False")
        text = input()
        ##### FLOW INPUT NOMOR DAN NOMINAL ######
        nomor_pattern = r"08\d{9,11}"
        nominal_pattern = r"\d+\s?ribu|\d+.000"
        nomor = re.findall(nomor_pattern, text)
        nominal = re.findall(nominal_pattern, text)
        if len(nomor) == 1 and len(nominal) == 1:
            # Cek nominal tersebut ada ngga, sama nomornya valid apa ngga
            nomor_kode = nomor[0][:4]
            data_provider = cek_provider(nomor_kode)
            nominal = nominal[0].replace(" ", "").replace(
                "ribu", '000').replace(".", "").replace(",", "")
            if data_provider is not False:
                # update_status = requests.post() # update status ke backend

                ###### Buat Lokal #######
                user_status["status_nomor"] = True
                user_status["status_nominal"] = True
                user_status["nomor"] = nomor[0]
                user_status["nominal"] = nominal
                #########################
                bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                    data_provider["provider"], nominal, nomor[0])
            else:
                bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"

        elif len(nomor) == 1:
            # Cek provider dari nomor tersebut
            nomor_kode = nomor[0][:4]
            data_provider = cek_provider(nomor_kode)
            ### Cek apakah user sudah ngasih info nominal ###
            # user_info = requests.get()
            if user_status["status_nominal"] and data_provider is not False:
                # update_status_nomor = requests.post() # Update nomor ke backend

                #### Buat Lokal ####
                user_status["status_nomor"] = True
                user_status["nomor"] = nomor[0]
                ######################

                bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                    data_provider["provider"], user_status["nominal"], nomor[0])

            elif data_provider is not False:
                # update_status_nomor = requests.post() # Update nomor ke backend

                #### Buat Lokal ####
                user_status["status_nomor"] = True
                user_status["nomor"] = nomor[0]
                ######################

                # Get product filter by provider
                # Keluarin message action berupa carousel dari macem macem product tersebut
                bot_message = "Silahkan dipilih nominal pulsanya kak"
            else:
                bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"

        elif len(nominal) == 1:
            # Format nominal jadi angka doang
            nominal = nominal[0].replace(" ", "").replace(
                "ribu", '000').replace(".", "").replace(",", "")
            # update status nominal
            # update_status_nominal = requests.post()
            
            ####### Buat Lokal #########
            user_status["status_nominal"] = True
            user_status["nominal"] = nominal
            # cari info apakah user sudah masukin nomor sebelumnya
            # user_info = requests.get()
            if user_status["status_nomor"]:
                bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
                    data_provider["provider"], nominal, user_status["nomor"])
            
            else:
                bot_message = "Beli pulsa {} ke nomor apa ya kak?".format(nominal)

        ### FLOW KONFIRMASI PEMBELIAN PULSA ###
        elif text == "yakin 100%":
            # Cek kalo user itu sudah ada data nomor dan nominal
            # user_info = requests.get()

            if user_status["status_nomor"] and user_status["status_nominal"]:
                bot_message = "Silahkan klik tombol di bawah untuk melakukan pembayaran"
                # Nembak requests ke mobile pulsa #
                # Reset status nominal #
                ####### Buat Lokal #######
                user_status["status_nominal"] = False
                user_status["status_nomor"] = False
                user_status["nominal"] = ""
                user_status["nomor"] = ""
                ###########################

            else:
                bot_message = "apanya yang yakin 100%?"

        elif text == "gajadi deh":
            bot_message = "Oh yaudah gapapa kak"
            # Reset status nominal #
            ####### Buat Lokal #######
            user_status["status_nominal"] = False
            user_status["status_nomor"] = False
            user_status["nominal"] = ""
            user_status["nomor"] = ""
            ###########################
        print(bot_message)

testing_flow()