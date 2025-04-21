import requests

url = "https://kaitotrader-email.onrender.com/send-email"
payload = {
    "to": "jan.jordan@email.cz",
    "subject": "Testovací e-mail",
    "text": "Toto je test od Kaitotradera – pokud čteš, funguje to!"
}

response = requests.post(url, json=payload)
print("Status:", response.status_code)
print("Odpověď:", response.text)
