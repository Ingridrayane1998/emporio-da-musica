import React, { useState } from 'react';
import { CartItem } from '../types';
import { X, Trash2, ShoppingBag, ArrowRight, CheckCircle2, Tag } from 'lucide-react';

interface CartModalProps {
  isOpen: boolean;
  onClose: () => void;
  cart: CartItem[];
  onUpdateQuantity: (id: string, delta: number) => void;
  onRemoveItem: (id: string) => void;
  onClearCart: () => void;
}

export const CartModal: React.FC<CartModalProps> = ({
  isOpen,
  onClose,
  cart,
  onUpdateQuantity,
  onRemoveItem,
  onClearCart,
}) => {
  const [coupon, setCoupon] = useState('OZZY10');
  const [appliedDiscount, setAppliedDiscount] = useState(0.1);
  const [couponSuccess, setCouponSuccess] = useState(true);
  const [isCompleted, setIsCompleted] = useState(false);

  if (!isOpen) return null;

  const subtotal = cart.reduce((sum, item) => sum + item.product.price * item.quantity, 0);
  const discountVal = subtotal * appliedDiscount;
  const total = subtotal - discountVal;
  const installments = total > 0 ? (total / 12).toFixed(2) : '0,00';

  const applyCoupon = () => {
    if (coupon.trim().toUpperCase() === 'OZZY10') {
      setAppliedDiscount(0.1);
      setCouponSuccess(true);
    } else {
      setAppliedDiscount(0);
      setCouponSuccess(false);
    }
  };

  const handleCheckout = () => {
    setIsCompleted(true);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-[#1A1330] border border-[#7C5CFF]/30 w-full max-w-lg rounded-2xl p-6 shadow-2xl flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-[#7C5CFF]/20">
          <div className="flex items-center gap-2">
            <ShoppingBag className="w-5 h-5 text-[#FF6B35]" />
            <h3 className="font-['Poppins'] font-semibold text-base text-[#F5F1FF]">
              Seu Carrinho • Empório da Música
            </h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded-lg text-[#A79FC4] hover:text-white hover:bg-[#251B45]"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        {isCompleted ? (
          <div className="py-12 text-center flex flex-col items-center">
            <CheckCircle2 className="w-16 h-16 text-[#3DDC97] mb-4 animate-bounce" />
            <h4 className="font-['Poppins'] text-xl font-bold text-white mb-2">
              Pedido Confirmado com Sucesso!
            </h4>
            <p className="text-xs text-[#A79FC4] max-w-sm mb-6">
              Nosso luthier já foi notificado para realizar a inspeção e regulagem completa do instrumento antes do envio expresso com seguro total.
            </p>
            <button
              onClick={() => {
                onClearCart();
                setIsCompleted(false);
                onClose();
              }}
              className="px-6 py-2.5 rounded-full bg-[#FF6B35] text-white text-xs font-semibold hover:bg-[#ff7b47]"
            >
              Concluir & Voltar ao Ozzy
            </button>
          </div>
        ) : cart.length === 0 ? (
          <div className="py-16 text-center text-[#A79FC4]">
            <p className="text-sm mb-2">Seu carrinho está vazio.</p>
            <p className="text-xs">Peça uma recomendação ao Ozzy no chat para começar!</p>
          </div>
        ) : (
          <>
            <div className="flex-1 overflow-y-auto py-4 space-y-3 pr-1">
              {cart.map(({ product, quantity }) => (
                <div
                  key={product.id}
                  className="flex items-center gap-3 p-3 bg-[#251B45] rounded-xl border border-[#7C5CFF]/15"
                >
                  <img
                    src={product.image}
                    alt={product.name}
                    className="w-14 h-14 rounded-lg object-cover bg-[#0F0B1A]"
                  />
                  <div className="flex-1 min-w-0">
                    <h5 className="font-semibold text-xs text-[#F5F1FF] truncate">
                      {product.name}
                    </h5>
                    <p className="text-xs text-[#FF6B35] font-bold font-mono">
                      R$ {product.price.toLocaleString('pt-BR')}
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => onUpdateQuantity(product.id, -1)}
                      className="w-6 h-6 rounded bg-[#1A1330] text-[#A79FC4] hover:text-white flex items-center justify-center text-xs"
                    >
                      -
                    </button>
                    <span className="text-xs font-semibold text-white px-1">
                      {quantity}
                    </span>
                    <button
                      onClick={() => onUpdateQuantity(product.id, 1)}
                      className="w-6 h-6 rounded bg-[#1A1330] text-[#A79FC4] hover:text-white flex items-center justify-center text-xs"
                    >
                      +
                    </button>
                    <button
                      onClick={() => onRemoveItem(product.id)}
                      className="p-1 text-[#A79FC4] hover:text-[#FF4D6D] ml-1"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Coupon */}
            <div className="pt-3 pb-2 border-t border-[#7C5CFF]/15 flex items-center gap-2">
              <div className="flex-1 flex items-center bg-[#251B45] px-3 py-1.5 rounded-lg border border-[#7C5CFF]/20">
                <Tag className="w-3.5 h-3.5 text-[#F7C948] mr-2" />
                <input
                  type="text"
                  value={coupon}
                  onChange={(e) => setCoupon(e.target.value)}
                  placeholder="Cupom de Desconto"
                  className="bg-transparent text-xs text-white uppercase focus:outline-none w-full"
                />
              </div>
              <button
                onClick={applyCoupon}
                className="px-3 py-1.5 bg-[#7C5CFF] hover:bg-[#6b4ae8] text-white text-xs font-medium rounded-lg"
              >
                Aplicar
              </button>
            </div>
            {couponSuccess && (
              <p className="text-[11px] text-[#3DDC97] mb-3">
                ✓ Cupom OZZY10 aplicado: 10% de desconto adicional!
              </p>
            )}

            {/* Totals & Checkout */}
            <div className="pt-3 border-t border-[#7C5CFF]/20 space-y-1.5">
              <div className="flex justify-between text-xs text-[#A79FC4]">
                <span>Subtotal:</span>
                <span>R$ {subtotal.toLocaleString('pt-BR')}</span>
              </div>
              {appliedDiscount > 0 && (
                <div className="flex justify-between text-xs text-[#3DDC97]">
                  <span>Desconto Cupom:</span>
                  <span>- R$ {discountVal.toLocaleString('pt-BR')}</span>
                </div>
              )}
              <div className="flex justify-between text-sm font-bold text-white pt-1">
                <span>Total:</span>
                <span className="text-[#FF6B35] font-['Poppins'] text-base">
                  R$ {total.toLocaleString('pt-BR')}
                </span>
              </div>
              <p className="text-[11px] text-[#A79FC4] text-right">
                ou até 12x de R$ {installments} sem juros
              </p>

              <button
                onClick={handleCheckout}
                className="w-full mt-3 py-3 rounded-full bg-[#FF6B35] hover:bg-[#ff7b47] text-white font-semibold text-xs flex items-center justify-center gap-2 shadow-lg shadow-[#FF6B35]/25 transition-all"
              >
                <span>Finalizar Pedido</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
