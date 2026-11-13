import { useAuthStore } from '~/store/auth';

// Страницы входа/регистрации: авторизованного пользователя сразу ведём в кабинет
export default defineNuxtRouteMiddleware(async () => {
    const authStore = useAuthStore();
    await authStore.ensureLoaded();

    if (authStore.isAuthenticated) {
        return navigateTo('/lk');
    }
});
