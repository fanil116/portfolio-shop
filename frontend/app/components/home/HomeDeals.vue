<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import SectionHeading from '~/components/home/SectionHeading.vue';
    import ProductCard from '~/components/product/ProductCard.vue';

    import { useCountdown } from '~/composables/common/useCountdown';

    const props = defineProps<{ block: IHomeBlock }>();

    // Первая позиция — крупная карточка, остальные — сетка 4×2
    const MAX_GRID = 8;
    const lead = computed(() => props.block.products[0]);
    const rest = computed(() => props.block.products.slice(1, MAX_GRID + 1));

    const { parts } = useCountdown(() => props.block.ends_at);
    const timer = computed(() => {
        const value = parts.value;
        if (!value) {
            return [];
        }
        return [
            `${value.days}д`,
            `${value.hours}ч`,
            `${String(value.minutes).padStart(2, '0')}м`,
            `${String(value.seconds).padStart(2, '0')}с`,
        ];
    });
</script>

<template>
    <section :class="['container', $style.HomeDeals]">
        <SectionHeading
            :title="block.title || 'Лучшие предложения'"
            :link-text="block.link_text"
            :link-url="block.link_url"
        >
            <template
                v-if="block.ends_at"
                #extra
            >
                <span :class="$style.endsIn">
                    До конца акции
                    <time
                        :datetime="block.ends_at"
                        :class="$style.timer"
                    >
                        <template v-if="timer.length">{{ timer.join(' : ') }}</template>
                        <template v-else>…</template>
                    </time>
                </span>
            </template>
        </SectionHeading>

        <div :class="$style.grid">
            <ProductCard
                v-if="lead"
                :product="lead"
                variant="featured"
                :class="$style.lead"
            />
            <ProductCard
                v-for="product in rest"
                :key="product.id"
                :product="product"
            />
        </div>
    </section>
</template>

<style lang="scss" module>
    .HomeDeals {
        padding-top: fluid(48px, 72px);
    }

    .endsIn {
        display: flex;
        align-items: center;
        gap: space(3);

        @include typography(body-sm);
    }

    .timer {
        min-width: 150px;
        padding: space(1.5) space(3);
        border-radius: radius(xs);
        background-color: color(warning, 300);
        font-variant-numeric: tabular-nums;

        @include typography(body-md);
    }

    // Сетка из «склеенных» карточек: соседние рамки не удваиваются за счёт margin −1px
    .grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));

        > * {
            margin: 0 -1px -1px 0;
        }

        @include respond-to(md) {
            grid-template-columns: repeat(3, minmax(0, 1fr));
        }

        @include respond-to(lg) {
            grid-template-columns: 1.32fr repeat(4, minmax(0, 1fr));
            grid-template-rows: repeat(2, auto);
        }
    }

    .lead {
        grid-column: 1 / -1;

        @include respond-to(lg) {
            grid-row: span 2;
            grid-column: auto;
        }
    }
</style>
