<script setup lang="ts">
    import VIcon from '~/components/ui/VIcon.vue';

    type Variant = 'primary' | 'warning' | 'light' | 'link';

    const props = withDefaults(
        defineProps<{
            to?: string;
            variant?: Variant;
            size?: 'md' | 'lg';
            icon?: string;
            type?: 'button' | 'submit';
            disabled?: boolean;
        }>(),
        { to: undefined, variant: 'primary', size: 'md', icon: undefined, type: 'button' }
    );

    const tag = computed(() => (props.to ? resolveComponent('NuxtLink') : 'button'));
</script>

<template>
    <component
        :is="tag"
        :to="to"
        :type="to ? undefined : type"
        :disabled="to ? undefined : disabled"
        :class="[$style.VButton, $style[`_${variant}`], $style[`_${size}`]]"
    >
        <slot />
        <VIcon
            v-if="icon"
            :name="icon"
            :size="size === 'lg' ? 24 : 20"
        />
    </component>
</template>

<style lang="scss" module>
    @use 'sass:list';

    // Цвета вариантов: фон, текст, фон при наведении
    $variants: (
        primary: (
            color(primary),
            color(gray, 0),
            color(primary, 600),
        ),
        warning: (
            color(warning),
            color(gray, 900),
            color(warning, 400),
        ),
        light: (
            color(gray, 0),
            color(primary),
            color(primary, 50),
        ),
    );

    .VButton {
        @include reset-button;

        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: space(2);
        border-radius: radius(xs);
        white-space: nowrap;
        transition:
            background-color $transition-fast,
            color $transition-fast;

        @include typography(caption);
        @include focus-ring;

        &:disabled {
            opacity: 0.6;
            cursor: default;
        }

        @each $name, $colors in $variants {
            &._#{$name} {
                padding: 0 space(6);
                background-color: list.nth($colors, 1);
                color: list.nth($colors, 2);

                @include hover {
                    background-color: list.nth($colors, 3);
                }
            }
        }

        &._link {
            color: color(secondary);

            @include typography(body-sm, 600);

            @include hover {
                color: color(secondary, 700);
            }
        }
    }

    ._md:not(._link) {
        height: 48px;
    }

    ._lg:not(._link) {
        gap: space(3);
        height: 56px;
        padding: 0 space(8);
        border-radius: radius(sm);
        font-size: rem(16px);
        letter-spacing: 0.192px;
    }
</style>
