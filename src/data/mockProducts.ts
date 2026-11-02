import { Product, ChatMessage } from '../types';

export const OZZY_AVATAR = '/src/assets/images/ozzy_mascot_avatar_1793632768308.jpg';
export const STORE_HERO = '/src/assets/images/emporio_store_hero_1793632769824.jpg';
export const GUITAR_SUNBURST = '/src/assets/images/electric_guitar_sunburst_1793632768094.jpg';
export const ACOUSTIC_GUITAR = '/src/assets/images/acoustic_guitar_wood_1793632769160.jpg';
export const TUBE_AMP = '/src/assets/images/tube_amp_vintage_1793632770085.jpg';

export const PRODUCTS: Product[] = [
  {
    id: 'gtr-sunburst-59',
    name: 'Gibson Les Paul Standard 50s Sunburst',
    brand: 'Gibson USA',
    category: 'guitars',
    price: 18990,
    originalPrice: 23740,
    discountPercent: 20,
    image: GUITAR_SUNBURST,
    rating: 4.9,
    reviewsCount: 48,
    tags: ['Valvulados', 'Burstbucker', 'Tampo Flamed Maple'],
    specs: {
      'Corpo': 'Mogno Maciço com tampo em Maple AA',
      'Braço': 'Vintage 50s Rounded',
      'Captadores': 'Burstbucker 1 (braço) & Burstbucker 2 (ponte)',
      'Escala': 'Rosewood 22 trastes Medium Jumbo',
      'Ponte': 'ABR-1 Tune-O-Matic em alumínio'
    },
    audioToneType: 'rock',
    description: 'O ícone supremo do classic rock e blues com sustain infinito, captadores Burstbucker Alnico II e tampo flame maple fascinante.',
    inStock: true,
    isOzzyPick: true
  },
  {
    id: 'acoust-martin-d28',
    name: 'Martin D-28 Standard Handcrafted Dreadnought',
    brand: 'Martin Guitar',
    category: 'acoustics',
    price: 24500,
    originalPrice: 28900,
    discountPercent: 15,
    image: ACOUSTIC_GUITAR,
    rating: 5.0,
    reviewsCount: 32,
    tags: ['Sitka Spruce', 'East Indian Rosewood', 'Acústico Puro'],
    specs: {
      'Tampo': 'Sitka Spruce Sólido com acabamento Gloss',
      'Fundo e Laterais': 'East Indian Rosewood Maciço',
      'Braço': 'Hardwood Selecionado com Perfil Oval Modificado',
      'Escala': 'Ébano Africano legítimo',
      'Cavalete': 'Ébano com rastilho em osso compensado'
    },
    audioToneType: 'acoustic',
    description: 'O padrão dourado pelo qual todos os violões de aço são julgados. Graves profundos e riqueza harmônica celestial.',
    inStock: true,
    isOzzyPick: true
  },
  {
    id: 'amp-valve-deluxe',
    name: 'Valve Harmonics Custom Boutique 22W Combo',
    brand: 'Valve Harmonics',
    category: 'amps',
    price: 9800,
    originalPrice: 12250,
    discountPercent: 20,
    image: TUBE_AMP,
    rating: 4.9,
    reviewsCount: 27,
    tags: ['100% Valvulado', '6V6 Power Tubes', 'Spring Reverb'],
    specs: {
      'Potência': '22W Classe AB valvulado (com seletor 7W)',
      'Válvulas': '2x 6V6, 1x 12AT7, 3x 12AX7, 1x 5AR4',
      'Alto-falante': '12" Celestion Creamback Heritage',
      'Canais': 'Vintage Clean & Harmonically Rich Drive',
      'Reverb': 'Tanque de molas Accutronics genuíno'
    },
    audioToneType: 'blues',
    description: 'Amplificador valvulado boutique com aquecimento harmônico vintage, dinâmica tátil impressionante e o autêntico "sag" dos anos 60.',
    inStock: true,
    isOzzyPick: true
  },
  {
    id: 'pedal-tube-screamer-ts808',
    name: 'Ibanez TS808 Vintage Tube Screamer Reissue',
    brand: 'Ibanez Japan',
    category: 'pedals',
    price: 1580,
    originalPrice: 1860,
    discountPercent: 15,
    image: GUITAR_SUNBURST,
    rating: 4.8,
    reviewsCount: 114,
    tags: ['JRC4558D', 'Overdrive Lendário', 'True Bypass'],
    specs: {
      'Circuito': 'Chip operacional JRC4558D clássico',
      'Controles': 'Overdrive, Tone, Level',
      'Chaveamento': 'Bypass silencioso de alta impedância',
      'Alimentação': '9V DC (bateria ou fonte)'
    },
    audioToneType: 'blues',
    description: 'O pedal de overdrive mais influente da história da guitarra. Empurre qualquer amplificador valvulado com o icônico empurrão de médios.',
    inStock: true
  },
  {
    id: 'gtr-fender-strat-american',
    name: 'Fender American Vintage II 1961 Stratocaster',
    brand: 'Fender Musical Instruments',
    category: 'guitars',
    price: 16490,
    originalPrice: 19400,
    discountPercent: 15,
    image: GUITAR_SUNBURST,
    rating: 4.9,
    reviewsCount: 56,
    tags: ['Pure Vintage 61', 'Raio 7.25', 'Alder Body'],
    specs: {
      'Corpo': 'Alder Premium com acabamento em Nitrocelulose',
      'Braço': 'Maple perfil 1961 "C"',
      'Captadores': 'Trio Pure Vintage \'61 Single-Coil Strat',
      'Escala': 'Slab Rosewood 21 trastes vintage tall',
      'Ponte': 'Tremolo sincronizado Pure Vintage'
    },
    audioToneType: 'sparkle',
    description: 'O verdadeiro estalo e ressonância de sino (bell-like chime) dos anos 60. Sensação de instrumento vintage de colecionador.',
    inStock: true
  },
  {
    id: 'audio-shure-sm7b',
    name: 'Shure SM7B Vocal Dynamic Studio Microphone',
    brand: 'Shure',
    category: 'studio',
    price: 3690,
    originalPrice: 4100,
    discountPercent: 10,
    image: TUBE_AMP,
    rating: 5.0,
    reviewsCount: 89,
    tags: ['Padrão da Indústria', 'Gravação Vocal', 'Rejeição de Ruído'],
    specs: {
      'Tipo': 'Dinâmico cardióide de bobina móvel',
      'Resposta de Freqüência': '50Hz a 20kHz plana e ampla',
      'Blindagem': 'Eletromagnética avançada contra interferência',
      'Conector': 'XLR balanceado padrão de estúdio'
    },
    audioToneType: 'jazz',
    description: 'O microfone lendário utilizado por lendas da música e nos melhores estúdios ao redor do globo. Calor vocal aveludado.',
    inStock: true
  }
];

export const INITIAL_CHAT_MESSAGES: ChatMessage[] = [
  {
    id: 'msg-1',
    sender: 'ozzy',
    text: 'Olá! Eu sou o Ozzy, seu consultor musical e especialista de timbres do Empório da Música! 🦊🎸 Como posso afinar sua busca hoje? Procura uma guitarra clássica, um amplificador valvulado de boutique ou quer montar a sua cadeia de pedais perfeita?',
    timestamp: '10:30',
    chips: [
      '🎸 Recomende uma guitarra até R$ 20.000',
      '🔥 O que são os amplificadores valvulados?',
      '⚡ Timbre de Blues e Classic Rock',
      '🔧 Agendar serviço na Luthieria',
      '🏷️ Ver ofertas com 20% OFF'
    ]
  },
  {
    id: 'msg-2',
    sender: 'user',
    text: 'Estou procurando uma Les Paul com som vintage e corpo em mogno legítimo. O que você tem disponível?',
    timestamp: '10:31'
  },
  {
    id: 'msg-3',
    sender: 'ozzy',
    text: 'Excelente escolha! Para quem busca aquele som encorpado dos deuses do rock dos anos 50 e 60, acabamos de receber na boutique a extraordinária **Gibson Les Paul Standard 50s Sunburst**! O sustain dela no braço de mogno maciço com os captadores Burstbucker Alnico II é pura poesia sonora. Dá uma olhada no acabamento e aproveite que está com -20%!',
    timestamp: '10:31',
    productCard: PRODUCTS[0],
    chips: [
      'Ouvir amostra de timbre 🎵',
      'Qual amplificador combina com ela?',
      'Falar com especialista humano no WhatsApp'
    ]
  }
];
