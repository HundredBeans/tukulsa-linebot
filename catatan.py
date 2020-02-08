import re

pattern_complaint = r"laporkan masalah TUKULSAORDER.?-\d+"
pattern_order = r"TUKULSAORDER.?-\d+"
order_id = re.findall(pattern_complaint, "laporkan masalah TUKULSAORDER-1")
print(order_id)