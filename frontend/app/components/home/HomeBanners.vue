<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import BannerCard from '~/components/home/BannerCard.vue';

    defineProps<{ block: IHomeBlock }>();
</script>

<template>
    <!-- Один баннер — во всю ширину, несколько — в ряд -->
    <section
        :class="['container', $style.HomeBanners, { [$style._row]: block.banners.length > 1 }]"
    >
        <BannerCard
            v-for="banner in block.banners"
            :key="banner.id"
            :banner="banner"
            :layout="block.banners.length > 1 ? 'card' : 'wide'"
        />
    </section>
</template>

<style lang="scss" module>
    .HomeBanners {
        display: grid;
        gap: space(6);
        padding-top: fluid(48px, 72px);
    }

    ._row {
        @include respond-to(lg) {
            grid-template-columns: repeat(auto-fit, minmax(0, 1fr));
        }
    }
</style>
