import pandas as pd

data = pd.read_csv("packet_data.txt")
rows = []

def is_local(ip):
    return ip.startswith("192.168.10.")

def get_last_octet(ip):
    return int(ip.split(".")[3])

for idx, row in data.iterrows():
    ip_a = row["Address A"].strip('"')
    ip_b = row["Address B"].strip('"')
    bytes_val = row["Bytes"]
    a_local = is_local(ip_a)
    b_local = is_local(ip_b)
    
    if a_local and not b_local:
        rows.append({"Local IP": ip_a, "Other Host IP": ip_b, "Bytes": bytes_val})
    elif b_local and not a_local:
        rows.append({"Local IP": ip_b, "Other Host IP": ip_a, "Bytes": bytes_val})
    elif a_local and b_local:
        rows.append({"Local IP": ip_a, "Other Host IP": ip_b, "Bytes": bytes_val})
        rows.append({"Local IP": ip_b, "Other Host IP": ip_a, "Bytes": bytes_val})

sorted = pd.DataFrame(rows)
sorted["last_octet"] = sorted["Local IP"].apply(get_last_octet)
sorted_data = sorted.sort_values(by=["last_octet", "Bytes"], ascending=[True, False])
sorted_data = sorted_data.drop(columns="last_octet")

sorted_data.to_csv("packet_data.csv", index=False)





