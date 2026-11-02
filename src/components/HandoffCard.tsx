import React from 'react';
import { MessageCircle, ShieldCheck, UserCheck, ArrowRight } from 'lucide-react';

interface HandoffCardProps {
  specialistName: string;
  specialistRole: string;
  reason: string;
  whatsappNumber: string;
}

export const HandoffCard: React.FC<HandoffCardProps> = ({
  specialistName,
  specialistRole,
  reason,
  whatsappNumber,
}) => {
  const handleOpenWhatsApp = () => {
    const text = encodeURIComponent(
      `Olá ${specialistName}! Estava conversando com o Ozzy no Empório da Música sobre: ${reason}. Gostaria de falar com você.`
    );
    window.open(`https://wa.me/${whatsappNumber}?text=${text}`, '_blank');
  };

  return (
    <div className="relative p-0.5 rounded-2xl bg-gradient-to-r from-[#FF6B35] via-[#7C5CFF] to-[#F7C948] my-3 shadow-xl shadow-[#7C5CFF]/15 max-w-md w-full">
      <div className="bg-[#1A1330] rounded-[15px] p-4 sm:p-5">
        <div className="flex items-center gap-2.5 mb-2.5">
          <div className="w-8 h-8 rounded-full bg-[#7C5CFF]/20 border border-[#7C5CFF]/40 flex items-center justify-center text-[#F7C948]">
            <UserCheck className="w-4 h-4" />
          </div>
          <div>
            <span className="text-[11px] font-semibold tracking-wider uppercase text-[#F7C948]">
              Atendimento Especialista
            </span>
            <h4 className="font-['Poppins'] font-semibold text-sm text-[#F5F1FF]">
              {specialistName}
            </h4>
          </div>
        </div>

        <p className="text-xs text-[#A79FC4] mb-3">
          {specialistRole}
        </p>

        <div className="bg-[#251B45]/70 rounded-xl p-3 border border-[#7C5CFF]/15 mb-3.5">
          <span className="text-[11px] text-[#A79FC4] block">Motivo da Conexão:</span>
          <span className="text-xs font-medium text-[#F5F1FF]">{reason}</span>
        </div>

        <button
          onClick={handleOpenWhatsApp}
          className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-full bg-[#3DDC97] hover:bg-[#34c486] text-[#0F0B1A] font-semibold text-xs transition-all shadow-md hover:scale-[1.01]"
        >
          <MessageCircle className="w-4 h-4 fill-current" />
          <span>Falar no WhatsApp com o Especialista</span>
          <ArrowRight className="w-3.5 h-3.5 ml-auto" />
        </button>
      </div>
    </div>
  );
};
