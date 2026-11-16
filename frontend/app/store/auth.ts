import type {
    ILoginPayload,
    IProfilePayload,
    IRegisterPayload,
    IUser,
} from '~/repository/modules/auth/types';

import { FetchError } from 'ofetch';

import { CSRF_COOKIE, readBrowserCookie } from '~/utils/cookies';

const UNAUTHORIZED_STATUSES = new Set([401, 403]);

function isUnauthorized(error: unknown): boolean {
    return error instanceof FetchError && UNAUTHORIZED_STATUSES.has(error.status ?? 0);
}

export const useAuthStore = defineStore('auth', () => {
    const { $fetchData } = useNuxtApp();

    const user = ref<IUser | null>(null);
    // Запрашивали ли текущего пользователя в рамках этого рендера/сессии
    const isLoaded = ref(false);

    const isAuthenticated = computed(() => user.value !== null);

    async function fetchMe(): Promise<void> {
        try {
            user.value = await $fetchData.auth.me();
        } catch (error) {
            user.value = null;
            // 401/403 — обычный гость; остальное (backend недоступен и т.п.) логируем,
            // но страницу не роняем: пользователь увидит сайт как гость
            if (!isUnauthorized(error)) {
                console.error('[auth] не удалось получить пользователя', error);
            }
        } finally {
            isLoaded.value = true;
        }
    }

    async function ensureLoaded(): Promise<void> {
        if (!isLoaded.value) {
            await fetchMe();
        }
    }

    /** Гость без cookie сессии: запрашивать backend незачем. */
    function markGuest(): void {
        user.value = null;
        isLoaded.value = true;
    }

    /** Запрашивает cookie csrftoken, только если её ещё нет. */
    async function ensureCsrf(): Promise<void> {
        if (!readBrowserCookie(CSRF_COOKIE)) {
            await $fetchData.auth.csrf();
        }
    }

    async function login(payload: ILoginPayload): Promise<void> {
        await ensureCsrf();
        user.value = await $fetchData.auth.login(payload);
    }

    async function register(payload: IRegisterPayload): Promise<void> {
        await ensureCsrf();
        user.value = await $fetchData.auth.register(payload);
    }

    async function updateProfile(payload: IProfilePayload): Promise<void> {
        await ensureCsrf();
        user.value = await $fetchData.auth.updateProfile(payload);
    }

    async function logout(): Promise<void> {
        try {
            await ensureCsrf();
            await $fetchData.auth.logout();
        } catch (error) {
            // 401/403 — сессия на сервере уже истекла: пользователь фактически вышел
            if (!isUnauthorized(error)) {
                throw error;
            }
        }
        user.value = null;
    }

    return {
        user,
        isLoaded,
        isAuthenticated,
        fetchMe,
        ensureLoaded,
        markGuest,
        ensureCsrf,
        login,
        register,
        updateProfile,
        logout,
    };
});
