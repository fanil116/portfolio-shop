<script setup lang="ts">
    import type { HomeBlockKind, IHomeBlock } from '~/repository/modules/content/types';
    import type { Component } from 'vue';

    import HomeBanners from '~/components/home/HomeBanners.vue';
    import HomeCategories from '~/components/home/HomeCategories.vue';
    import HomeDeals from '~/components/home/HomeDeals.vue';
    import HomeFeatures from '~/components/home/HomeFeatures.vue';
    import HomeHero from '~/components/home/HomeHero.vue';
    import HomeNewsletter from '~/components/home/HomeNewsletter.vue';
    import HomeProductColumns from '~/components/home/HomeProductColumns.vue';
    import HomeProductTabs from '~/components/home/HomeProductTabs.vue';

    // Тип блока из админки → компонент секции
    const BLOCKS: Record<HomeBlockKind, Component> = {
        hero: HomeHero,
        features: HomeFeatures,
        deals: HomeDeals,
        categories: HomeCategories,
        product_tabs: HomeProductTabs,
        banners: HomeBanners,
        product_columns: HomeProductColumns,
        newsletter: HomeNewsletter,
    };

    const { $fetchData } = useNuxtApp();
    const { data, error } = await useAsyncData('home', () => $fetchData.content.home());

    if (error.value) {
        console.error('[home] не удалось загрузить главную', error.value);
    }

    // Неизвестный тип (новый блок на бэке раньше фронта) пропускаем, а не ломаем страницу
    const blocks = computed(() =>
        (data.value?.blocks ?? []).filter((block): block is IHomeBlock => block.kind in BLOCKS)
    );

    // Блоки «Товары с табами» чередуют сторону баннеров, как в макете
    const reversedIds = computed(() => {
        const tabs = blocks.value.filter((block) => block.kind === 'product_tabs');
        return new Set(tabs.filter((_, index) => index % 2 === 1).map((block) => block.id));
    });

    useHead({ title: 'Магазин электроники' });
</script>

<template>
    <div :class="$style.HomePage">
        <h1 :class="$style.hidden">Магазин электроники</h1>
        <component
            :is="BLOCKS[block.kind]"
            v-for="block in blocks"
            :key="block.id"
            :block="block"
            :reverse="reversedIds.has(block.id) || undefined"
        />
        <p
            v-if="error"
            :class="['container', $style.error]"
        >
            Не удалось загрузить витрину. Обновите страницу чуть позже.
        </p>
    </div>
</template>

<style lang="scss" module>
    .hidden {
        @include visually-hidden;
    }

    .error {
        padding: space(20) 0;
        text-align: center;
        color: color(gray, 600);
    }
</style>
