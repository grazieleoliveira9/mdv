from flask import render_template, request
from app import app
from app.services.scraper import scrape, CONFIG

@app.route('/', methods=['GET', 'POST'])
def index():
    produtos = []
    if request.method == 'POST':
        site = request.form['site']
        query = request.form['busca']
        produtos = scrape(site, query)
    
    return render_template('index.html', 
                         produtos=produtos,
                         sites=list(CONFIG.keys()))