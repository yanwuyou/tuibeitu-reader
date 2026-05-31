import re, json

# Map Chinese numerals to integers
CN_NUM = {c: i+1 for i, c in enumerate("一二三四五六七八九十")}
# Handle compound numbers like 十二, 二十, 三十, etc.
def parse_cn_num(s):
    s = s.strip()
    if s in CN_NUM:
        return CN_NUM[s]
    n = 0
    if s.startswith("十"):
        n = 10
        s = s[1:]
        if s: n += CN_NUM.get(s, 0)
    elif "十" in s:
        parts = s.split("十")
        n = CN_NUM.get(parts[0], 0) * 10
        if len(parts) > 1 and parts[1]:
            n += CN_NUM.get(parts[1], 0)
    return n

with open(r"E:\焱无忧知识库\02-领域\历史\推背图-金圣叹批注版-全文.md", encoding="utf-8") as f:
    text = f.read()

# Start from first 象
idx = text.index("## 第一象")
text = text[idx:]

# Split by "## 第" to get each image section
# First restore the marker
parts = text.split("## 第")
images = []

for part in parts:
    if not part.strip():
        continue

    # Restore the full header
    full = "## 第" + part

    # Extract image number and title - match Chinese numerals
    m = re.search(r"第(.+?)象 (.+?)\n", full)
    if not m:
        print(f"SKIP: no match for header in: {full[:80]}")
        continue

    cn_num = m.group(1).strip()
    xiang_num = parse_cn_num(cn_num)
    gan_zhi_title = m.group(2).strip()

    # Parse 干支（标题）
    gm = re.match(r"(.+?)（(.+?)）", gan_zhi_title)
    gan_zhi = gm.group(1) if gm else gan_zhi_title
    title = gm.group(2) if gm else ""

    # Extract 谶曰 content
    chen = ""
    song = ""
    jinpi = ""

    cm = re.search(r"\*\*谶曰：?\*\*\s*\n(.*?)(?=\n\*\*颂曰)", full, re.DOTALL)
    if cm:
        chen = cm.group(1).strip()

    sm = re.search(r"\*\*颂曰：?\*\*\s*\n(.*?)(?=\n\*\*金圣叹注解)", full, re.DOTALL)
    if sm:
        song = sm.group(1).strip()

    jm = re.search(r"\*\*金圣叹注解：?\*\*\s*\n?(.*?)$", full, re.DOTALL)
    if jm:
        jinpi = jm.group(1).strip()

    images.append({
        "id": xiang_num,
        "ganZhi": gan_zhi,
        "title": title,
        "chen": chen,
        "song": song,
        "jinPi": jinpi,
        "baiHua": "",
        "period": "",
        "startYear": None,
        "endYear": None
    })
    print(f"OK: 第{xiang_num}象 {gan_zhi}({title}) chen={len(chen)} song={len(song)} jinpi={len(jinpi)}")

print(f"\n解析到 {len(images)} 象")

with open(r"E:\推背图浏览器\data_raw.json", "w", encoding="utf-8") as f:
    json.dump(images, f, ensure_ascii=False, indent=2)
print("已写入 data_raw.json")
