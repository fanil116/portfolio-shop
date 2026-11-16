<script setup lang="ts">
    export type BadgeTone = 'discount' | 'hot' | 'sale' | 'new' | 'best_deal' | 'sold';

    defineProps<{ tone: BadgeTone }>();
</script>

<template>
    <span :class="[$style.VBadge, $style[`_${tone}`]]">
        <slot />
    </span>
</template>

<style lang="scss" module>
    @use 'sass:list';

    // Тон плашки → (фон, текст)
    $tones: (
        discount: (
            color(warning, 400),
            color(gray, 900),
        ),
        hot: (
            color(danger),
            color(gray, 0),
        ),
        sale: (
            color(success),
            color(gray, 0),
        ),
        new: (
            color(secondary),
            color(gray, 0),
        ),
        best_deal: (
            color(secondary),
            color(gray, 0),
        ),
        sold: (
            color(gray, 400),
            color(gray, 0),
        ),
    );

    .VBadge {
        display: inline-block;
        padding: space(1.25) space(2.5);
        border-radius: radius(xs);
        white-space: nowrap;
        text-transform: uppercase;

        @include typography(body-tiny, 600);

        @each $tone, $colors in $tones {
            &._#{$tone} {
                background-color: list.nth($colors, 1);
                color: list.nth($colors, 2);
            }
        }
    }
</style>
