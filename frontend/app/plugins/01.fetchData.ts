import type { FetchOptions } from 'ofetch';

import { $fetch } from 'ofetch';

import AuthModule from '~/repository/modules/auth/auth';
import CatalogModule from '~/repository/modules/catalog/catalog';
import ContentModule from '~/repository/modules/content/content';

import { CSRF_COOKIE, readBrowserCookie } from '~/utils/cookies';

export interface IApiInstance {
    auth: AuthModule;
    catalog: CatalogModule;
    content: ContentModule;
}

const UNSAFE_METHODS = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);

// Заголовки входящего запроса, которые SSR пробрасывает в backend
const FORWARDED_HEADERS = [
    'cookie',
    'x-real-ip',
    'x-forwarded-for',
    'x-forwarded-host',
    'x-forwarded-proto',
] as const;

export default defineNuxtPlugin(() => {
    const config = useRuntimeConfig();
    let options: FetchOptions;

    if (import.meta.server) {
        // SSR ходит в backend напрямую и представляется от имени пользователя (его cookie)
        options = {
            baseURL: config.apiInternalUrl,
            headers: useRequestHeaders([...FORWARDED_HEADERS]),
        };
    } else {
        options = {
            baseURL: '/',
            credentials: 'same-origin',
            // Токен читаем при каждом запросе: Django меняет его после входа
            onRequest({ options: requestOptions }) {
                const method = (requestOptions.method ?? 'GET').toUpperCase();
                const token = readBrowserCookie(CSRF_COOKIE);
                if (UNSAFE_METHODS.has(method) && token) {
                    requestOptions.headers.set('X-CSRFToken', token);
                }
            },
        };
    }

    const apiFetcher = $fetch.create(options);

    const modules: IApiInstance = {
        auth: new AuthModule(apiFetcher),
        catalog: new CatalogModule(apiFetcher),
        content: new ContentModule(apiFetcher),
    };

    return {
        provide: {
            fetchData: modules,
        },
    };
});
