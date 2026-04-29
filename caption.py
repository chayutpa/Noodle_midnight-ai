from __future__ import annotations

import os

from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPICallError, ResourceExhausted

load_dotenv(dotenv_path=".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "models/gemini-2.5-flash")


def configure_genai() -> None:
    """ตั้งค่า API key สำหรับ Google Generative AI."""
    if not GOOGLE_API_KEY:
        raise RuntimeError("กรุณาใส่ GOOGLE_API_KEY ในไฟล์ .env")
    genai.configure(api_key=GOOGLE_API_KEY)


def build_prompt(menu_name: str, price: str) -> str:
    """สร้าง prompt ภาษาไทยสำหรับให้โมเดลเขียน caption แบบกันเอง."""
    return (
        "เขียน caption Instagram เป็นภาษาไทย สำหรับร้าน MilkLab cafe\n"
        "ให้มีโทนเป็นกันเอง อ่านแล้วน่ารัก ไม่เป็นทางการ และสั้นกระชับ\n"
        "สร้าง 3 แบบดังนี้:\n"
        "1. สไตล์น่ารัก\n"
        "2. สไตล์มินิมอล\n"
        "3. สไตล์เจน-ซี\n"
        f"ชื่อเมนู: {menu_name}\n"
        f"ราคา: {price}\n"
        "ตอบเป็นรายการที่แยกแต่ละบรรทัด และใส่หัวข้อสั้น ๆ ก่อนแต่ละแบบ"
    )


def generate_captions(menu_name: str, price: str) -> str:
    """เรียกใช้งานโมเดลเพื่อสร้าง caption แบบภาษาไทย."""
    configure_genai()
    model = genai.GenerativeModel(model_name=MODEL_NAME)
    prompt = build_prompt(menu_name, price)
    try:
        response = model.generate_content(prompt)
    except ResourceExhausted as exc:
        raise RuntimeError(
            "โควต้าการใช้งาน API หมดแล้ว กรุณารอ แล้วลองใหม่ หรือเช็กแผนการใช้งาน Google AI ของคุณ"
        ) from exc
    except GoogleAPICallError as exc:
        raise RuntimeError(
            "เกิดข้อผิดพลาดจาก Google AI API: "
            + str(exc)
            + "\nลองตรวจสอบคีย์, โควต้าหรือชื่อโมเดลอีกครั้ง"
        ) from exc
    return getattr(response, "text", str(response))


def main() -> None:
    """อ่านข้อมูลจากผู้ใช้และแสดง caption ภาษาไทยแบบเป็นกันเอง."""
    menu_name = input("ชื่อเมนู: ").strip() or "ลาเต้เย็น"
    price = input("ราคา: ").strip() or "95 บาท"

    print("\nกำลังสร้าง caption แบบภาษาไทยให้เลยนะ...\n")
    try:
        captions = generate_captions(menu_name, price)
    except RuntimeError as exc:
        print(f"เกิดปัญหา: {exc}")
        return
    print(captions)


if __name__ == "__main__":
    main()
