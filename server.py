#!/usr/bin/env python3
"""
Empório da Música & Ozzy - Python Chat Backend
Zero-dependency HTTP API powered by standard library Python 3.10
Handles Ozzy's musical dialogue, gear recommendations, audio samples, and luthier handoffs.
"""

import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
from datetime import datetime

PORT = 5001

# Boutique instrument catalog
PRODUCTS = [
    {
        "id": "gtr-sunburst-59",
        "name": "Gibson Les Paul Standard 50s Sunburst",
        "brand": "Gibson USA",
        "category": "guitars",
        "price": 18990,
        "originalPrice": 23740,
        "discountPercent": 20,
        "image": "/src/assets/images/electric_guitar_sunburst_1793632768094.jpg",
        "rating": 4.9,
        "reviewsCount": 48,
        "audioToneType": "rock",
        "description": "O ícone supremo do classic rock e blues com sustain infinito, captadores Burstbucker Alnico II e tampo flame maple fascinante.",
        "specs": {
            "Corpo": "Mogno maciço com tampo em Maple AA",
            "Braço": "Vintage 50s Rounded",
            "Captadores": "Burstbucker 1 (braço) & Burstbucker 2 (ponte)",
            "Escala": "Rosewood 22 trastes Medium Jumbo"
        }
    },
    {
        "id": "acoust-martin-d28",
        "name": "Martin D-28 Standard Handcrafted Dreadnought",
        "brand": "Martin Guitar",
        "category": "acoustics",
        "price": 24500,
        "originalPrice": 28900,
        "discountPercent": 15,
        "image": "/src/assets/images/acoustic_guitar_wood_1793632769160.jpg",
        "rating": 5.0,
        "reviewsCount": 32,
        "audioToneType": "acoustic",
        "description": "O padrão de referência acústico supremo. Graves ressonantes, projeção profunda e riqueza harmônica celestial.",
        "specs": {
            "Tampo": "Sitka Spruce Sólido",
            "Fundo e Laterais": "East Indian Rosewood Maciço",
            "Escala": "Ébano Africano legítimo"
        }
    },
    {
        "id": "amp-valve-deluxe",
        "name": "Valve Harmonics Custom Boutique 22W Combo",
        "brand": "Valve Harmonics",
        "category": "amps",
        "price": 9800,
        "originalPrice": 12250,
        "discountPercent": 20,
        "image": "/src/assets/images/tube_amp_vintage_1793632770085.jpg",
        "rating": 4.9,
        "reviewsCount": 27,
        "audioToneType": "blues",
        "description": "Amplificador valvulado boutique com aquecimento harmônico vintage, dinâmica tátil impressionante e o autêntico som valvulado.",
        "specs": {
            "Potência": "22W Classe AB (chave seletora 7W)",
            "Válvulas": "2x 6V6, 1x 12AT7, 3x 12AX7",
            "Alto-falante": '12" Celestion Creamback Heritage',
            "Reverb": "Tanque de molas genuíno Accutronics"
        }
    }
]

def process_ozzy_chat(user_message: str):
    """
    Core Python intelligence for Ozzy
    """
    text = (user_message or "").strip().lower()
    time_now = datetime.now().strftime("%H:%M")
    
    # 1. Guitarras / Les Paul / Strato / Cordas
    if any(k in text for k in ["guitarra", "les paul", "strat", "fender", "gibson", "corda"]):
        prod = PRODUCTS[0]
        return {
            "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
            "sender": "ozzy",
            "text": "Fala, músico! A **Gibson Les Paul Standard 50s Sunburst** é pura lenda. O sustain no corpo de mogno com tampo de maple e os captadores Burstbucker entregam aquele som gordo e aveludado dos anos 50. Dá uma olhada nela aqui:",
            "timestamp": time_now,
            "productCard": prod,
            "chips": [
                "🎵 Ouvir amostra de timbre",
                "Qual amplificador valvulado você indica?",
                "Adicionar ao carrinho com -20%"
            ]
        }

    # 2. Violão / Acústico / Martin
    if any(k in text for k in ["violao", "violão", "acustico", "acústico", "martin"]):
        prod = PRODUCTS[1]
        return {
            "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
            "sender": "ozzy",
            "text": "Para quem busca som acústico de alta classe, o **Martin D-28 Standard** é insuperável! O tampo em Sitka Spruce maciço com fundo em Rosewood projeta uma ressonância cristalina e encorpada. O instrumento vem 100% regulado pela nossa luthieria.",
            "timestamp": time_now,
            "productCard": prod,
            "chips": [
                "🎶 Ouvir arpejo acústico",
                "Quais cordas combinam com ele?",
                "Falar com especialista no WhatsApp"
            ]
        }

    # 3. Amplificador valvulado / válvulas
    if any(k in text for k in ["amplificador", "valvula", "valvulado", "amp", "caixa"]):
        prod = PRODUCTS[2]
        return {
            "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
            "sender": "ozzy",
            "text": "Nada substitui a compressão e a saturação harmônica de um valvulado de verdade! O **Valve Harmonics Custom 22W** tem válvulas 6V6 e falante Celestion Creamback de 12\". É o par perfeito para guitarras com humbucker ou single coil.",
            "timestamp": time_now,
            "productCard": prod,
            "chips": [
                "🔥 Ouvir saturação valvulada",
                "Tem chave atenuadora de potência?",
                "Ver opções de frete"
            ]
        }

    # 4. Luthieria / Regulagem / Ruído / Trastes
    if any(k in text for k in ["luthier", "regulagem", "traste", "ruido", "ruído", "blindagem", "conserto", "afinar"]):
        return {
            "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
            "sender": "ozzy",
            "text": "Nossa bancada de Luthieria artesanal faz regulagem completa de ação de cordas, calibração de tensor, oitavas e blindagem eletrostática para eliminar ruídos de aterramento. Já conectei nossa equipe técnica para você:",
            "timestamp": time_now,
            "handoffCard": {
                "specialistName": "Mestre Gilberto (Luthier Chefe)",
                "specialistRole": "Luthieria Artesanal & Calibração Custom",
                "reason": "Agendamento de Regulagem & Inspeção Gratuita",
                "whatsappNumber": "5511999887766"
            },
            "chips": [
                "🔧 Ver tabela de serviços",
                "Quanto tempo demora?",
                "Voltar aos instrumentos"
            ]
        }

    # 5. Promoções / Ofertas / Desconto / Preço
    if any(k in text for k in ["desconto", "promo", "promoção", "oferta", "cupom", "preco", "preço"]):
        return {
            "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
            "sender": "ozzy",
            "text": "Hoje é dia de som novo! 🏷️ Todos os itens marcados na boutique estão com **até 20% OFF** à vista ou parcelamento em até **12x sem juros**. Além disso, use o cupom secreto **OZZY10** para ganhar mais 10% de desconto adicional!",
            "timestamp": time_now,
            "productCard": PRODUCTS[0],
            "chips": [
                "Aplicar cupom OZZY10",
                "Ver mais guitarras em promoção",
                "Calcular frete expresso"
            ]
        }

    # 6. Default conversational response
    return {
        "id": f"ozzy-{int(datetime.now().timestamp()*1000)}",
        "sender": "ozzy",
        "text": f"Opa! Como consultor sonoro do Empório da Música, posso te recomendar o melhor instrumento para seu estilo (Rock, Blues, MPB, Jazz ou Metal), explicar diferenças de madeiras e captadores, ou agendar uma revisão na nossa luthieria. O que você gostaria de explorar hoje?",
        "timestamp": time_now,
        "chips": [
            "🎸 Recomende uma guitarra clássica",
            "🔥 Como funciona um amplificador valvulado?",
            "🔧 Agendar luthieria para meu instrumento",
            "🏷️ Ofertas e descontos especiais"
        ]
    }


class SimpleAPIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        if self.path == '/api/health':
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "ok", "backend": "Python 3.10", "service": "Ozzy Musical Chat"}).encode('utf-8'))
        elif self.path == '/api/products':
            self._set_headers(200)
            self.wfile.write(json.dumps(PRODUCTS).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))

    def do_POST(self):
        if self.path == '/api/chat':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            try:
                data = json.loads(body)
                user_msg = data.get('message', '')
                reply = process_ozzy_chat(user_msg)
                self._set_headers(200)
                self.wfile.write(json.dumps(reply).encode('utf-8'))
            except Exception as e:
                self._set_headers(400)
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": "Not found"}).encode('utf-8'))

def run_server():
    server_address = ('127.0.0.1', PORT)
    httpd = HTTPServer(server_address, SimpleAPIHandler)
    print(f"🐍 Python Backend running on http://127.0.0.1:{PORT}", flush=True)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()
