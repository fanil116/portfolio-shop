<script setup lang="ts">
    import VIcon from '~/components/ui/VIcon.vue';

    withDefaults(defineProps<{ name: string; logo?: string | null; tone?: 'light' | 'accent' }>(), {
        logo: null,
        tone: 'light',
    });
</script>

<template>
    <NuxtLink
        to="/"
        :class="[$style.SiteLogo, $style[`_${tone}`]]"
        :aria-label="`${name} — на главную`"
    >
        <img
            v-if="logo"
            :src="logo"
            :alt="name"
            :class="$style.image"
        />
        <template v-else>
            <VIcon
                name="logo-mark"
                :class="$style.mark"
            />
            <span :class="$style.name">{{ name }}</span>
        </template>
    </NuxtLink>
</template>

<style lang="scss" module>
    .SiteLogo {
        display: inline-flex;
        flex-shrink: 0;
        align-items: center;
        gap: space(2);
        color: color(gray, 0);

        @include focus-ring(color(gray, 0));
    }

    // В футере значок оранжевый, текст белый
    ._accent .mark {
        color: color(primary);
    }

    .mark {
        --icon-size: #{fluid(36px, 48px)};
    }

    .name {
        font-size: fluid(24px, 32px);
        font-weight: 700;
        line-height: 1.25;
        letter-spacing: -0.02em;
        text-transform: uppercase;
    }

    .image {
        max-height: 48px;
    }
</style>
