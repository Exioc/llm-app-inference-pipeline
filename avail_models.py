import requests
from src.config.config import OLLAMA_BASE_URL, OLLAMA_API_KEY

def main():
    url = f"{OLLAMA_BASE_URL}/api/tags"

    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        models = data.get("models", [])

        if not models:
            print("Keine Modelle gefunden.")
            return

        print(f"{len(models)} Modelle gefunden:\n")

        for m in models:
            name = m.get("name", "unknown")
            family = m.get("details", {}).get("family", "unknown")
            params = m.get("details", {}).get("parameter_size", "unknown")
            size_gb = m.get("size", 0) / 1e9

            print(f"- {name} | {family} | {params} | {size_gb:.1f} GB")

    except requests.exceptions.Timeout:
        print("Request hat zu lange gedauert (Timeout).")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Fehler: {e} | Response: {response.text}")

    except requests.exceptions.RequestException as e:
        print(f"Netzwerkfehler: {e}")

    except ValueError:
        print("Antwort konnte nicht als JSON gelesen werden.")

if __name__ == "__main__":    
    main()