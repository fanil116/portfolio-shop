const rubles = new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
    maximumFractionDigits: 0,
});

/** Цена из API (строка Decimal "49990.00") → «49 990 ₽». */
export function formatPrice(value: string | number): string {
    return rubles.format(Number(value));
}
