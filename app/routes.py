from flask import render_template, request, flash
from app import app
from app.services.scraper import scrape_product, get_available_sites
from app.exceptions import ScrapingError
import os 


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'produtos': [],
        'sites': get_available_sites(),
        'search_performed': False
    }
    print(f"Caminho dos templates: {app.template_folder}")
    print(f"Arquivos disponíveis: {os.listdir(app.template_folder)}")


    if request.method == 'POST':
        try:
            site = request.form.get('site')
            query = request.form.get('busca', '').strip()
            
            if not query:
                flash('Por favor, digite um termo para buscar', 'error')
            else:
                context['produtos'] = scrape_product(site, query)
                context['search_performed'] = True
                
        except ScrapingError as e:
            flash(f'Erro na busca: {str(e)}', 'error')
        except Exception as e:
            app.logger.error(f'Erro inesperado: {str(e)}')
            flash('Ocorreu um erro interno durante a busca', 'error')

    return render_template('index.html', **context)

print(app.url_map)  # Mostrará todas as rotas registradas


# @app.route('/teste')
# def teste():
#     return "TESTE OK - Rota funcionando"