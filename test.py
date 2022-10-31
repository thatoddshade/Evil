import src.settings as st
for item in st.item_data.items():
    #print(item["name"] + "," + item["max_stack"] + ", " + item["lore"])
    print('"' + item[1]["name"] + '",', str(item[1]["max_stack"]) + ",", '"""' + item[1]["lore"] + '"""')
