import { useAuthStore } from '~/store/auth';

// Определяем пользователя один раз за SSR-рендер; на клиент состояние приходит через гидрацию Pinia
export default defineNuxtPlugin(async () => {
    await useAuthStore().ensureLoaded();
});
