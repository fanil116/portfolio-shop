import { useSiteStore } from '~/store/site';

// Шапка и футер нужны на каждой странице — загружаем один раз за SSR-рендер,
// на клиент данные приходят через гидрацию Pinia
export default defineNuxtPlugin(async () => {
    await useSiteStore().load();
});
