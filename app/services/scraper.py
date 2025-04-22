from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import time
import random

CONFIG = {
    'amazon': {
        'url': 'https://www.amazon.com.br/s?k={query}',
        'selectors': {
            'container': 'div.s-result-item',
            'name': 'h2.a-size-mini',
            'price': 'span.a-price-whole',
            'link': 'a.a-link-normal'
        }
    },
    'magazineluiza': {
        'url': 'https://www.magazineluiza.com.br/busca/{query}/',
        'selectors': {
            'container': 'li[data-testid="product-item"]',
            'name': 'h2[data-testid="product-title"]',
            'price': 'p[data-testid="price-value"]',
            'link': 'a[data-testid="product-card-container"]'
        }
    }
}

def get_driver():
    options = Options()
    options.headless = True  # Modo sem interface gráfica
    
    # Instala automaticamente o geckodriver
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver
def scrape(site, query):
    driver = get_driver()
    try:
        config = CONFIG[site]
        url = config['url'].format(query=query.replace(' ', '+'))
        driver.get(url)
        
        # Espera inteligente com timeout explícito
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, config['selectors']['container'])))
        
        # Rolagem progressiva
        for _ in range(3):
            driver.execute_script("window.scrollBy(0, 500)")
            time.sleep(random.uniform(0.5, 1.5))
            
        # Debug: captura print da tela
        driver.save_screenshot('debug_screenshot.png')
        print("Debug: Screenshot salvo")
        
        products = []
        items = driver.find_elements(By.CSS_SELECTOR, config['selectors']['container'])[:5]
        
        if not items:
            print("AVISO: Nenhum item encontrado com o seletor:", config['selectors']['container'])
        
        for item in items:
            try:
                products.append({
                    'nome': WebDriverWait(item, 5).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, config['selectors']['name']))).text,
                    'preco': WebDriverWait(item, 5).until(
                        EC.visibility_of_element_located(
                            (By.CSS_SELECTOR, config['selectors']['price']))).text,
                    'link': item.find_element(
                        By.CSS_SELECTOR, config['selectors']['link']).get_attribute('href'),
                    'site': site
                })
            except Exception as e:
                print(f"Erro ao extrair item: {str(e)}")
                continue
                
        return products
        
    except Exception as e:
        print(f"ERRO NO SCRAPING: {str(e)}")
        return []
    finally:
        driver.quit()