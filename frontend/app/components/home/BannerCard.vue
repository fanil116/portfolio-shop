<script setup lang="ts">
    import type { IBanner } from '~/repository/modules/content/types';

    import VButton from '~/components/ui/VButton.vue';

    withDefaults(
        defineProps<{
            banner: IBanner;
            /** hero — главный слайд, side — малый в колонке, card — в ряду, wide — во всю ширину */
            layout?: 'hero' | 'side' | 'card' | 'wide' | 'tall';
        }>(),
        { layout: 'card' }
    );
</script>

<template>
    <article
        :class="[$style.BannerCard, $style[`_${layout}`], $style[`_${banner.theme}`]]"
        :style="{ '--banner-bg': banner.background_color }"
    >
        <div :class="$style.content">
            <p
                v-if="banner.eyebrow"
                :class="$style.eyebrow"
            >
                {{ banner.eyebrow }}
            </p>
            <h3 :class="$style.title">{{ banner.title }}</h3>
            <p
                v-if="banner.text"
                :class="$style.text"
            >
                {{ banner.text }}
            </p>
            <VButton
                v-if="banner.button_text && banner.url"
                :to="banner.url"
                icon="arrow-right"
                :size="layout === 'hero' ? 'lg' : 'md'"
            >
                {{ banner.button_text }}
            </VButton>
        </div>
        <img
            v-if="banner.image"
            :src="banner.image"
            alt=""
            :class="$style.image"
            :loading="layout === 'hero' ? 'eager' : 'lazy'"
        />
        <span
            v-if="banner.badge_text"
            :class="$style.badge"
        >
            {{ banner.badge_text }}
        </span>
    </article>
</template>

<style lang="scss" module>
    .BannerCard {
        position: relative;
        overflow: hidden;
        display: flex;
        align-items: center;
        gap: space(5);
        height: 100%;
        padding: fluid(24px, 40px);
        border-radius: radius(lg);
        background-color: var(--banner-bg);
        color: color(gray, 900);
    }

    ._dark {
        color: color(gray, 0);

        .eyebrow {
            color: color(warning);
        }

        .text {
            color: color(gray, 300);
        }
    }

    .content {
        position: relative;
        z-index: z(base);
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: space(3);
        flex: 1 1 50%;
    }

    .eyebrow {
        color: color(secondary, 600);
        text-transform: uppercase;

        @include typography(body-sm, 600);
    }

    .title {
        @include typography(heading-03);
    }

    .text {
        max-width: 356px;
        color: color(gray, 700);

        @include typography(body-md);
    }

    .image {
        flex: 0 1 45%;
        min-width: 0;
        max-height: 100%;
        object-fit: contain;
    }

    .badge {
        position: absolute;
        top: space(6);
        right: space(6);
        padding: space(2) space(4);
        border-radius: radius(xs);
        background-color: color(warning, 400);
        color: color(gray, 900);

        @include typography(body-md, 600);
    }

    // Главный слайд: крупный заголовок, цена в круге
    ._hero {
        min-height: 400px;
        padding: fluid(32px, 56px);

        .title {
            font-size: fluid(32px, 48px);
            line-height: 1.17;
        }

        .eyebrow:before {
            content: '';
            display: inline-block;
            width: space(6);
            height: 2px;
            margin-right: space(2);
            background-color: currentcolor;
            vertical-align: middle;
        }

        // Круг, который растягивается в «пилюлю», если цена длиннее диаметра
        .badge {
            display: grid;
            place-items: center;
            min-width: fluid(80px, 100px);
            height: fluid(80px, 100px);
            padding: 0 space(5);
            border-radius: radius(round);
            white-space: nowrap;
            border: 4px solid color(gray, 0);
            background-color: color(secondary);
            color: color(gray, 0);

            @include typography(body-xl, 600);
        }

        @include respond-below(md) {
            flex-direction: column-reverse;
            align-items: stretch;

            .image {
                max-height: 220px;
            }
        }
    }

    ._side {
        padding: space(8);
    }

    // Вертикальный баннер в колонке рядом с товарами
    ._tall {
        flex-direction: column;
        justify-content: space-between;
        text-align: center;

        .content {
            align-items: center;
            flex: none;
        }
    }

    ._wide {
        min-height: 336px;

        .title {
            font-size: fluid(32px, 48px);
            line-height: 1.17;
        }

        @include respond-below(md) {
            flex-direction: column;
            align-items: flex-start;
        }
    }
</style>
