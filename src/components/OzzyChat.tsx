import React, { useState, useRef, useEffect } from 'react';
import { Send, Sparkles, Volume2, VolumeX, Trash2, Code2, Check, ArrowRight } from 'lucide-react';
import { ChatMessage, Product } from '../types';
import { INITIAL_CHAT_MESSAGES, OZZY_AVATAR } from '../data/mockProducts';
import { ProductCard } from './ProductCard';
import { HandoffCard } from './HandoffCard';
import { soundSynth } from '../services/audioSynthesizer';
import { getOzzyResponse } from '../services/ozzyBrain';

interface OzzyChatProps {
  onAddToCart: (product: Product) => void;
}

export const OzzyChat: React.FC<OzzyChatProps> = ({ onAddToCart }) => {
  const [messages, setMessages] = useState<ChatMessage[]>(INITIAL_CHAT_MESSAGES);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const [isMuted, setIsMuted] = useState(soundSynth.getMuted());
  const [showPythonCode, setShowPythonCode] = useState(false);
  const [copiedCode, setCopiedCode] = useState(false);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSendMessage = async (textToSend?: string) => {
    const text = (textToSend || input).trim();
    if (!text || isTyping) return;

    const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text,
      timestamp: time,
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInput('');
    setIsTyping(true);

    try {
      // First try calling our Python backend API on /api/chat
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text }),
      });

      if (res.ok) {
        const data = await res.json();
        // Give a realistic feeling of Ozzy tuning recommendations
        setTimeout(() => {
          setMessages((prev) => [...prev, data]);
          setIsTyping(false);
        }, 650);
        return;
      }
    } catch {
      // Fallback to client-side brain if Python server is warming up
    }

    // Fallback
    setTimeout(async () => {
      const response = await getOzzyResponse(text);
      setMessages((prev) => [...prev, response]);
      setIsTyping(false);
    }, 700);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleClearChat = () => {
    setMessages([
      {
        id: `ozzy-${Date.now()}`,
        sender: 'ozzy',
        text: 'Conversa reiniciada! Como posso te ajudar a encontrar o som perfeito hoje?',
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        chips: [
          '🎸 Recomende uma guitarra até R$ 20.000',
          '🔥 O que são os amplificadores valvulados?',
          '🔧 Agendar serviço na Luthieria',
        ],
      },
    ]);
  };

  const toggleSound = () => {
    const muted = soundSynth.toggleMute();
    setIsMuted(muted);
  };

  const copyPythonCode = () => {
    const code = `import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ozzy Chatbot Python Core
def process_ozzy_chat(message: str):
    text = message.lower()
    if "guitarra" in text or "les paul" in text:
        return {
            "sender": "ozzy",
            "text": "A Gibson Les Paul Standard 50s Sunburst é o ícone supremo do rock clássico!",
            "chips": ["Ouvir Timbre", "Ver Amplificadores"]
        }
    return {
        "sender": "ozzy",
        "text": "Olá! Sou o Ozzy, especialista musical do Empório da Música."
    }
`;
    navigator.clipboard.writeText(code);
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <div className="relative w-full flex flex-col items-center justify-center p-3 sm:p-6 lg:p-8">
      {/* Centered Chat Card Structure: 420px–480px width on desktop */}
      <div className="w-full max-w-[480px] bg-[#1A1330] rounded-2xl border border-[#7C5CFF]/25 shadow-2xl shadow-black/60 flex flex-col h-[82vh] max-h-[780px] overflow-hidden relative">
        
        {/* Chat Card Header */}
        <div className="bg-[#251B45] px-4 py-3 border-b border-[#7C5CFF]/20 flex items-center justify-between shrink-0">
          <div className="flex items-center gap-3">
            <div className="relative">
              <img
                src={OZZY_AVATAR}
                alt="Ozzy Mascot"
                referrerPolicy="no-referrer"
                className="w-10 h-10 rounded-full object-cover border-2 border-[#FF6B35] shadow-md shadow-[#FF6B35]/30"
              />
              <span className="absolute bottom-0 right-0 w-3 h-3 bg-[#3DDC97] border-2 border-[#251B45] rounded-full" />
            </div>

            <div>
              <div className="flex items-center gap-1.5">
                <h3 className="font-['Poppins'] font-semibold text-sm text-[#F5F1FF]">
                  Ozzy
                </h3>
                <span className="text-[10px] font-mono px-1.5 py-0.2 bg-[#0F0B1A] text-[#F7C948] rounded border border-[#F7C948]/30">
                  🐍 Python 3.10
                </span>
              </div>
              <p className="text-[11px] text-[#A79FC4] flex items-center gap-1">
                <span className="w-1.5 h-1.5 bg-[#FF6B35] rounded-full animate-ping"></span>
                Consultor Musical • Empório
              </p>
            </div>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={toggleSound}
              title={isMuted ? 'Ativar Áudio' : 'Desativar Áudio'}
              className="p-1.5 rounded-lg text-[#A79FC4] hover:text-[#F5F1FF] hover:bg-[#1A1330] transition-colors"
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4 text-[#F7C948]" />}
            </button>

            <button
              onClick={() => setShowPythonCode(!showPythonCode)}
              title="Ver Código Python do Chat"
              className={`p-1.5 rounded-lg transition-colors ${
                showPythonCode ? 'bg-[#7C5CFF]/30 text-[#F7C948]' : 'text-[#A79FC4] hover:text-[#F5F1FF] hover:bg-[#1A1330]'
              }`}
            >
              <Code2 className="w-4 h-4" />
            </button>

            <button
              onClick={handleClearChat}
              title="Reiniciar Conversa"
              className="p-1.5 rounded-lg text-[#A79FC4] hover:text-[#FF4D6D] hover:bg-[#1A1330] transition-colors"
            >
              <Trash2 className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Python Code Drawer if toggled */}
        {showPythonCode && (
          <div className="bg-[#0F0B1A] border-b border-[#7C5CFF]/20 p-3 text-xs font-mono text-[#F5F1FF] max-h-48 overflow-y-auto shrink-0 transition-all">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[#F7C948] font-bold">🐍 backend/server.py</span>
              <button
                onClick={copyPythonCode}
                className="flex items-center gap-1 px-2 py-0.5 rounded bg-[#251B45] text-[11px] text-[#A79FC4] hover:text-white"
              >
                {copiedCode ? <Check className="w-3 h-3 text-[#3DDC97]" /> : null}
                <span>{copiedCode ? 'Copiado!' : 'Copiar Código'}</span>
              </button>
            </div>
            <pre className="text-[11px] text-[#A79FC4] leading-relaxed select-all">
{`# Backend Python nativo processando requisições do chat
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

def process_ozzy_chat(message: str):
    # Inteligência de timbres e catálogo
    return {"sender": "ozzy", "text": "..."}`}
            </pre>
          </div>
        )}

        {/* Chat Message Scroll Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`flex flex-col ${
                msg.sender === 'user' ? 'items-end' : 'items-start'
              }`}
            >
              <div
                className={`flex items-end gap-2 max-w-[92%] ${
                  msg.sender === 'user' ? 'flex-row-reverse' : 'flex-row'
                }`}
              >
                {/* Ozzy Mascot Avatar Thumbnail next to Ozzy's bubble */}
                {msg.sender === 'ozzy' && (
                  <img
                    src={OZZY_AVATAR}
                    alt="Ozzy"
                    referrerPolicy="no-referrer"
                    className="w-7 h-7 rounded-full object-cover shrink-0 mb-1 border border-[#FF6B35]/40"
                  />
                )}

                {/* Message Bubble */}
                <div
                  className={`p-3.5 text-xs sm:text-sm leading-relaxed transition-all shadow-md ${
                    msg.sender === 'user'
                      ? 'bg-[#FF6B35] text-white rounded-2xl rounded-br-none shadow-[#FF6B35]/20'
                      : 'bg-[#251B45] text-[#F5F1FF] rounded-2xl rounded-bl-none border border-[#7C5CFF]/15'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.text}</p>
                </div>
              </div>

              {/* Timestamp */}
              <span className="text-[10px] text-[#A79FC4] mt-1 px-1">
                {msg.timestamp}
              </span>

              {/* Embedded Product Card if present */}
              {msg.productCard && (
                <div className="w-full mt-2 pl-9">
                  <ProductCard
                    product={msg.productCard}
                    onAddToCart={onAddToCart}
                    isCompact={true}
                  />
                </div>
              )}

              {/* Embedded Handoff Card if present */}
              {msg.handoffCard && (
                <div className="w-full mt-2 pl-9">
                  <HandoffCard {...msg.handoffCard} />
                </div>
              )}

              {/* Suggestion Chips */}
              {msg.chips && msg.chips.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2.5 pl-9">
                  {msg.chips.map((chip, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSendMessage(chip)}
                      className="text-[11px] font-medium py-1 px-3 rounded-full bg-[#1A1330] hover:bg-[#7C5CFF] text-[#F5F1FF] border border-[#7C5CFF]/40 hover:border-[#7C5CFF] transition-all hover:scale-[1.02] shadow-sm text-left"
                    >
                      {chip}
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}

          {/* Typing Indicator: Animated 4-bar vertical equalizer */}
          {isTyping && (
            <div className="flex items-end gap-2">
              <img
                src={OZZY_AVATAR}
                alt="Ozzy"
                referrerPolicy="no-referrer"
                className="w-7 h-7 rounded-full object-cover shrink-0 mb-1 border border-[#FF6B35]/40"
              />
              <div className="bg-[#251B45] px-4 py-3 rounded-2xl rounded-bl-none border border-[#7C5CFF]/20 flex items-center gap-3">
                {/* 4-bar vertical equalizer */}
                <div className="flex items-end gap-1 h-5">
                  <span className="w-1 bg-[#FF6B35] rounded-full animate-eq-1"></span>
                  <span className="w-1 bg-[#F7C948] rounded-full animate-eq-2"></span>
                  <span className="w-1 bg-[#7C5CFF] rounded-full animate-eq-3"></span>
                  <span className="w-1 bg-[#FF6B35] rounded-full animate-eq-4"></span>
                </div>
                <span className="text-xs text-[#A79FC4] italic">
                  Ozzy está afinando as recomendações...
                </span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input: Full-width pill container with --surface-2 */}
        <div className="p-3 bg-[#1A1330] border-t border-[#7C5CFF]/15 shrink-0">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex items-center gap-2 bg-[#251B45] rounded-full p-1.5 pl-4 border border-[#7C5CFF]/25 focus-within:border-[#FF6B35] transition-all shadow-inner"
          >
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Pergunte ao Ozzy sobre guitarras, timbres, amps..."
              className="flex-1 bg-transparent text-xs sm:text-sm text-[#F5F1FF] placeholder-[#A79FC4] focus:outline-none"
            />

            <button
              type="submit"
              disabled={!input.trim() || isTyping}
              className={`w-9 h-9 rounded-full flex items-center justify-center transition-all ${
                input.trim() && !isTyping
                  ? 'bg-[#FF6B35] text-white shadow-md shadow-[#FF6B35]/40 hover:scale-105 active:scale-95'
                  : 'bg-[#1A1330] text-[#A79FC4] cursor-not-allowed'
              }`}
            >
              <Send className="w-4 h-4 fill-current ml-0.5" />
            </button>
          </form>
        </div>

      </div>
    </div>
  );
};
