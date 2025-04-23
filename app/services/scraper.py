from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from app.exceptions import ScrapingError
import time
import random

# Configurações dos sites (agora mais organizada)
CONFIG = {
    'amazon': {
        'url': 'https://www.amazon.com.br/s?k={query}',
        'container': 'div[data-component-type="s-search-result"]',
        'name': 'h2 span',  # Seletor simplificado
        'price': 'span.a-price span',
        'link': 'h2 a'
    },
    'magazineluiza': {
        'url': 'https://www.magazineluiza.com.br/busca/{query}/',
        'container': 'li[data-testid="product-list-item"]',
        'name': 'h2[data-testid="product-title"]',
        'price': 'p[data-testid="price-value"]',
        'link': 'a[href*="/produto/"]'
    }
}

def get_driver():
    """Configura e retorna o driver do Firefox pronto para uso"""
    options = Options()
    
    # Configurações anti-bloqueio
    options.headless = False  # Mude para False durante os testes
    options.set_preference("dom.webdriver.enabled", False)
    options.set_preference("useAutomationExtension", False)
    options.set_preference("dom.webnotifications.enabled", False)
    options.set_preference("dom.push.enabled", False)
    
    # Rotação de User-Agents
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ]
    options.set_preference("general.useragent.override", random.choice(user_agents))
    
    # Configuração do serviço
    service = Service(GeckoDriverManager().install())
    
    driver = webdriver.Firefox(service=service, options=options)
    
    # Script para ocultar WebDriver
    driver.execute_script(
        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    )
    
    return driver

def get_available_sites():
    """Retorna a lista de sites configurados"""
    return list(CONFIG.keys())

def scrape_product(site, query):
    """Função principal de scraping com tratamento robusto de erros"""
    if site not in CONFIG:
        raise ScrapingError(f"Site {site} não está configurado")
    
    driver = get_driver()
    try:
        config = CONFIG[site]
        url = config['url'].format(query=query.replace(' ', '+'))
        driver.get(url)
        
        # Debug: salva screenshot
        driver.save_screenshot(f'debug_{site}.png')
        
        # Espera inteligente
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config['container'])))
        
        # Rolagem progressiva
        for _ in range(2):
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(random.uniform(0.5, 1.5))
        
        # Extração dos produtos
        produtos = []
        items = driver.find_elements(By.CSS_SELECTOR, config['container'])[:5]
        
        for item in items:
            try:
                produtos.append({
                    'nome': item.find_element(By.CSS_SELECTOR, config['name']).text,
                    'preco': item.find_element(By.CSS_SELECTOR, config['price']).text,
                    'link': item.find_element(By.CSS_SELECTOR, config['link']).get_attribute('href'),
                    'site': site
                })
            except Exception as e:
                print(f"Erro ao processar item: {str(e)}")  # Log de erro
                continue
        
        if not produtos:
            raise ScrapingError("Nenhum produto encontrado (pode ter sido bloqueado)")
            
        return produtos
        
    except Exception as e:
        raise ScrapingError(f"Falha técnica ao acessar {site}: {str(e)}")
    finally:
        driver.quit()