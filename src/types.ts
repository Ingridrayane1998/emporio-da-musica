export interface Product {
  id: string;
  name: string;
  brand: string;
  category: 'guitars' | 'acoustics' | 'amps' | 'pedals' | 'studio';
  price: number;
  originalPrice: number;
  discountPercent?: number;
  image: string;
  rating: number;
  reviewsCount: number;
  tags: string[];
  specs: { [key: string]: string };
  audioToneType: 'rock' | 'acoustic' | 'blues' | 'jazz' | 'sparkle';
  description: string;
  inStock: boolean;
  isOzzyPick?: boolean;
}

export interface ChatMessage {
  id: string;
  sender: 'ozzy' | 'user';
  text: string;
  timestamp: string;
  productCard?: Product;
  handoffCard?: {
    specialistName: string;
    specialistRole: string;
    reason: string;
    whatsappNumber: string;
  };
  chips?: string[];
}

export interface CartItem {
  product: Product;
  quantity: number;
}

export type ActiveTab = 'chat' | 'catalog' | 'tone-builder' | 'luthieria' | 'python-hub';
