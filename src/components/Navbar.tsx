import React from 'react';
import { ActiveTab, CartItem } from '../types';
import { ShoppingBag, Volume2, VolumeX, Sparkles } from 'lucide-react';
import { soundSynth } from '../services/audioSynthesizer';

interface NavbarProps {
  activeTab: ActiveTab;
  setActiveTab: (tab: ActiveTab) => void;
  cart: CartItem[];
  setIsCartOpen: (open: boolean) => void;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  cart,
  setIsCartOpen,
}) => {
  const [isMuted, setIsMuted] = React.useState(soundSynth.getMuted());
  const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  const toggleSound = () => {
    const muted = soundSynth.toggleMute();
    setIsMuted(muted);
  };

  return (
    <header className="sticky top-0 z-40 w-full bg-[#1A1330]/90 backdrop-blur-md border-b border-[#7C5CFF]/20 px-4 lg:px-8 py-3.5 transition-all">
      <div className="max-w-7xl mx-auto flex items-center justify-between gap-8">
        {/* Zone 1: Brand Wordmark */}
        <button
          onClick={() => setActiveTab('chat')}
          className="flex items-center gap-2.5 text-left focus:outline-none group shrink-0"
        >
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#FF6B35] to-[#F7C948] flex items-center justify-center text-white shadow-md shadow-[#FF6B35]/25 group-hover:scale-105 transition-transform">
            <span className="font-bold text-sm tracking-tighter">EM</span>
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight text-[#F5F1FF] font-['Poppins'] whitespace-nowrap block">
              Empório da Música
            </span>
          </div>
        </button>

        {/* Zone 2: 4-5 Clean Single-Line Navigation Links */}
        <nav className="hidden md:flex items-center gap-6 text-sm font-medium">
          <button
            onClick={() => setActiveTab('chat')}
            className={`whitespace-nowrap transition-colors py-1 relative ${
              activeTab === 'chat'
                ? 'text-[#FF6B35] font-semibold'
                : 'text-[#A79FC4] hover:text-[#F5F1FF]'
            }`}
          >
            Assistente Ozzy
            {activeTab === 'chat' && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#FF6B35] rounded-full" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('catalog')}
            className={`whitespace-nowrap transition-colors py-1 relative ${
              activeTab === 'catalog'
                ? 'text-[#FF6B35] font-semibold'
                : 'text-[#A79FC4] hover:text-[#F5F1FF]'
            }`}
          >
            Showroom
            {activeTab === 'catalog' && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#FF6B35] rounded-full" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('tone-builder')}
            className={`whitespace-nowrap transition-colors py-1 relative ${
              activeTab === 'tone-builder'
                ? 'text-[#FF6B35] font-semibold'
                : 'text-[#A79FC4] hover:text-[#F5F1FF]'
            }`}
          >
            Laboratório de Timbres
            {activeTab === 'tone-builder' && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#FF6B35] rounded-full" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('luthieria')}
            className={`whitespace-nowrap transition-colors py-1 relative ${
              activeTab === 'luthieria'
                ? 'text-[#FF6B35] font-semibold'
                : 'text-[#A79FC4] hover:text-[#F5F1FF]'
            }`}
          >
            Luthieria
            {activeTab === 'luthieria' && (
              <span className="absolute bottom-0 left-0 right-0 h-0.5 bg-[#FF6B35] rounded-full" />
            )}
          </button>

          <button
            onClick={() => setActiveTab('python-hub')}
            className={`whitespace-nowrap flex items-center gap-1.5 transition-colors py-1 px-2.5 rounded-full border border-[#7C5CFF]/30 ${
              activeTab === 'python-hub'
                ? 'bg-[#7C5CFF]/20 text-[#F7C948] border-[#F7C948]/50 font-semibold'
                : 'bg-[#251B45]/50 text-[#A79FC4] hover:text-[#F5F1FF]'
            }`}
          >
            <span>🐍 Python App & API</span>
          </button>
        </nav>

        {/* Zone 3: 1 Primary Action (Cart & Sound) */}
        <div className="flex items-center gap-3 shrink-0">
          <button
            onClick={toggleSound}
            title={isMuted ? 'Ativar áudio de demonstração' : 'Silenciar áudio'}
            className="p-2 rounded-full bg-[#251B45] text-[#A79FC4] hover:text-[#F5F1FF] hover:bg-[#32245e] transition-colors"
            aria-label="Controle de Áudio"
          >
            {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4 text-[#F7C948]" />}
          </button>

          <button
            onClick={() => setIsCartOpen(true)}
            className="relative flex items-center gap-2 px-4 py-2 bg-[#FF6B35] hover:bg-[#ff7b47] text-white text-xs font-semibold rounded-full shadow-lg shadow-[#FF6B35]/25 transition-all hover:scale-[1.02] active:scale-[0.98] whitespace-nowrap shrink-0"
          >
            <ShoppingBag className="w-4 h-4" />
            <span className="hidden sm:inline">Carrinho</span>
            {totalCartCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 bg-[#0F0B1A] text-[#F7C948] text-[11px] font-bold rounded-full">
                {totalCartCount}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Mobile Nav Bar */}
      <div className="md:hidden flex items-center justify-around pt-3 mt-2 border-t border-[#7C5CFF]/15 text-xs text-[#A79FC4]">
        <button
          onClick={() => setActiveTab('chat')}
          className={`py-1 px-2 ${activeTab === 'chat' ? 'text-[#FF6B35] font-semibold' : ''}`}
        >
          Ozzy
        </button>
        <button
          onClick={() => setActiveTab('catalog')}
          className={`py-1 px-2 ${activeTab === 'catalog' ? 'text-[#FF6B35] font-semibold' : ''}`}
        >
          Showroom
        </button>
        <button
          onClick={() => setActiveTab('tone-builder')}
          className={`py-1 px-2 ${activeTab === 'tone-builder' ? 'text-[#FF6B35] font-semibold' : ''}`}
        >
          Timbres
        </button>
        <button
          onClick={() => setActiveTab('luthieria')}
          className={`py-1 px-2 ${activeTab === 'luthieria' ? 'text-[#FF6B35] font-semibold' : ''}`}
        >
          Luthieria
        </button>
        <button
          onClick={() => setActiveTab('python-hub')}
          className={`py-1 px-2 text-[#F7C948] font-medium ${activeTab === 'python-hub' ? 'underline' : ''}`}
        >
          Python
        </button>
      </div>
    </header>
  );
};
