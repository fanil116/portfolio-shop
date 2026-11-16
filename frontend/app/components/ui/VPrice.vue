<script setup lang="ts">
    import { formatPrice } from '~/composables/common/useFormatPrice';

    withDefaults(
        defineProps<{
            price: string;
            oldPrice?: string | null;
            size?: 'sm' | 'md';
        }>(),
        { oldPrice: null, size: 'sm' }
    );
</script>

<template>
    <span :class="[$style.VPrice, $style[`_${size}`]]">
        <s
            v-if="oldPrice"
            :class="$style.old"
        >
            {{ formatPrice(oldPrice) }}
        </s>
        <span :class="$style.current">{{ formatPrice(price) }}</span>
    </span>
</template>

<style lang="scss" module>
    .VPrice {
        display: inline-flex;
        flex-wrap: wrap;
        align-items: baseline;
        gap: space(1);
        white-space: nowrap;
    }

    .old {
        color: color(gray, 400);
    }

    .current {
        font-weight: 600;
        color: color(secondary);
    }

    ._sm {
        @include typography(body-sm);
    }

    ._md {
        .old {
            @include typography(body-md);
        }

        .current {
            @include typography(body-lg, 600);
        }
    }
</style>
