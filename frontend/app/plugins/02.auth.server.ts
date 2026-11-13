import { useAuthStore } from '~/store/auth';

import { SESSION_COOKIE } from '~/utils/cookies';

// Определяем пользователя один раз за SSR-рендер; на клиент состояние приходит через гидрацию Pinia
export default defineNuxtPlugin(async () => {
    const authStore = useAuthStore();

    // Без cookie сессии пользователь точно гость — не нагружаем backend запросом /me
    if (!useCookie(SESSION_COOKIE).value) {
        authStore.markGuest();
        return;
    }

    await authStore.ensureLoaded();
});
