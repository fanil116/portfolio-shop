import type { ICategoryNode } from '~/repository/modules/catalog/types';
import type { IMenu, ISiteSettings } from '~/repository/modules/content/types';

/** Данные шапки и футера: настройки сайта, меню и дерево категорий. */
export const useSiteStore = defineStore('site', () => {
    const { $fetchData } = useNuxtApp();

    const settings = ref<ISiteSettings | null>(null);
    const menus = ref<IMenu[]>([]);
    const categories = ref<ICategoryNode[]>([]);
    const isLoaded = ref(false);

    const menusByPlacement = computed(() => {
        const result: Record<IMenu['placement'], IMenu[]> = {
            header: [],
            footer: [],
            footer_tags: [],
        };
        for (const menu of menus.value) {
            result[menu.placement].push(menu);
        }
        return result;
    });

    async function load(): Promise<void> {
        if (isLoaded.value) {
            return;
        }
        // Запросы независимы — параллельно; падение одного не мешает второму
        const [site, tree] = await Promise.allSettled([
            $fetchData.content.site(),
            $fetchData.catalog.categoryTree(),
        ]);
        if (site.status === 'fulfilled') {
            settings.value = site.value.settings;
            menus.value = site.value.menus;
        } else {
            console.error('[site] не удалось загрузить настройки сайта', site.reason);
        }
        if (tree.status === 'fulfilled') {
            categories.value = tree.value;
        } else {
            console.error('[site] не удалось загрузить категории', tree.reason);
        }
        isLoaded.value = true;
    }

    return { settings, menus, categories, menusByPlacement, isLoaded, load };
});
