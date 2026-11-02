import React, { useState } from 'react';
import { OzzyChat } from './components/OzzyChat';
import { CartModal } from './components/CartModal';
import { CartItem, Product } from './types';
import { STORE_HERO } from './data/mockProducts';
import { ShoppingBag, Terminal, Music } from 'lucide-react';

export default function App() {
  const [cart, setCart] = useState<CartItem[]>([]);
  const [isCartOpen, setIsCartOpen] = useState(false);

  const handleAddToCart = (product: Product) => {
    setCart((prev) => {
      const existing = prev.find((item) => item.product.id === product.id);
      if (existing) {
        return prev.map((item) =>
          item.product.id === product.id
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
      }
      return [...prev, { product, quantity: 1 }];
    });
  };

  const handleUpdateQuantity = (id: string, delta: number) => {
    setCart((prev) =>
      prev
        .map((item) => {
          if (item.product.id === id) {
            const newQty = item.quantity + delta;
            return newQty > 0 ? { ...item, quantity: newQty } : null;
          }
          return item;
        })
        .filter(Boolean) as CartItem[]
    );
  };

  const handleRemoveItem = (id: string) => {
    setCart((prev) => prev.filter((item) => item.product.id !== id));
  };

  const handleClearCart = () => {
    setCart([]);
  };

  const totalCartCount = cart.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <div className="min-h-screen bg-[#0F0B1A] text-[#F5F1FF] flex flex-col relative overflow-hidden font-['Inter',sans-serif]">
      {/* Background Visual Layer: Boutique Shop Stage with warm tube-amp glow */}
      <div className="absolute inset-0 pointer-events-none z-0">
        <img
          src={STORE_HERO}
          alt="Boutique Stage Ambience"
          className="w-full h-full object-cover opacity-25 filter blur-sm scale-105"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-[#0F0B1A]/80 via-[#0F0B1A]/95 to-[#0F0B1A]" />
        {/* Ambient tube-amp orange & purple glows */}
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[500px] h-[500px] bg-[#FF6B35]/10 rounded-full blur-[120px]" />
        <div className="absolute bottom-10 right-10 w-[350px] h-[350px] bg-[#7C5CFF]/15 rounded-full blur-[100px]" />
      </div>

      {/* Header: Visual Branding & Cart Quick Access */}
      <header className="relative z-10 w-full px-4 sm:px-8 py-3.5 border-b border-[#7C5CFF]/20 bg-[#1A1330]/75 backdrop-blur-md flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-[#FF6B35] to-[#F7C948] flex items-center justify-center text-white shadow-md shadow-[#FF6B35]/30">
            <Music className="w-4 h-4" />
          </div>
          <div>
            <h1 className="font-['Poppins'] font-bold text-base sm:text-lg tracking-tight text-[#F5F1FF] leading-none">
              Empório da Música
            </h1>
            <span className="text-[11px] text-[#A79FC4]">
              Assistente Musical Ozzy • Som & Boutique
            </span>
          </div>
        </div>

        {/* Python Indicator & Cart Action */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#251B45] border border-[#7C5CFF]/30 text-xs font-mono text-[#F7C948]">
            <Terminal className="w-3.5 h-3.5 text-[#3DDC97]" />
            <span>Python 3.10 Backend</span>
          </div>

          <button
            onClick={() => setIsCartOpen(true)}
            className="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#FF6B35] hover:bg-[#ff7b47] text-white text-xs font-semibold shadow-md shadow-[#FF6B35]/30 transition-all hover:scale-105 active:scale-95"
          >
            <ShoppingBag className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Carrinho</span>
            {totalCartCount > 0 && (
              <span className="px-1.5 py-0.2 bg-[#0F0B1A] text-[#F7C948] rounded-full text-[11px] font-bold">
                {totalCartCount}
              </span>
            )}
          </button>
        </div>
      </header>

      {/* Main Content: Focused Chat Interface */}
      <main className="relative z-10 flex-1 flex flex-col justify-center items-center py-2 sm:py-4">
        <OzzyChat onAddToCart={handleAddToCart} />
      </main>

      {/* Visual Footer */}
      <footer className="relative z-10 py-3 text-center text-[11px] text-[#A79FC4] border-t border-[#7C5CFF]/15 bg-[#0F0B1A]/80 backdrop-blur-sm">
        <span>Empório da Música © 2026 • Inteligência em Python 3.10 • Ozzy Tone Assistant</span>
      </footer>

      {/* Cart Modal */}
      <CartModal
        isOpen={isCartOpen}
        onClose={() => setIsCartOpen(false)}
        cart={cart}
        onUpdateQuantity={handleUpdateQuantity}
        onRemoveItem={handleRemoveItem}
        onClearCart={handleClearCart}
      />
    </div>
  );
}
