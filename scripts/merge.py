import json

# Read the data from JSON (cleaner)
with open(r"E:\推背图浏览器\data_raw.json", encoding="utf-8") as f:
    data = json.load(f)

data_js = "const TUI_BEI_DATA = " + json.dumps(data, ensure_ascii=False, indent=2) + ";"

# Read HTML template
with open(r"E:\推背图浏览器\tuibeitu.html", encoding="utf-8") as f:
    html = f.read()

# Replace placeholder
html = html.replace("const TUI_BEI_DATA = __DATA_PLACEHOLDER__;", data_js)

# Write final file
with open(r"E:\推背图浏览器\tuibeitu.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"Merged: {len(data)} images, {len(html)} bytes total")
