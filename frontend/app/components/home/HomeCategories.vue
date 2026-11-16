<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import SectionHeading from '~/components/home/SectionHeading.vue';
    import VIcon from '~/components/ui/VIcon.vue';

    defineProps<{ block: IHomeBlock }>();

    const scroller = ref<HTMLElement | null>(null);

    // Прокрутка ленты на ширину видимой области; snap докрутит до ближайшей карточки
    function scrollBy(direction: 1 | -1): void {
        scroller.value?.scrollBy({
            left: direction * scroller.value.clientWidth,
            behavior: 'smooth',
        });
    }
</script>

<template>
    <section :class="['container', $style.HomeCategories]">
        <SectionHeading
            :title="block.title || 'Категории'"
            size="lg"
        />
        <div :class="$style.wrapper">
            <button
                type="button"
                :class="[$style.arrow, $style._prev]"
                aria-label="Предыдущие категории"
                @click="scrollBy(-1)"
            >
                <VIcon name="arrow-left" />
            </button>
            <ul
                ref="scroller"
                :class="$style.list"
            >
                <li
                    v-for="category in block.categories"
                    :key="category.id"
                >
                    <NuxtLink
                        :to="`/catalog/${category.slug}`"
                        :class="$style.card"
                    >
                        <img
                            v-if="category.image"
                            :src="category.image"
                            alt=""
                            :class="$style.image"
                            loading="lazy"
                        />
                        <span :class="$style.name">{{ category.name }}</span>
                    </NuxtLink>
                </li>
            </ul>
            <button
                type="button"
                :class="[$style.arrow, $style._next]"
                aria-label="Следующие категории"
                @click="scrollBy(1)"
            >
                <VIcon name="arrow-right" />
            </button>
        </div>
    </section>
</template>

<style lang="scss" module>
    .HomeCategories {
        padding-top: fluid(48px, 72px);
    }

    .wrapper {
        position: relative;
    }

    .list {
        // Шесть карточек в ряд на десктопе, на узких экранах — сколько поместится
        --snap-item-width: calc((100% - #{space(4.5)} * 5) / 6);

        @include reset-list;
        @include snap-scroller(space(4.5));

        @include respond-below(lg) {
            --snap-item-width: 180px;
        }
    }

    .card {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: space(4);
        height: 100%;
        padding: space(6) space(3);
        border-radius: radius(md);
        border: 1px solid color(gray, 100);
        transition:
            border-color $transition-fast,
            box-shadow $transition-base;

        @include focus-ring;

        @include hover {
            border-color: color(primary);
            box-shadow: $shadow-card-hover;
        }
    }

    .image {
        width: 100%;
        max-width: 148px;
        aspect-ratio: 1;
        object-fit: contain;
    }

    .name {
        text-align: center;
        color: color(gray, 900);

        @include typography(body-md, 500);
    }

    .arrow {
        @include reset-button;

        position: absolute;
        top: 50%;
        z-index: z(overlay);
        display: none;
        padding: space(3);
        border-radius: radius(round);
        background-color: color(primary);
        color: color(gray, 0);
        transform: translateY(-50%);
        transition: background-color $transition-fast;

        @include focus-ring;

        @include hover {
            background-color: color(primary, 600);
        }

        @include respond-to(lg) {
            display: flex;
        }

        &._prev {
            left: space(-6);
        }

        &._next {
            right: space(-6);
        }
    }
</style>
