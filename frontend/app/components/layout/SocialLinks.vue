<script setup lang="ts">
    import VIcon from '~/components/ui/VIcon.vue';

    defineProps<{ socials: { network: string; url: string }[] }>();

    // Соцсеть → иконка из assets/icons; для сетей без иконки в макете — короткая подпись
    const ICONS: Record<string, string> = {
        x: 'twitter',
        facebook: 'facebook',
        pinterest: 'pinterest',
        reddit: 'reddit',
        youtube: 'youtube',
        instagram: 'instagram',
    };
    const LABELS: Record<string, string> = { telegram: 'TG', vk: 'VK' };
    const TITLES: Record<string, string> = { telegram: 'Telegram', vk: 'ВКонтакте', x: 'X' };
</script>

<template>
    <ul :class="$style.SocialLinks">
        <li
            v-for="social in socials"
            :key="social.network"
        >
            <a
                :href="social.url"
                :class="$style.link"
                :aria-label="TITLES[social.network] ?? social.network"
                target="_blank"
                rel="noopener noreferrer"
            >
                <VIcon
                    v-if="ICONS[social.network]"
                    :name="ICONS[social.network]!"
                    :size="16"
                />
                <span
                    v-else
                    :class="$style.text"
                >
                    {{ LABELS[social.network] ?? social.network.slice(0, 2).toUpperCase() }}
                </span>
            </a>
        </li>
    </ul>
</template>

<style lang="scss" module>
    .SocialLinks {
        display: flex;
        gap: space(3);

        @include reset-list;
    }

    .link {
        display: flex;
        align-items: center;
        justify-content: center;
        min-width: 16px;
        height: 16px;
        opacity: 0.85;
        transition: opacity $transition-fast;

        @include focus-ring(color(gray, 0));

        @include hover {
            opacity: 1;
        }
    }

    .text {
        font-size: rem(11px);
        font-weight: 700;
        line-height: 1;
    }
</style>
