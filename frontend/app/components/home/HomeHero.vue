<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import BannerCard from '~/components/home/BannerCard.vue';

    const props = defineProps<{ block: IHomeBlock }>();

    const AUTOPLAY_MS = 6000;

    const slides = computed(() => props.block.banners.filter((b) => b.variant !== 'side'));
    const sides = computed(() => props.block.banners.filter((b) => b.variant === 'side'));

    const active = ref(0);
    // Мышь и клавиатурный фокус ставят паузу независимо: уход мыши не снимает паузу,
    // пока фокус внутри слайдера, иначе слайд с фокусом уехал бы и стал inert
    const isHovered = ref(false);
    const hasFocus = ref(false);
    const isPaused = computed(() => isHovered.value || hasFocus.value);
    let timer: ReturnType<typeof setInterval> | undefined;

    // Переход фокуса между элементами внутри слайдера паузу не снимает
    function onFocusOut(event: FocusEvent): void {
        const slider = event.currentTarget as HTMLElement;
        hasFocus.value = slider.contains(event.relatedTarget as Node | null);
    }

    function goTo(index: number): void {
        active.value = (index + slides.value.length) % slides.value.length;
    }

    // Автопрокрутка только если слайдов больше одного и пользователь не просил меньше анимаций
    onMounted(() => {
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (slides.value.length > 1 && !reduceMotion) {
            timer = setInterval(() => {
                if (!isPaused.value) {
                    goTo(active.value + 1);
                }
            }, AUTOPLAY_MS);
        }
    });
    onBeforeUnmount(() => clearInterval(timer));
</script>

<template>
    <section :class="['container', $style.HomeHero, { [$style._single]: !sides.length }]">
        <div
            v-if="slides.length"
            :class="$style.slider"
            aria-roledescription="carousel"
            @mouseenter="isHovered = true"
            @mouseleave="isHovered = false"
            @focusin="hasFocus = true"
            @focusout="onFocusOut"
        >
            <div
                :class="$style.track"
                :style="{ '--active': active }"
            >
                <div
                    v-for="(slide, index) in slides"
                    :key="slide.id"
                    :class="$style.slide"
                    :aria-hidden="index !== active"
                    :inert="index !== active"
                >
                    <BannerCard
                        :banner="slide"
                        layout="hero"
                    />
                </div>
            </div>
            <div
                v-if="slides.length > 1"
                :class="$style.dots"
            >
                <button
                    v-for="(slide, index) in slides"
                    :key="slide.id"
                    type="button"
                    :class="[$style.dot, { [$style._active]: index === active }]"
                    :aria-label="`Слайд ${index + 1}: ${slide.title}`"
                    :aria-current="index === active"
                    @click="goTo(index)"
                />
            </div>
        </div>

        <div
            v-if="sides.length"
            :class="$style.sides"
        >
            <BannerCard
                v-for="banner in sides"
                :key="banner.id"
                :banner="banner"
                layout="side"
            />
        </div>
    </section>
</template>

<style lang="scss" module>
    .HomeHero {
        display: grid;
        gap: space(6);
        padding-top: space(6);

        @include respond-to(lg) {
            grid-template-columns: 2fr 1fr;
        }

        &._single {
            grid-template-columns: 1fr;
        }
    }

    .slider {
        position: relative;
        overflow: hidden;
        border-radius: radius(lg);
    }

    // Лента слайдов сдвигается на --active ширин
    .track {
        display: flex;
        height: 100%;
        transform: translateX(calc(var(--active) * -100%));
        transition: transform 0.5s ease;

        @media (prefers-reduced-motion: reduce) {
            transition: none;
        }
    }

    .slide {
        flex: 0 0 100%;
    }

    .dots {
        position: absolute;
        bottom: space(10);
        left: fluid(32px, 56px);
        display: flex;
        gap: space(2);
    }

    .dot {
        @include reset-button;

        width: 10px;
        height: 10px;
        border-radius: radius(round);
        background-color: color(gray, 300);
        transition:
            background-color $transition-fast,
            width $transition-fast;

        @include focus-ring;

        &._active {
            width: 24px;
            background-color: color(gray, 900);
        }
    }

    .sides {
        display: grid;
        gap: space(6);

        @include respond-to(md) {
            grid-template-columns: 1fr 1fr;
        }

        @include respond-to(lg) {
            grid-template-columns: 1fr;
        }
    }
</style>
