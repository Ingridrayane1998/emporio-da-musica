import React from 'react';
import { Product } from '../types';
import { Play, ShoppingCart, Check, Music2, Star } from 'lucide-react';
import { soundSynth } from '../services/audioSynthesizer';

interface ProductCardProps {
  product: Product;
  onAddToCart: (product: Product) => void;
  onConsultOzzy?: (product: Product) => void;
  isCompact?: boolean;
}

export const ProductCard: React.FC<ProductCardProps> = ({
  product,
  onAddToCart,
  onConsultOzzy,
  isCompact = false,
}) => {
  const [isPlaying, setIsPlaying] = React.useState(false);
  const [added, setAdded] = React.useState(false);

  const handlePlaySound = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsPlaying(true);
    soundSynth.playTone(product.audioToneType, 2.2);
    setTimeout(() => setIsPlaying(false), 2200);
  };

  const handleAdd = (e: React.MouseEvent) => {
    e.stopPropagation();
    onAddToCart(product);
    setAdded(true);
    setTimeout(() => setAdded(false), 1800);
  };

  return (
    <div
      className={`group relative rounded-2xl bg-[#251B45]/90 border border-[#7C5CFF]/20 hover:border-[#FF6B35]/50 transition-all duration-300 overflow-hidden flex flex-col ${
        isCompact ? 'max-w-md w-full my-2 shadow-lg' : 'h-full hover:shadow-2xl hover:shadow-[#FF6B35]/15'
      }`}
    >
      {/* Media Thumbnail Container */}
      <div className="relative aspect-square w-full bg-[#1A1330] overflow-hidden">
        <img
          src={product.image}
          alt={product.name}
          referrerPolicy="no-referrer"
          className="w-full h-full object-cover object-center group-hover:scale-105 transition-transform duration-500"
        />

        {/* Promo Discount Badge */}
        {product.discountPercent && (
          <div className="absolute top-3 left-3 bg-[#F7C948] text-[#0F0B1A] font-bold text-xs px-2.5 py-1 rounded-md shadow-md tracking-wider">
            -{product.discountPercent}% OFF
          </div>
        )}

        {/* Audio Demo Trigger Overlay */}
        <button
          onClick={handlePlaySound}
          title="Ouvir demonstração de timbre"
          className={`absolute bottom-3 right-3 flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold backdrop-blur-md transition-all shadow-md ${
            isPlaying
              ? 'bg-[#FF6B35] text-white ring-2 ring-[#FF6B35]/50 scale-105'
              : 'bg-[#1A1330]/85 text-[#F5F1FF] hover:bg-[#FF6B35] hover:text-white'
          }`}
        >
          {isPlaying ? (
            <>
              <div className="flex items-center gap-0.5 h-3">
                <span className="w-1 bg-white h-3 animate-eq-1 rounded-full"></span>
                <span className="w-1 bg-white h-2 animate-eq-2 rounded-full"></span>
                <span className="w-1 bg-white h-3 animate-eq-3 rounded-full"></span>
              </div>
              <span>Tocando...</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Ouvir Timbre</span>
            </>
          )}
        </button>
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col justify-between">
        <div>
          {/* Metadata Brand and Category */}
          <div className="flex items-center justify-between text-xs text-[#A79FC4] mb-1">
            <span>{product.brand}</span>
            <div className="flex items-center gap-1 text-[#F7C948]">
              <Star className="w-3 h-3 fill-current" />
              <span className="tabular-nums font-semibold">{product.rating.toFixed(1)}</span>
              <span className="text-[#A79FC4]">({product.reviewsCount})</span>
            </div>
          </div>

          {/* Product Name */}
          <h4 className="font-['Poppins'] font-semibold text-sm sm:text-base text-[#F5F1FF] line-clamp-2 leading-snug mb-2 group-hover:text-[#FF6B35] transition-colors">
            {product.name}
          </h4>

          {/* Specs / Tags */}
          <p className="text-xs text-[#A79FC4] line-clamp-2 mb-3 leading-relaxed">
            {product.description}
          </p>
        </div>

        {/* Pricing & CTA */}
        <div className="pt-3 border-t border-[#7C5CFF]/15">
          <div className="flex items-baseline gap-2 mb-3">
            <span className="text-lg sm:text-xl font-bold text-[#FF6B35] font-['Poppins'] tabular-nums">
              R$ {product.price.toLocaleString('pt-BR')}
            </span>
            {product.originalPrice > product.price && (
              <span className="text-xs text-[#A79FC4] line-through tabular-nums">
                R$ {product.originalPrice.toLocaleString('pt-BR')}
              </span>
            )}
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={handleAdd}
              className={`flex-1 flex items-center justify-center gap-1.5 py-2 px-3 rounded-full text-xs font-semibold transition-all ${
                added
                  ? 'bg-[#3DDC97] text-[#0F0B1A]'
                  : 'bg-[#FF6B35] hover:bg-[#ff7b47] text-white shadow-md shadow-[#FF6B35]/20 hover:scale-[1.02]'
              }`}
            >
              {added ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>No Carrinho</span>
                </>
              ) : (
                <>
                  <ShoppingCart className="w-3.5 h-3.5" />
                  <span>Adicionar</span>
                </>
              )}
            </button>

            {onConsultOzzy && (
              <button
                onClick={() => onConsultOzzy(product)}
                title="Tirar dúvidas com o Ozzy"
                className="py-2 px-3 rounded-full bg-[#1A1330] hover:bg-[#32245e] text-[#A79FC4] hover:text-[#F5F1FF] text-xs font-medium border border-[#7C5CFF]/30 transition-colors whitespace-nowrap"
              >
                Tirar Dúvida
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
