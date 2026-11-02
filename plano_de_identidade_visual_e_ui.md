# Plano de Identidade Visual e UI — Empório da Música + Ozzy (Google Stitch)

> **Escopo:** não é o site completo da loja. São apenas os elementos visuais que compõem o produto: **interface do chat**, **logo**, **avatar do Ozzy** e componentes de apoio.  
> **Uso:** anexe este documento no Stitch e use os prompts da seção 7, tela por tela, na ordem indicada.

---

## 1. Contexto

- **Marca:** Empório da Música — loja para amantes de música (instrumentos acústicos, elétricos, acessórios, áudio).
- **Produto:** janela de chat de atendimento com o assistente **Ozzy**.
- **Público:** músicos, hobbistas, colecionadores e fãs de música, de iniciantes a profissionais.
- **Sensação desejada:** acolhedora, moderna, com personalidade musical. Como entrar em uma loja de instrumentos charmosa, com atendimento simpático.
- **Palavras-chave:** vibrante, aconchegante, moderno, analógico-meets-digital, "acústico + elétrico vibrante".

---

## 2. Identidade da marca

### Conceito do logo
Combinar **símbolo musical + calor de loja tradicional ("empório")**. Ideias (escolher uma):
1. **Palheta + emporium:** uma palheta de violão/guitarra cujo centro forma a letra **E**, com um pequeno toldo/fita de loja no topo.
2. **Violão/clave + onda sonora:** silhueta minimalista de clave de sol cujo traço vira uma onda sonora.
3. **Monograma "EM":** letras entrelaçadas com uma nota musical como ponto.

**Entregas do logo:**
- Versão horizontal (símbolo + nome "Empório da Música")
- Versão só símbolo (favicon/ícone do chat)
- Versão sobre fundo escuro e sobre fundo claro
- Formato vetorial/PNG com fundo transparente

### Paleta de cores (tokens)
Tema principal **escuro** (clima de palco/estúdio) com tema claro opcional.

| Token | Hex | Uso |
|---|---|---|
| `--bg` | `#0F0B1A` | Fundo principal (roxo quase preto) |
| `--surface` | `#1A1330` | Cartões, cabeçalho |
| `--surface-2` | `#251B45` | Bolha do Ozzy, inputs |
| `--primary` | `#FF6B35` | Ação principal, bolha do usuário, botão enviar (laranja "amplificador valvulado") |
| `--accent` | `#F7C948` | Destaques, promoções, detalhes dourados ("latão do instrumento") |
| `--accent-2` | `#7C5CFF` | Elementos secundários, links, indicadores |
| `--success` | `#3DDC97` | Status online, confirmações |
| `--text` | `#F5F1FF` | Texto principal |
| `--text-muted` | `#A79FC4` | Texto secundário, horários |
| `--danger` | `#FF4D6D` | Erros |

Gradiente de marca: `#FF6B35 → #F7C948` (cabeçalho do botão, brilho do logo).  
Gradiente de fundo sutil: `#0F0B1A → #1A1330`.

### Tipografia
- **Títulos / marca:** *Poppins* (600–700) ou *Space Grotesk* (alternativa mais "tech")
- **Corpo / chat:** *Inter* (400–500)
- Detalhes (horários, tags): *Inter* 12px, `--text-muted`

### Forma e estilo
- Cantos bem arredondados (bolhas 20px; cartões 16px; botões pill)
- Sombras suaves com leve brilho colorido (glow laranja no botão principal)
- Ícones de linha, traço fino (estilo Lucide/Phosphor)
- Textura opcional muito sutil no fundo: linhas de pentagrama ou ondas sonoras com 4–6% de opacidade
- Animações discretas: bolha entrando com fade/slide, indicador de "digitando" como **3 barras de equalizador** pulsando

---

## 3. Persona visual do Ozzy (avatar)

**Quem é:** assistente amigável da loja, jovem, descontraído, apaixonado por música. É um mascote, não um humano realista.

**Opções de conceito (escolher uma):**
- **A. Robô-fone:** cabeça arredondada de robô simpático com **fones de ouvido grandes** (as conchas fazem de "orelhas"), olhos expressivos em LED, sorriso suave.
- **B. Mascote Violão/Palheta:** um violão acústico animado ou palheta com rosto, olhos e fones de ouvido.
- **C. Personagem ilustrado:** figura simpática com boné, fones no pescoço e uma palheta de violão como detalhe.

**Recomendação:** **A (robô-fone)**, pois comunica "assistente virtual" e "música" com clareza e funciona bem em tamanho pequeno.

**Direção de arte:** ilustração 3D suave/flat com gradientes, cores da paleta (corpo em roxo `#7C5CFF`, fones laranja `#FF6B35`, detalhes dourados), fundo transparente, olhos grandes e brilhantes, expressão acolhedora.

**Variações de expressão (para o chat):**
1. Neutro/sorrindo (padrão)
2. Feliz (resposta bem-sucedida)
3. Pensando (buscando informação, olhos para cima)
4. Empático/preocupado (cliente insatisfeito)
5. Piscando/acenando (boas-vindas)

**Formatos:** círculo 40×40 (mensagens), 64×64 (cabeçalho), 160×160 (tela de boas-vindas), com borda de 2px em gradiente laranja→dourado e indicador verde de "online".

---

## 4. Estrutura da UI do chat

### Layout desktop (card central, 420–480px de largura em fundo com gradiente, ou tela dividida)
```
┌────────────────────────────────────┐
│ [avatar] Ozzy • Empório da Música  │  ← cabeçalho (status "Online agora" ●)
│          assistente de atendimento │     botão "Falar com atendente" (ícone fone)
├────────────────────────────────────┤
│                                    │
│  [avatar] Fala, músico! Eu sou o   │  ← bolha do Ozzy (surface-2)
│           Ozzy. Como posso ajudar? │
│                                    │
│  [chips: 🎸 Promoções] [📦 Meu pedido]│  ← sugestões rápidas
│  [🔁 Trocas e devoluções] [🚚 Frete] │
│                                    │
│            Quero ver violões  ───► │  ← bolha do usuário (primary)
│                                    │
│  [cartão de produto: imagem, nome, │
│   preço, selo de promoção, botão]  │
│                                    │
├────────────────────────────────────┤
│ [ Escreva sua mensagem...    ] [➤] │  ← input + botão enviar (pill)
│  Ozzy responde apenas sobre a loja │  ← microcopy
└────────────────────────────────────┘
```

### Layout mobile
Tela cheia, cabeçalho compacto fixo, input fixo no rodapé, chips roláveis horizontalmente, bolhas até 85% da largura.

### Telas/estados a prototipar
1. **Boas-vindas** (avatar grande, saudação, 4 chips de sugestão)
2. **Conversa ativa** (mensagens, horário, "digitando" com equalizador)
3. **Resposta com cartão de produto** (carrossel horizontal de 2–3 produtos)
4. **Resposta de política** (bolha com selo "📄 Política da loja" e link "ver detalhes")
5. **Cliente insatisfeito** (Ozzy com expressão empática + botão destacado "Falar com um atendente")
6. **Transferência para atendente** (cartão de confirmação: "Pronto! Um atendente vai te chamar em breve", status do ticket)
7. **Estado de erro/offline** (mensagem amigável + botão "Tentar de novo")
8. **Versão mobile** das telas 1, 2 e 5

---

## 5. Componentes a definir

| Componente | Detalhes |
|---|---|
| Cabeçalho | Avatar com ponto verde, nome, subtítulo, botão de atendente |
| Bolha Ozzy | Fundo `--surface-2`, canto inferior-esquerdo menos arredondado, avatar ao lado |
| Bolha usuário | Fundo `--primary`, texto escuro/branco com contraste AA, alinhada à direita |
| Chips de sugestão | Pill com borda `--accent-2`, hover com preenchimento |
| Indicador "digitando" | 3–4 barras verticais animadas (equalizador) |
| Cartão de produto | Imagem 1:1, nome, preço, preço riscado e selo "-20%" dourado, botão "Ver mais" |
| Selo de política | Tag pequena com ícone de documento |
| Cartão de atendente | Ícone de fone, texto, botão primário "Falar com atendente" |
| Input | Pill escuro, foco com borda gradiente, botão enviar circular laranja com glow |
| Rodapé/microcopy | "O Ozzy responde apenas sobre a Empório da Música" |

**Acessibilidade:** contraste mínimo AA, alvos de toque ≥ 44px, foco visível, rótulos `aria-label` nos botões de ícone.

---

## 6. Tom de voz (microcopy da interface)

- Saudação: "Fala, músico! 🎶 Eu sou o Ozzy, assistente da Empório da Música. No que posso te ajudar hoje?"
- Placeholder do input: "Pergunte sobre produtos, pedidos, trocas..."
- Digitando: "Ozzy está afinando a resposta..."
- Erro: "Opa, desafinei aqui! Tenta de novo?"
- Atendente: "Quer que eu chame alguém do nosso time? É rapidinho."

---

## 7. Prompts para colar no Google Stitch (em ordem)

> Dica: gere uma tela por vez, aprove e só então peça variações. Primeiro cole o **Prompt 0 (sistema de design)** e mantenha-o como referência nas telas seguintes.

### Prompt 0 — Sistema de design
```
Crie o sistema de design de uma interface de chat de atendimento chamada "Ozzy" para a loja de instrumentos musicais "Empório da Música". Tema escuro moderno e acolhedor, inspirado em instrumentos acústicos, elétricos, estúdio e palco. Cores: fundo #0F0B1A, superfícies #1A1330 e #251B45, primária laranja #FF6B35, destaque dourado #F7C948, secundária roxo #7C5CFF, sucesso #3DDC97, texto #F5F1FF, texto secundário #A79FC4. Fontes: Poppins para títulos e Inter para o corpo. Cantos bem arredondados (20px nas bolhas, 16px nos cartões, botões em formato pill), sombras suaves com leve brilho laranja no botão principal, ícones de linha com traço fino. Textura sutil de pentagrama ou ondas sonoras no fundo com 5% de opacidade.
```

### Prompt 1 — Tela de boas-vindas (desktop)
```
Tela de boas-vindas de um chat em card central de 460px de largura sobre fundo em gradiente escuro (#0F0B1A para #1A1330). Cabeçalho com avatar circular do assistente Ozzy (um robô simpático com fones de ouvido grandes, em roxo e laranja), nome "Ozzy", subtítulo "Assistente da Empório da Música", ponto verde "Online agora" e um botão de ícone de fone de ouvido para "Falar com atendente". No corpo, uma bolha de mensagem do Ozzy: "Fala, músico! 🎶 Eu sou o Ozzy, assistente da Empório da Música. No que posso te ajudar hoje?". Abaixo, quatro chips de sugestão: "🎸 Promoções", "📦 Meu pedido", "🔁 Trocas e devoluções", "🚚 Frete e prazos". No rodapé, campo de texto em formato pill com placeholder "Pergunte sobre produtos, pedidos, trocas..." e botão de enviar circular laranja com brilho suave. Microcopy abaixo: "O Ozzy responde apenas sobre a Empório da Música". Estilo moderno, acolhedor, com personalidade musical.
```

### Prompt 2 — Conversa ativa
```
Mesma interface, agora com uma conversa em andamento. Mensagem do usuário à direita em bolha laranja (#FF6B35): "Quero ver violões de aço até R$ 1.500". Resposta do Ozzy à esquerda com mini avatar, em bolha #251B45. Abaixo, um carrossel horizontal com 3 cartões de produto: imagem quadrada do violão, nome, preço em destaque, preço antigo riscado, selo dourado "-15%" e botão "Ver detalhes". Horários discretos nas mensagens. Inclua também o indicador de "digitando" do Ozzy como 4 barras verticais de equalizador animadas, com o texto "Ozzy está afinando a resposta...".
```

### Prompt 3 — Resposta de política da loja
```
Variação da conversa: o usuário pergunta "Qual o prazo para trocar um produto?". O Ozzy responde numa bolha com texto curto e claro, destacando o prazo em negrito, e abaixo um selo pequeno com ícone de documento e o texto "Política de trocas e devoluções". Ao final da bolha, duas sugestões rápidas: "Como solicitar troca" e "Falar com atendente".
```

### Prompt 4 — Cliente insatisfeito + atendente
```
Variação da conversa: o usuário escreve com tom irritado "Meu pedido atrasou de novo, isso é um absurdo!". O Ozzy responde com uma bolha empática, o avatar mostra expressão preocupada/empática, e logo abaixo aparece um cartão de destaque com borda em gradiente laranja-dourado, ícone de fone de ouvido e o texto "Quer que eu chame alguém do nosso time agora? É rapidinho." com um botão primário "Falar com um atendente" e um botão secundário "Ver status do pedido".
```

### Prompt 5 — Transferência para atendente
```
Cartão de confirmação dentro do chat: ícone de check verde, título "Tudo certo!", texto "Já avisei nosso time. Um atendente vai te chamar em breve.", um chip de status "Ticket #1234 • Aguardando atendente" e o avatar do Ozzy sorrindo ao lado. Mantenha o campo de mensagem habilitado abaixo.
```

### Prompt 6 — Estado de erro
```
Estado de erro no chat: bolha do Ozzy com a mensagem "Opa, desafinei aqui! Tenta de novo?" e um botão "Tentar novamente" com ícone de recarregar, em tom amigável, sem aspecto alarmante. Use o vermelho-rosado #FF4D6D apenas em um detalhe sutil.
```

### Prompt 7 — Versão mobile
```
Adapte as telas de boas-vindas, conversa com cartões de produto e cliente insatisfeito para mobile (390x844). Tela cheia, cabeçalho compacto fixo no topo, chips de sugestão em rolagem horizontal, bolhas com até 85% da largura, campo de entrada fixo no rodapé com área de toque de pelo menos 44px.
```

### Prompt 8 — Tema claro (opcional)
```
Crie uma variação em tema claro da mesma interface: fundo #FFF8F0, superfícies brancas, bolha do Ozzy em #F1EBFF, bolha do usuário em #FF6B35, texto #1B1530, mantendo laranja, dourado e roxo como destaques.
```

---

## 8. Geração do logo e do avatar

O Stitch é voltado a telas de interface. Para **logo** e **avatar do Ozzy**, recomenda-se gerá-los com uma ferramenta de imagem (por exemplo, o Gemini com geração de imagens) e depois importá-los no Stitch como referência.

### Prompt — Logo
```
Logo vetorial minimalista para uma loja de música chamada "Empório da Música". Símbolo: uma palheta estilizada (ou silhueta de violão/guitarra) cujo centro forma a letra "E", com uma pequena nota musical dourada. Paleta: laranja #FF6B35, dourado #F7C948 e roxo #7C5CFF. Estilo moderno, limpo, formas arredondadas. Fundo transparente. Gere versão horizontal com o nome "Empório da Música" em tipografia sem serifa geométrica (estilo Poppins) e versão apenas com o símbolo.
```

### Prompt — Avatar do Ozzy
```
Mascote "Ozzy", um robô assistente simpático com cabeça arredondada, olhos grandes em LED brilhantes e sorriso suave, usando fones de ouvido grandes laranja (#FF6B35) com detalhes dourados (#F7C948). Corpo/cabeça em roxo #7C5CFF com gradiente suave. Ilustração 3D suave, acolhedora, centralizada, fundo transparente, vista frontal em busto. Gere 5 expressões: neutro sorrindo, feliz, pensando, empático/preocupado e acenando.
```

---

## 9. Entregáveis para o desenvolvimento

Ao final da etapa visual, exportar e entregar ao projeto Python:
- [ ] Código HTML/CSS das telas (desktop + mobile)
- [ ] `logo-horizontal`, `logo-simbolo` (PNG/SVG, fundo transparente)
- [ ] `ozzy-neutro`, `ozzy-feliz`, `ozzy-pensando`, `ozzy-empatico`, `ozzy-aceno` (PNG, fundo transparente, 512px)
- [ ] `favicon` (32px e 180px)
- [ ] Tokens de cor e fonte (copiar a tabela da seção 2 para o CSS como variáveis `:root`)
- [ ] Lista dos estados de interface aprovados (seção 4)

**Requisitos técnicos para facilitar a integração:** pedir ao Stitch que mantenha IDs/classes claros nos elementos principais — `#chat-messages`, `#chat-input`, `#send-button`, `.bubble-user`, `.bubble-ozzy`, `.product-card`, `.suggestion-chip`, `#typing-indicator`, `#handoff-card` — para que o backend e o JS mínimo consigam conectar o chat.