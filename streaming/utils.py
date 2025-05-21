import requests

def request_airdrop(user_pubkey: str, amount: int):
    url = "http://localhost:3000/airdrop"
    payload = {
        "user": user_pubkey,
        "amount": amount
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при запросе airdrop: {e}")
        return None
