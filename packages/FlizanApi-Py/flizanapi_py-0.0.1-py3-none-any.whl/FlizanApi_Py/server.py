import requests

def get_server(api_key, server_ip, server_port, game):
    url = "https://api.flizan.ru/api/getstatusserver/"
    params = {
        'server_ip': server_ip,
        'server_port': server_port,
        'game': game,
        'api_key': api_key
    }
    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == "success":
            print(data)
        elif data['status'] == "error":
            print(data['message'])
        else:
            print("Неизвестная ошибка!")
    else:
        print({'error': f"Ошибка: {response.status_code}"})
