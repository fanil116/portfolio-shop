/** Cookie сессии Django (SESSION_COOKIE_NAME) и CSRF-токена (CSRF_COOKIE_NAME). */
export const SESSION_COOKIE = 'sessionid';
export const CSRF_COOKIE = 'csrftoken';

/**
 * Читает cookie напрямую из document.cookie — всегда актуальное значение,
 * в отличие от закэшированного useCookie (Django меняет csrftoken после входа).
 * Только для клиента.
 */
export function readBrowserCookie(name: string): string | undefined {
    const match = document.cookie.match(new RegExp(`(?:^|; )${name}=([^;]*)`));
    return match?.[1] ? decodeURIComponent(match[1]) : undefined;
}
