import type { $Fetch } from 'ofetch';

type HttpMethod = 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE';

/**
 * Базовый класс модулей репозитория: модуль получает настроенный $fetch
 * (baseURL, заголовки, CSRF) из плагина fetchData.
 */
export default class HttpFactory {
    protected readonly $fetch: $Fetch;

    constructor(fetcher: $Fetch) {
        this.$fetch = fetcher;
    }

    protected call<T>(method: HttpMethod, url: string, body?: object): Promise<T> {
        return this.$fetch<T>(url, { method, body });
    }
}
