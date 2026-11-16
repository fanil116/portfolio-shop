<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import VIcon from '~/components/ui/VIcon.vue';

    defineProps<{ block: IHomeBlock }>();
</script>

<template>
    <section class="container">
        <ul :class="$style.HomeFeatures">
            <li
                v-for="feature in block.features"
                :key="feature.id"
                :class="$style.item"
            >
                <VIcon
                    :name="`feature-${feature.icon}`"
                    :size="40"
                    :class="$style.icon"
                />
                <div>
                    <p :class="$style.title">{{ feature.title }}</p>
                    <p :class="$style.text">{{ feature.text }}</p>
                </div>
            </li>
        </ul>
    </section>
</template>

<style lang="scss" module>
    .HomeFeatures {
        display: grid;
        margin-top: space(6);
        padding: space(4);
        border-radius: radius(lg);
        border: 1px solid color(gray, 100);

        @include reset-list;

        // Явная сетка вместо auto-fit: известно, с какой ширины пункты стоят в одну строку
        @include respond-to(sm) {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }

        @include respond-to(lg) {
            grid-auto-flow: column;
            grid-template-columns: none;
            grid-auto-columns: minmax(0, 1fr);
        }
    }

    .item {
        display: flex;
        align-items: center;
        gap: space(4);
        padding: space(4);

        // Разделитель между пунктами — с того же брейкпоинта, где они встают в одну строку
        @include respond-to(lg) {
            & + & {
                border-left: 1px solid color(gray, 100);
            }
        }
    }

    .icon {
        color: color(gray, 900);
    }

    .title {
        color: color(gray, 900);
        text-transform: uppercase;

        @include typography(body-sm, 500);
    }

    .text {
        color: color(gray, 600);

        @include typography(body-sm);
    }
</style>
