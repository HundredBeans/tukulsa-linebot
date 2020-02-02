import re
from chatbot import bot_action


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
            "provider": "tri",
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


text = input()
nomor_pattern = r"08\d{9,11}"
nominal_pattern = r"\d+\s?ribu|\d+.000"
nomor = re.findall(nomor_pattern, text)
nominal = re.findall(nominal_pattern, text)
if len(nomor) > 0 and len(nominal) > 0:
    # Cek nominal tersebut ada ngga, sama nomornya valid apa ngga
    nomor_kode = nomor[0][:4]
    data_provider = cek_provider(nomor_kode)
    nominal = nominal[0].replace(" ", "").replace(
        "ribu", '000').replace(".", "").replace(",", "")
    if data_provider is not False:
        bot_message = "Yakin mau beli pulsa {} {} ke nomor {}?".format(
            data_provider["provider"], nominal, nomor[0])
    else:
        bot_message = "Nomornya ngga valid tuh kak, coba dicek lagi"
    print(bot_message)
