import { useSiteStore } from '~/store/site';

// Шапка и футер нужны на каждой странице — загружаем один раз за SSR-рендер,
// на клиент данные приходят через гидрацию Pinia. Выполняется параллельно с плагином auth.
export default defineNuxtPlugin({
    name: 'site',
    parallel: true,
    async setup() {
        await useSiteStore().load();
    },
});
