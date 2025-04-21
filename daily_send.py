from fpdf import FPDF
import requests
import os
from datetime import datetime
import unicodedata
import base64

def debug(msg):
    print("[DEBUG]", msg)

# Odstranění diakritiky
def remove_diacritics(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

# PDF generátor
class TradingPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Denní obchodní návrh - Kaitotrader", ln=True, align="C")
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Stránka {self.page_no()}", 0, 0, "C")

    def add_trade_idea(self, title, content):
        self.set_font("Arial", "B", 11)
        self.cell(0, 10, title, ln=True)
        self.set_font("Arial", "", 10)
        self.multi_cell(0, 10, content)
        self.ln()

try:
    debug("Generuji PDF...")
    pdf = TradingPDF()
    pdf.add_page()
    pdf.add_trade_idea("Ticker: QQQ", remove_diacritics(
        "Styl: Konzervativní\n"
        "Strategie: Credit Spread (Call)\n"
        "Vstup: 8:45-9:15 EST (14:45-15:15 CET)\n"
        "Strike: 430/435\n"
        "Pravdepodobnost uspechu: 78 %\n"
        "RRR: 1:2\n"
        "Zadani do IBKR: Sell 1 QQQ 430 Call, Buy 1 QQQ 435 Call\n"
        "Cilovy zisk: 60 USD, max. riziko: 40 USD\n"
        "Vystoupit pri: 75 % z max zisku nebo blizici se expiraci\n"
        "Komentar: Rustove momentum zpomaluje, vhodne pro vstup do mirne medvediho setupu."
    ))

    filename = f"kaitotrader_navrh_{datetime.today().strftime('%Y%m%d')}.pdf"
    pdf.output(filename)
    debug(f"PDF vygenerován: {filename}")

    with open(filename, "rb") as f:
        encoded = base64.b64encode(f.read()).decode('utf-8')

    debug("Odesílám e-mail...")
    response = requests.post("https://kaitotrader-email.onrender.com/send-email", json={
        "to": "jan.jordan@email.cz",
        "subject": f"Kaitotrader – Navrh obchodu ({datetime.today().strftime('%d.%m.%Y')})",
        "message": "Viz prilozeny obchodni navrh ve formatu PDF.",
        "filename": filename,
        "filecontent_base64": encoded
    })

    print("Status kód:", response.status_code)
    print("Odpověď:", response.text)

except Exception as e:
    print("[CHYBA]", str(e))
