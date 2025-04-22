import requests

def search_products(api_key, query):
    url = "https://api.mercadolibre.com/sites/MLB/search"
    params = {
        'q': query,
        'limit': 5,
        'access_token': api_key
    }
    response = requests.get(url, params=params)
    results = []
    
    if response.status_code == 200:
        for item in response.json()['results'][:5]:
            results.append({
                'nome': item['title'],
                'preco': f"R$ {item['price']}",
                'link': item['permalink'],
                'site': 'Mercado Livre (API)'
            })
    
    return results