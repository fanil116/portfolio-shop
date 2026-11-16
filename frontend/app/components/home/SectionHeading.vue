<script setup lang="ts">
    import VButton from '~/components/ui/VButton.vue';

    withDefaults(
        defineProps<{
            title: string;
            linkText?: string;
            linkUrl?: string;
            size?: 'md' | 'lg';
        }>(),
        { linkText: '', linkUrl: '', size: 'md' }
    );
</script>

<template>
    <div :class="[$style.SectionHeading, $style[`_${size}`]]">
        <div :class="$style.start">
            <h2 :class="$style.title">{{ title }}</h2>
            <slot name="extra" />
        </div>
        <div :class="$style.end">
            <slot name="end" />
            <VButton
                v-if="linkText && linkUrl"
                :to="linkUrl"
                variant="link"
                icon="arrow-right"
            >
                {{ linkText }}
            </VButton>
        </div>
    </div>
</template>

<style lang="scss" module>
    .SectionHeading {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        gap: space(3) space(6);
        margin-bottom: space(6);
    }

    .start,
    .end {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        gap: space(3) space(6);

        // Не шире заголовка: длинные табы прокручиваются внутри, а не раздвигают страницу
        min-width: 0;
        max-width: 100%;
    }

    .title {
        @include typography(body-xl, 600);

        @include respond-to(md) {
            @include typography(heading-03);
        }
    }

    // Крупный центрированный заголовок («Покупайте по категориям»)
    ._lg {
        justify-content: center;
        margin-bottom: space(10);

        .title {
            text-align: center;
            font-size: fluid(24px, 32px);
            line-height: 1.25;
        }
    }
</style>
