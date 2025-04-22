from flask import render_template, request
from app import app
import requests
from bs4 import BeautifulSoup
import re

def scrape_mercadolivre(busca):
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        url = f"https://lista.mercadolivre.com.br/{busca.replace(' ', '-')}"
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        produtos = []
        for item in soup.find_all('div', class_=re.compile('ui-search-result__wrapper'))[:5]:
            try:
                nome = item.find('h2', class_=re.compile('ui-search-item__title')).text.strip()
                preco = item.find('span', class_=re.compile('price-tag-fraction')).text.strip()
                link = item.find('a')['href']
                produtos.append({'nome': nome, 'preco': preco, 'link': link})
            except:
                continue
        return produtos
    except:
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    produtos = []
    if request.method == 'POST':
        produtos = scrape_mercadolivre(request.form['busca'])
    return render_template('index.html', produtos=produtos)