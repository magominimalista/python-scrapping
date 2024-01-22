from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from src.search_list import SearchLists
from src.to_json import ListToJson
import json

class JSONHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json; charset=utf-8")
        self.end_headers()

        # Analisa a URL da solicitação para extrair o termo de pesquisa após a barra
        url_parts = urlparse(self.path)
        path_components = url_parts.path.split('/')
        
        termo_pesquisa = "macbook"
        # Verifique se a URL tem um caminho após a barra e use-o como termo de pesquisa
        if len(path_components) > 1:
            termo_pesquisa = path_components[1]
            

        # Use a classe SearchLists para obter a lista de itens com base no termo de pesquisa
        item_search = SearchLists(termo_pesquisa)
        item_list = item_search.get_search_lists()

        # Use a classe ListToJson para converter a lista em JSON
        # Instancie a classe ListToJson com sua lista de dados
        json_converter = ListToJson(item_list)
        json_data = json_converter.to_json()

        # Converta o dicionário JSON em uma string JSON
        json_str = json.dumps(json_data, ensure_ascii=False)

        self.wfile.write(json_str.encode('utf-8'))

server = HTTPServer(("localhost", 7000), JSONHandler)
server.serve_forever()
