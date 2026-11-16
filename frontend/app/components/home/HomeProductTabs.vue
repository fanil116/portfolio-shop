<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import BannerCard from '~/components/home/BannerCard.vue';
    import SectionHeading from '~/components/home/SectionHeading.vue';
    import ProductCard from '~/components/product/ProductCard.vue';

    const props = withDefaults(
        defineProps<{
            block: IHomeBlock;
            /** Баннеры справа от товаров (по умолчанию слева) — блоки на главной чередуются */
            reverse?: boolean;
        }>(),
        { reverse: false }
    );

    const MAX_PRODUCTS = 8;
    const ALL = 0;
    const activeTab = ref<number>(ALL);

    const tabs = computed(() => [
        { id: ALL, name: 'Все товары' },
        ...props.block.categories.map(({ id, name }) => ({ id, name })),
    ]);

    // category_ids содержит и предков: таб «Компьютеры» покажет товары подкатегорий
    const visibleProducts = computed(() =>
        props.block.products
            .filter((p) => activeTab.value === ALL || p.category_ids.includes(activeTab.value))
            .slice(0, MAX_PRODUCTS)
    );
</script>

<template>
    <section
        :class="[
            'container',
            $style.HomeProductTabs,
            { [$style._reverse]: reverse, [$style._withBanners]: block.banners.length },
        ]"
    >
        <div
            v-if="block.banners.length"
            :class="$style.banners"
        >
            <BannerCard
                v-for="banner in block.banners"
                :key="banner.id"
                :banner="banner"
                layout="tall"
            />
        </div>

        <div :class="$style.main">
            <SectionHeading
                :title="block.title"
                :link-text="block.link_text"
                :link-url="block.link_url"
            >
                <template
                    v-if="tabs.length > 1"
                    #end
                >
                    <div
                        :class="$style.tabs"
                        role="tablist"
                        :aria-label="`${block.title}: категории`"
                    >
                        <button
                            v-for="tab in tabs"
                            :key="tab.id"
                            type="button"
                            role="tab"
                            :aria-selected="activeTab === tab.id"
                            :class="[$style.tab, { [$style._active]: activeTab === tab.id }]"
                            @click="activeTab = tab.id"
                        >
                            {{ tab.name }}
                        </button>
                    </div>
                </template>
            </SectionHeading>

            <div
                v-if="visibleProducts.length"
                :class="$style.grid"
                role="tabpanel"
            >
                <ProductCard
                    v-for="product in visibleProducts"
                    :key="product.id"
                    :product="product"
                    show-rating
                />
            </div>
            <p
                v-else
                :class="$style.empty"
            >
                В этой категории пока нет товаров.
            </p>
        </div>
    </section>
</template>

<style lang="scss" module>
    $banner-width: 312px;

    .HomeProductTabs {
        display: grid;

        // minmax(0, …): иначе колонку распирает строка табов и появляется горизонтальный скролл
        grid-template-columns: minmax(0, 1fr);
        gap: space(6);
        padding-top: fluid(48px, 72px);

        @include respond-to(xl) {
            &._withBanners {
                grid-template-columns: $banner-width minmax(0, 1fr);
            }

            &._withBanners._reverse {
                grid-template-columns: minmax(0, 1fr) $banner-width;

                .banners {
                    order: 2;
                }
            }
        }
    }

    .banners {
        display: grid;
        gap: space(6);

        @include respond-below(xl) {
            display: none;
        }
    }

    // На узких экранах табы листаются горизонтально внутри своей строки
    .tabs {
        display: flex;
        gap: space(4);
        overflow-x: auto;
        max-width: 100%;
        scrollbar-width: none;
    }

    .tab {
        @include reset-button;

        padding: space(1) 0;
        border-bottom: 2px solid transparent;
        white-space: nowrap;
        color: color(gray, 600);
        transition:
            color $transition-fast,
            border-color $transition-fast;

        @include typography(body-sm);
        @include focus-ring;

        @include hover {
            color: color(gray, 900);
        }

        &._active {
            font-weight: 600;
            color: color(gray, 900);
            border-bottom-color: color(primary);
        }
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: space(4);

        @include respond-to(md) {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        @include respond-to(lg) {
            grid-template-columns: repeat(4, minmax(0, 1fr));
        }
    }

    .empty {
        padding: space(10) 0;
        text-align: center;
        color: color(gray, 500);
    }
</style>
