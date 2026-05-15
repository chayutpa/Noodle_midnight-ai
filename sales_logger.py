from __future__ import annotations

import sys
from datetime import date
from typing import Sequence

from dotenv import load_dotenv

from sheets_client import get_sheet


def parse_sale_entry(entry: str) -> tuple[str, int, float]:
    parts = entry.strip().split(":")
    if len(parts) != 3:
        raise ValueError(
            "รูปแบบไม่ถูกต้อง: ต้องเป็น เมนู:จำนวน:ราคา เช่น กาแฟ:2:45.50"
        )

    menu, quantity_str, price_str = parts
    if not menu:
        raise ValueError("เมนูต้องไม่ว่าง")

    try:
        quantity = int(quantity_str)
    except ValueError as exc:
        raise ValueError("จำนวนต้องเป็นจำนวนเต็ม") from exc

    try:
        price = float(price_str)
    except ValueError as exc:
        raise ValueError("ราคาต้องเป็นตัวเลข") from exc

    return menu, quantity, price


def main(argv: Sequence[str] | None = None) -> int:
    argv = argv if argv is not None else sys.argv

    load_dotenv()

    if len(argv) >= 2:
        entry = argv[1]
    else:
        entry = input("กรุณาใส่ยอดขายในรูปแบบ เมนู:จำนวน:ราคา: ").strip()

    menu, quantity, price = parse_sale_entry(entry)
    total = quantity * price
    today = date.today().isoformat()

    sheet = get_sheet()
    sheet.append_row([today, menu, str(quantity), f"{price:.2f}", f"{total:.2f}"])

    print(
        f"เพิ่มยอดขายเรียบร้อย: วันที่={today}, เมนู={menu}, จำนวน={quantity}, ราคา={price:.2f}, ยอดรวม={total:.2f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
