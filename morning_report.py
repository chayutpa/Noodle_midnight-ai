from __future__ import annotations

from collections import Counter
from datetime import date, timedelta
import os

import requests
from dotenv import load_dotenv

from sheets_client import get_sheet


def is_header_row(row: list[str]) -> bool:
    if not row:
        return False
    return row[0].strip().lower() in {"วันที่", "date", "day"} and len(row) >= 4


def parse_row(row: list[str]) -> tuple[str, str, int, float, float]:
    if len(row) < 4:
        raise ValueError("แถวข้อมูลไม่ครบ: ต้องมีอย่างน้อย วันที่, เมนู, จำนวน, ราคา")

    sale_date = row[0].strip()
    menu = row[1].strip()
    quantity = int(row[2].strip())
    price = float(row[3].strip())
    total = float(row[4].strip()) if len(row) >= 5 and row[4].strip() else quantity * price
    return sale_date, menu, quantity, price, total


def build_summary(rows: list[list[str]], yesterday: str) -> str:
    yesterday_rows = []
    for row in rows:
        if is_header_row(row):
            continue
        if not row or row[0].strip() != yesterday:
            continue

        try:
            sale_date, menu, quantity, price, total = parse_row(row)
        except ValueError:
            continue
        yesterday_rows.append((menu, quantity, price, total))

    if not yesterday_rows:
        return f"ไม่มีรายการขายของเมื่อวานนี้เลย "

    total_revenue = sum(item[3] for item in yesterday_rows)
    total_items = sum(item[1] for item in yesterday_rows)
    menu_counter = Counter()
    menu_revenue = Counter()
    for menu, qty, price, total in yesterday_rows:
        menu_counter[menu] += qty
        menu_revenue[menu] += total

    best_menu, best_qty = menu_counter.most_common(1)[0]
    best_value = menu_revenue[best_menu]

    lines = [
        f"สรุปยอดขายเมื่อวานนี้ ({yesterday}) ☀️",
        f"รวมทั้งหมด {total_items} ชิ้น ยอดรวม {total_revenue:.2f} บาท 💸",
        f"เมนูขายดีสุด: {best_menu} ({best_qty} ชิ้น) ยอด {best_value:.2f} บาท ❤️",
        "\nรายละเอียด:"
    ]

    for menu, qty, price, total in yesterday_rows:
        lines.append(f"- {menu}: {qty} x {price:.2f} = {total:.2f} บาท")

    lines.append("\nขอให้วันนี้ชีวิตมีรสชาติ กลมกล่อมและแซ่บลงตัวเหมือนก๋วยเตี๋ยวชามโปรดนะครับ 🔥🍜")
    return "\n".join(lines)


def send_telegram_message(token: str, chat_id: str, message: str) -> None:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()


def main() -> int:
    load_dotenv()

    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        raise RuntimeError("ต้องกำหนด TELEGRAM_BOT_TOKEN และ TELEGRAM_CHAT_ID ใน .env")

    sheet = get_sheet()
    rows = sheet.get_all_values()
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    message = build_summary(rows, yesterday)

    send_telegram_message(bot_token, chat_id, message)
    print("ส่งสรุปไปยัง Telegram เรียบร้อยแล้ว 🎉")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
