import type { IBrand, ICategory, IProductCard } from '~/repository/modules/catalog/types';

export type HomeBlockKind =
    | 'hero'
    | 'features'
    | 'deals'
    | 'categories'
    | 'product_tabs'
    | 'banners'
    | 'product_columns'
    | 'newsletter';

export interface IBanner {
    id: number;
    variant: 'card' | 'slide' | 'side';
    eyebrow: string;
    title: string;
    text: string;
    badge_text: string;
    image: string | null;
    background_color: string;
    theme: 'light' | 'dark';
    button_text: string;
    url: string;
}

export interface IFeature {
    id: number;
    icon: 'delivery' | 'return' | 'payment' | 'support';
    title: string;
    text: string;
}

export interface IBlockProduct extends IProductCard {
    /** Название колонки для блока «Колонки товаров» */
    group: string;
}

export interface IHomeBlock {
    id: number;
    kind: HomeBlockKind;
    title: string;
    subtitle: string;
    link_text: string;
    link_url: string;
    ends_at: string | null;
    products: IBlockProduct[];
    categories: ICategory[];
    banners: IBanner[];
    features: IFeature[];
    brands: IBrand[];
}

export interface IHome {
    blocks: IHomeBlock[];
}

export interface IMenuItem {
    id: number;
    title: string;
    url: string;
    icon: string;
}

export interface IMenu {
    id: number;
    title: string;
    placement: 'header' | 'footer' | 'footer_tags';
    items: IMenuItem[];
}

export interface IPromo {
    label: string;
    title: string;
    highlight: string;
    text: string;
    button_text: string;
    url: string;
}

export interface ISiteSettings {
    site_name: string;
    logo: string | null;
    welcome_text: string;
    phone: string;
    email: string;
    address: string;
    copyright_text: string;
    google_play_url: string;
    app_store_url: string;
    promo: IPromo | null;
    socials: { network: string; url: string }[];
}

export interface ISite {
    settings: ISiteSettings;
    menus: IMenu[];
}
