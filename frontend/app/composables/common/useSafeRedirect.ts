/**
 * Путь из ?next= для возврата после входа. Разрешаем только внутренние пути,
 * чтобы ссылкой вида /login?next=https://evil.example нельзя было увести пользователя.
 */
export function getSafeRedirect(next: unknown, fallback = '/lk'): string {
    if (typeof next !== 'string' || !next.startsWith('/') || next.startsWith('//')) {
        return fallback;
    }
    if (next.includes('\\')) {
        return fallback;
    }
    return next;
}
