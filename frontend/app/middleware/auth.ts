import { useAuthStore } from '~/store/auth';

// Закрывает страницу от гостей: отправляет на вход и возвращает обратно после него
export default defineNuxtRouteMiddleware(async (to) => {
    const authStore = useAuthStore();
    await authStore.ensureLoaded();

    if (!authStore.isAuthenticated) {
        return navigateTo({ path: '/login', query: { next: to.fullPath } });
    }
});
