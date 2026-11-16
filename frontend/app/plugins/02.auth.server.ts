import { useAuthStore } from '~/store/auth';

import { SESSION_COOKIE } from '~/utils/cookies';

// Определяем пользователя один раз за SSR-рендер; на клиент состояние приходит через гидрацию Pinia.
// parallel: следующий плагин (данные сайта) не ждёт /me — запросы к backend идут одновременно,
// Nuxt дожидается обоих до рендера. $fetchData к этому моменту уже создан плагином 01.
export default defineNuxtPlugin({
    name: 'auth',
    parallel: true,
    async setup() {
        const authStore = useAuthStore();

        // Без cookie сессии пользователь точно гость — не нагружаем backend запросом /me
        if (!useCookie(SESSION_COOKIE).value) {
            authStore.markGuest();
            return;
        }

        await authStore.ensureLoaded();
    },
});
