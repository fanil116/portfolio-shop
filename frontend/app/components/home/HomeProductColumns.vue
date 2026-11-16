<script setup lang="ts">
    import type { IBlockProduct, IHomeBlock } from '~/repository/modules/content/types';

    import ProductCard from '~/components/product/ProductCard.vue';

    const props = defineProps<{ block: IHomeBlock }>();

    const MAX_PER_COLUMN = 3;

    // Колонки в порядке первого появления названия; товары без колонки — в «Товары»
    const columns = computed(() => {
        const groups = new Map<string, IBlockProduct[]>();
        for (const product of props.block.products) {
            const title = product.group || 'Товары';
            groups.set(title, [...(groups.get(title) ?? []), product]);
        }
        return [...groups].map(([title, products]) => ({
            title,
            products: products.slice(0, MAX_PER_COLUMN),
        }));
    });
</script>

<template>
    <section :class="['container', $style.HomeProductColumns]">
        <div
            v-for="column in columns"
            :key="column.title"
            :class="$style.column"
        >
            <h2 :class="$style.title">{{ column.title }}</h2>
            <ProductCard
                v-for="product in column.products"
                :key="product.id"
                :product="product"
                variant="row"
            />
        </div>
    </section>
</template>

<style lang="scss" module>
    .HomeProductColumns {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
        gap: space(6);
        padding-top: fluid(48px, 72px);
        padding-bottom: fluid(48px, 72px);
    }

    .column {
        display: flex;
        flex-direction: column;
        gap: space(4);
    }

    .title {
        text-transform: uppercase;

        @include typography(body-md, 600);
    }
</style>
