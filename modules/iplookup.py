import requests

def get_ip_info(target="8.8.8.8"):
    try:
        response = requests.get(f"http://ip-api.com/json/{target}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "query": data.get("query"),
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "status": "Sucesso"
            }
    except Exception as e:
        return {"error": str(e), "status": "Falha"}
    return {"status": "Indisponível"}

if __name__ == "__main__":
    print(get_ip_info())
