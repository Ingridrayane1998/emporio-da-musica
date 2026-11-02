document.addEventListener('DOMContentLoaded', () => {
  const messagesContainer = document.getElementById('messagesContainer');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const typingIndicator = document.getElementById('typingIndicator');
  const muteBtn = document.getElementById('muteBtn');
  const clearBtn = document.getElementById('clearBtn');
  const suggestionChips = document.querySelectorAll('.suggestion-chip');

  let isTyping = false;
  // Gerenciamento de sessao: ID unico por aba/sessao de navegador
  let sessionId = sessionStorage.getItem('ozzy_session_id') || null;

  // Inicia sessao ao carregar a pagina
  async function initSession() {
    if (!sessionId) {
      try {
        const res = await fetch('/api/session', { method: 'POST' });
        const data = await res.json();
        sessionId = data.session_id;
        sessionStorage.setItem('ozzy_session_id', sessionId);
      } catch (e) {
        sessionId = 'local-' + Math.random().toString(36).slice(2);
      }
    }
  }
  initSession();

  // Format currency
  function formatBRL(val) {
    return new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(val);
  }

  // Get current HH:MM
  function getCurrentTime() {
    return new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
  }

  function scrollToBottom() {
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function setTyping(loading) {
    isTyping = loading;
    typingIndicator.style.display = loading ? 'flex' : 'none';
    sendBtn.disabled = loading;
    chatInput.disabled = loading;
    if (!loading) {
      chatInput.focus();
    }
    scrollToBottom();
  }

  // Append user message
  function appendUserMessage(text) {
    const row = document.createElement('div');
    row.className = 'message-row user';
    row.innerHTML = `
      <div class="msg-body">
        <div class="msg-bubble">${escapeHtml(text)}</div>
        <div class="msg-meta">
          <span>${getCurrentTime()}</span>
        </div>
      </div>
    `;
    messagesContainer.appendChild(row);
    scrollToBottom();
  }

  // Append Ozzy message
  function appendOzzyMessage(data) {
    const row = document.createElement('div');
    row.className = 'message-row ozzy';

    let contentHtml = '';
    const text = typeof data === 'string' ? data : (data.reply || data.text || '');

    // Convert newlines to breaks or render simple text
    const formattedText = escapeHtml(text).replace(/\n/g, '<br>');
    contentHtml += `<div class="msg-bubble">${formattedText}</div>`;

    // Attached products
    if (data.products && Array.isArray(data.products) && data.products.length > 0) {
      data.products.forEach(p => {
        contentHtml += renderProductCard(p);
      });
    }

    // Attached handoff / ticket
    if (data.handoff || data.ticket) {
      contentHtml += renderHandoffCard(data.handoff || data.ticket);
    }

    row.innerHTML = `
      <img src="/static/images/ozzy_mascot_avatar_1793632768308.jpg" alt="Ozzy" class="msg-avatar">
      <div class="msg-body">
        ${contentHtml}
        <div class="msg-meta">
          <span>Ozzy</span> &bull; <span>${getCurrentTime()}</span>
        </div>
      </div>
    `;

    messagesContainer.appendChild(row);
    scrollToBottom();
  }

  function renderProductCard(p) {
    const imgUrl = p.image || '/static/images/electric_guitar_sunburst_1793632768094.jpg';
    const oldPriceHtml = p.originalPrice ? `<span class="product-old-price">${formatBRL(p.originalPrice)}</span>` : '';
    const discountHtml = p.discountPercent ? `<span class="product-discount-tag">-${p.discountPercent}%</span>` : '';
    const toneType = p.audioToneType || 'rock';

    return `
      <div class="product-card">
        <div class="product-header">
          <img src="${imgUrl}" alt="${escapeHtml(p.name)}" class="product-img">
          <div class="product-info">
            <span class="product-brand">${escapeHtml(p.brand || 'Boutique')}</span>
            <div class="product-title">${escapeHtml(p.name)}</div>
            <div class="product-prices">
              <span class="product-price">${formatBRL(p.price)}</span>
              ${oldPriceHtml}
              ${discountHtml}
            </div>
          </div>
        </div>
        <div class="product-actions">
          <button class="btn-tone" onclick="window.soundSynth.playTone('${toneType}')">
            &#9835; Ouvir Timbre
          </button>
        </div>
      </div>
    `;
  }

  function renderHandoffCard(h) {
    const ticketId = h.ticket_id || h.ticketId || '#TK-9021';
    const reason = h.reason || h.motivo || 'Atendimento com especialista humano';
    const priority = h.priority || h.prioridade || 'Alta';

    return `
      <div class="handoff-card">
        <div class="handoff-header">
          <span class="handoff-badge">Ticket ${priority}</span>
          <span class="handoff-ticket">${ticketId}</span>
        </div>
        <div class="handoff-title">Especialista Notificado</div>
        <div class="handoff-desc">${escapeHtml(reason)}. Nosso luthier/atendente foi acionado e entrarÃ¡ em contato em instantes!</div>
      </div>
    `;
  }

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Send message
  async function sendMessage(text) {
    const msg = (text || chatInput.value).trim();
    if (!msg || isTyping) return;

    appendUserMessage(msg);
    chatInput.value = '';
    setTyping(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg, session_id: sessionId })
      });

      if (!response.ok) {
        throw new Error(`HTTP error ${response.status}`);
      }

      const data = await response.json();
      setTimeout(() => {
        appendOzzyMessage(data);
        setTyping(false);
      }, 400);

    } catch (err) {
      console.error("Erro na comunicaÃ§Ã£o com a API:", err);
      setTimeout(() => {
        appendOzzyMessage({
          reply: "Opa, tive uma pequena oscilaÃ§Ã£o na conexÃ£o com o palco! Mas jÃ¡ estou afinando tudo aqui de novo. Pode repetir sua pergunta?"
        });
        setTyping(false);
      }, 500);
    }
  }

  // Event Listeners
  sendBtn.addEventListener('click', () => sendMessage());

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  suggestionChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const prompt = chip.getAttribute('data-prompt');
      if (prompt) {
        sendMessage(prompt);
      }
    });
  });

  muteBtn.addEventListener('click', () => {
    const isMuted = window.soundSynth.toggleMute();
    muteBtn.innerHTML = isMuted ? '&#128263;' : '&#128266;';
    muteBtn.title = isMuted ? 'Desmutar Ã¡udio' : 'Mutar Ã¡udio';
  });

  clearBtn.addEventListener('click', () => {
    if (confirm("Deseja limpar as mensagens do chat?")) {
      messagesContainer.innerHTML = '';
      appendOzzyMessage({
        reply: "Palco zerado! Como posso te ajudar agora? Quer encontrar um instrumento, checar um pedido ou saber nossas polÃ­ticas?"
      });
    }
  });
});

