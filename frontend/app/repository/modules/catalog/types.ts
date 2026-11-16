export type ProductBadge = '' | 'hot' | 'sale' | 'best_deal' | 'new';

export interface IProductCard {
    id: number;
    name: string;
    slug: string;
    image: string | null;
    brand: string | null;
    price: string;
    old_price: string | null;
    discount_percent: number;
    rating: string;
    reviews_count: number;
    badge: ProductBadge;
    in_stock: boolean;
    /** Категория товара и все её предки — для фильтрации по табам */
    category_ids: number[];
}

export interface ICategory {
    id: number;
    name: string;
    slug: string;
    image: string | null;
    parent_id: number | null;
}

export interface ICategoryNode extends ICategory {
    children: ICategoryNode[];
}

export interface IBrand {
    id: number;
    name: string;
    slug: string;
    logo: string | null;
}
