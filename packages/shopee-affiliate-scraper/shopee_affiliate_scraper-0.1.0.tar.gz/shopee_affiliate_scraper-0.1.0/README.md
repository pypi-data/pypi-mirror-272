# Shopee Affiliate - Scraper Tool

## Quickstart

### Creating Affiliate URL:

```py
from shopee_affiliate import ShopeeAffiliate
import json

def get_shopee_cookies() -> list[dict]:
    with open("shopee.com.br.cookies.json", "r") as file:
        cookies = json.load(file)
        return cookies

def main() -> None:
    cookies = get_shopee_cookies()

    shopee_affiliate = ShopeeAffiliate(
        cookies = cookies,
        headless = False
    )

    affiliate_urls = shopee_affiliate.create_affiliate_urls([
        "https://shopee.com.br/Anel-A%C3%A7o-Inoxidavel-Titanium-Ultra-Resistente-Elegante-Moderno-Tit%C3%A2nio-i.216863756.19571410921?sp_atk=32011a47-12e1-4519-930f-e1babe0029d4&xptdk=32011a47-12e1-4519-930f-e1babe0029d4",
        "https://shopee.com.br/8MM-De-Largura-Novo-Anel-De-A%C3%A7o-Tit%C3%A2nio-Colorido-Para-Homens-Acess%C3%B3rios-De-J%C3%B3ias-Inoxid%C3%A1vel-Fashionable-i.1006215031.20986808207?sp_atk=94900ec4-a80b-4dc4-9780-cb7ac0edef9f&xptdk=94900ec4-a80b-4dc4-9780-cb7ac0edef9f",
        "https://shopee.com.br/Anel-Masculino-A%C3%A7o-Negro-Preto-Inoxid%C3%A1vel-Motoqueiro-Moderno-i.331420767.21899047159?sp_atk=f6efd325-ccc4-42e3-a590-14d425ebb09a&xptdk=f6efd325-ccc4-42e3-a590-14d425ebb09a",
        "https://shopee.com.br/8MM-Moda-Homem-E-Mulher-Simples-Anel-Duplo-Biselado-Polido-Azul-Ouro-Tit%C3%A2nio-De-A%C3%A7o-i.397469095.22226995990?sp_atk=57420437-3fa9-4c98-af02-aafb2556e7f5&xptdk=57420437-3fa9-4c98-af02-aafb2556e7f5",
        "https://shopee.com.br/An%C3%A9is-De-A%C3%A7o-Tit%C3%A2nio-Para-Mulheres-E-Homens-i.1006215031.23387604145?sp_atk=6929b0ff-53ee-4099-a3a6-891c948817cf&xptdk=6929b0ff-53ee-4099-a3a6-891c948817cf"
    ])

    print(affiliate_urls)

if __name__ == "__main__":
    main()
```