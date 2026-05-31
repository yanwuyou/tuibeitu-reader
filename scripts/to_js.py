import json

with open(r"E:\推背图浏览器\data_raw.json", encoding="utf-8") as f:
    data = json.load(f)

js = "const TUI_BEI_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"

with open(r"E:\推背图浏览器\data.js", "w", encoding="utf-8") as f:
    f.write(js)

print(f"Generated data.js with {len(data)} images, {len(js)} bytes")
