# Mercado Livre Affiliate - Scraper Tool

## Quickstart

### Creating Affiliate URL:

```py
from mercado_livre_affiliate import MercadoLivreAffiliate
import json

def main():
    with open("www.mercadolivre.com.br.cookies.json", "r", encoding = "utf-8") as file:
        cookies = json.load(file)

    mercado_livre_affiliate = MercadoLivreAffiliate(
        cookies = cookies, # Mercado Livre site cookies
        origin_url = "https://www.mercadolivre.com.br/", # Mercado Livre root URL in your country
        webdriver_file_path = "path/to/webdriver.exe", # Path to browser webdriver
        headless = True # If the browser will appear
    )

    # Create an affiliate URL like: https://mercadolivre.com/sec/1QJMZsX
    affiliate_url = mercado_livre_affiliate.create_affiliate_url("https://produto.mercadolivre.com.br/MLB-2698490696-capinha-flashcase-aveludada-para-samsung-todos-os-modelos-_JM#reco_item_pos=1&reco_backend=univb-pdp-buybox&reco_backend_type=low_level&reco_client=pdp-v2p&reco_id=36bd3735-c484-4d17-b8f7-80a94da980f5&reco_backend_model=univb") 

    print(affiliate_url)

if __name__ == "__main__":
    main()
```