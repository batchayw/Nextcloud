import requests

URL = "https://nextcloud.example.com"

try:
    response = requests.get(URL)
    if response.status_code == 200:
        print("✅ Nextcloud est en ligne !")
    else:
        print(f"⚠️ Erreur {response.status_code} lors de l'accès à Nextcloud")
except Exception as e:
    print(f"❌ Impossible d'accéder à Nextcloud : {e}")
