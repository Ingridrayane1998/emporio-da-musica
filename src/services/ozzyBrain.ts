import { ChatMessage, Product } from '../types';
import { PRODUCTS } from '../data/mockProducts';

/**
 * Intelligent knowledge engine for Ozzy, the musical assistant of Empório da Música.
 * Provides musical expertise, gear recommendations, product card attachments, and handoffs.
 */
export async function getOzzyResponse(userText: string): Promise<ChatMessage> {
  const query = userText.toLowerCase().trim();
  const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

  // 1. Check for guitar recommendations
  if (query.includes('guitarra') || query.includes('les paul') || query.includes('stratocaster') || query.includes('fender') || query.includes('gibson')) {
    if (query.includes('strat') || query.includes('fender') || query.includes('single coil')) {
      const strat = PRODUCTS.find(p => p.id === 'gtr-fender-strat-american') || PRODUCTS[0];
      return {
        id: `ozzy-${Date.now()}`,
        sender: 'ozzy',
        text: 'A Stratocaster de 1961 é pura mística! Ela tem aquele ataque vítreo inconfundível, captadores Pure Vintage \'61 com som cristalino e a dinâmica perfeita para Blues, Funk e Rock alternativo. Que tal dar uma conferida no timbre dela?',
        timestamp,
        productCard: strat,
        chips: [
          '🎸 Testar timbre de Strat',
          'Qual amplificador valvulado você indica?',
          'Quero ver a Les Paul também'
        ]
      };
    } else {
      const lesPaul = PRODUCTS.find(p => p.id === 'gtr-sunburst-59') || PRODUCTS[0];
      return {
        id: `ozzy-${Date.now()}`,
        sender: 'ozzy',
        text: 'Para timbres encorpados, peso harmônico e sustain lendário, nada supera a Gibson Les Paul Standard 50s Sunburst! Ela vem com tampo de Maple AA esculpido e os captadores Burstbucker que reproduzem fielmente os PAFs originais. Selecionei ela para você:',
        timestamp,
        productCard: lesPaul,
        chips: [
          '🎵 Ouvir o sustain e o drive',
          'Quais pedais usar com ela?',
          'Adicionar ao carrinho com -20%'
        ]
      };
    }
  }

  // 2. Check for acoustic instruments (violão, Martin, acústico)
  if (query.includes('violão') || query.includes('violao') || query.includes('acústico') || query.includes('acustico') || query.includes('martin')) {
    const martin = PRODUCTS.find(p => p.id === 'acoust-martin-d28') || PRODUCTS[1];
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'Se o assunto é violão de alto padrão com projeção inigualável, o **Martin D-28 Standard** é a lenda máxima! Construído com tampo em Sitka Spruce maciço e fundo em East Indian Rosewood, ele preenche qualquer sala com uma riqueza acústica que arrepia. Está pronto para tocar no nosso showroom!',
      timestamp,
      productCard: martin,
      chips: [
        '🎶 Tocar arpejo acústico',
        'Vocês entregam afinado e regulado?',
        'Ver opções de cordas recomendadas'
      ]
    };
  }

  // 3. Check for amplifiers (amplificador, valvulado, valvula, amp)
  if (query.includes('amplificador') || query.includes('valvula') || query.includes('valvulado') || query.includes('amp')) {
    const amp = PRODUCTS.find(p => p.id === 'amp-valve-deluxe') || PRODUCTS[2];
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'O calor de um amplificador 100% valvulado é indescritível! Nosso **Valve Harmonics Custom 22W** utiliza válvulas 6V6 no power amp e alto-falante Celestion Creamback de 12", garantindo desde um clean aveludado e perolado até aquela compressão natural clássica dos discos dos anos 70.',
      timestamp,
      productCard: amp,
      chips: [
        '🔥 Ouvir saturação valvulada',
        'Funciona bem com pedais de overdrive?',
        'Tem chave seletora para tocar em casa (7W)?'
      ]
    };
  }

  // 4. Check for pedals or overdrive
  if (query.includes('pedal') || query.includes('overdrive') || query.includes('screamer') || query.includes('efeito')) {
    const pedal = PRODUCTS.find(p => p.id === 'pedal-tube-screamer-ts808') || PRODUCTS[3];
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'O clássico dos clássicos! O **Ibanez TS808 Vintage Reissue** com o chip original JRC4558D dá aquele "boost" característico nos médios, cortando a mixagem de banda perfeitamente sem embolar os graves. É o companheiro ideal de qualquer valvulado!',
      timestamp,
      productCard: pedal,
      chips: [
        '⚡ Como montar minha pedaleira?',
        'Diferença entre TS9 e TS808',
        'Falar com especialista'
      ]
    };
  }

  // 5. Check for luthier / setup / regulagem
  if (query.includes('luthier') || query.includes('regulagem') || query.includes('conserto') || query.includes('trastes') || query.includes('blindagem')) {
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'Nossa oficina de luthieria é uma das mais respeitadas do país! Fazemos regulagem de oitavas, alinhamento micrométrico de trastes com Plek Machine, blindagem eletrostática em cobre para eliminar ruídos e trocas de captação.',
      timestamp,
      handoffCard: {
        specialistName: 'Mestre Gilberto Silva (Luthier Chefe)',
        specialistRole: 'Luthieria Artesanal & Calibração Custom Shop',
        reason: 'Agendamento de Regulagem & Inspeção Gratuita',
        whatsappNumber: '5511999887766'
      },
      chips: [
        '🔧 Ver tabela de serviços e preços',
        'Quanto tempo demora a regulagem?',
        'Meu instrumento faz ruído de aterramento'
      ]
    };
  }

  // 6. Check for discount / promo / ofertas
  if (query.includes('desconto') || query.includes('promo') || query.includes('oferta') || query.includes('cupom') || query.includes('20%')) {
    const discounted = PRODUCTS[0];
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'Temos uma condição exclusiva hoje no Empório da Música! 🏷️ Todos os instrumentos selecionados da linha Custom Shop estão com **até 20% de desconto** à vista ou em até **12x sem juros**. Além disso, use o cupom secreto **OZZY10** para mais 10% OFF no seu primeiro pedido!',
      timestamp,
      productCard: discounted,
      chips: [
        'Aplicar cupom OZZY10 no carrinho',
        'Ver todas as guitarras em oferta',
        'Calcular frete para meu CEP'
      ]
    };
  }

  // 7. Check for human handoff
  if (query.includes('humano') || query.includes('atendente') || query.includes('whatsapp') || query.includes('contato') || query.includes('falar')) {
    return {
      id: `ozzy-${Date.now()}`,
      sender: 'ozzy',
      text: 'Com certeza! Vou conectar você diretamente com um dos nossos consultores músicos do balcão para tirar dúvidas pontuais ou fechar negociação especial.',
      timestamp,
      handoffCard: {
        specialistName: 'Rodrigo Medeiros',
        specialistRole: 'Consultor Sênior de Cordas & Amplificação',
        reason: 'Atendimento Personalizado & Teste Presencial em Cabine',
        whatsappNumber: '5511988881234'
      },
      chips: [
        'Chamar no WhatsApp agora',
        'Voltar ao catálogo de instrumentos'
      ]
    };
  }

  // Default helpful response
  const randomProd: Product = PRODUCTS[Math.floor(Math.random() * PRODUCTS.length)];
  return {
    id: `ozzy-${Date.now()}`,
    sender: 'ozzy',
    text: `Entendido perfeitamente! Como consultor musical do Empório, eu posso te ajudar a encontrar o instrumento ideal para o seu estilo sonoro, comparar especificações de madeiras e captadores, ou agendar uma revisão na nossa luthieria. Veja este destaque que separei para você:`,
    timestamp,
    productCard: randomProd,
    chips: [
      '🎸 Qual a melhor guitarra para iniciante?',
      '🔊 O que é impedância de caixas e amps?',
      '🎛️ Ir para o Laboratório de Timbres'
    ]
  };
}
