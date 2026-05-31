#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update baiHua field for items 41-60 in data_raw.json.
Uses a separate JSON data file to avoid quoting issues.
"""

import json

DATA_FILE = r"E:\推背图浏览器\data_raw.json"
BAIHUA_FILE = r"E:\推背图浏览器\scripts\baihua_41_60.json"


def main():
    # Load baihua data
    with open(BAIHUA_FILE, "r", encoding="utf-8") as f:
        baihua = json.load(f)

    # Convert keys to int
    baihua = {int(k): v for k, v in baihua.items()}

    # Load main data
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Update items
    updated = 0
    for item in data:
        item_id = item.get("id")
        if item_id in baihua:
            item["baiHua"] = baihua[item_id]
            updated += 1

    # Write back
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Done! Updated {updated} records (items 41-60).")


if __name__ == "__main__":
    main()
