import requests
from bs4 import BeautifulSoup
import re
import math

class SearchLists:
    def __init__(self, tag):
        self.tag = tag
        self.data = []

    def get_search_lists(self):
        

        url = f'https://www.buscape.com.br/search?q={self.tag}&hitsPerPage=48&page=1'
        response = requests.get(url)
        html = BeautifulSoup(response.text, 'html.parser')
        total_pages = html.select_one('div.SearchFilters_HitsCount__tyHIc')
        total_pages_number = re.sub(r'[^0-9]', '', total_pages.text)
        total_itens = int(total_pages_number)

        if total_itens > 300:
            total_itens = 300

        num_pages = total_itens / 48
        num_pages_total = math.ceil(num_pages)

        for page in range(1, num_pages_total + 1):

            url = f'https://www.buscape.com.br/search?q={self.tag}&hitsPerPage=48&page={page}'  # Correção aqui
            response = requests.get(url)
            html = BeautifulSoup(response.text, 'html.parser')

            for objet in html.select('#__next > div > div.Hits_Wrapper__GHrC6 > div'):
                link = objet.select_one('a')
                title = objet.select_one('h2.Text_Text__h_AF6')
                image = objet.select_one('img')
                price = objet.select_one('p.Text_Text__h_AF6.Text_MobileHeadingS__Zxam2')
                cond = objet.select_one('p:nth-of-type(2).Text_Text__h_AF6')
                comment = objet.select_one('h3.Text_Text__h_AF6')

                if title and image:
                    newtitle = title.get_text(strip=True)
                    image_src = image['src']
                    price_text = price.get_text(strip=True) if price else "Preço não encontrado"
                    cond_text = cond.get_text(strip=True) if cond else "Condição não encontrada"
                    comment_text = comment.get_text(strip=True) if comment else "Comentário não encontrado"
                    link_href = link['href']

                    if "sem juros" in cond_text:
                        cond_text = cond_text.replace("sem juros", "")
                        cond_text = cond_text + " sem juros"

                    if "com juros" in cond_text:
                        cond_text = cond_text.replace("com juros", "")
                        cond_text = cond_text + " com juros"
                    
                    item = {
                        'Pagina': page,
                        'Título': newtitle,
                        'Imagem': image_src,
                        'Preço': price_text,
                        'Condição': cond_text,
                        'Comentário': comment_text,
                        'Link': 'https://www.buscape.com.br'+link_href
                    }
                    self.data.append(item)

        return self.data