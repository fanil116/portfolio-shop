<script setup lang="ts">
    import type { IPromo } from '~/repository/modules/content/types';

    import VButton from '~/components/ui/VButton.vue';
    import VIcon from '~/components/ui/VIcon.vue';

    const props = defineProps<{ promo: IPromo }>();

    // Короткий отпечаток текста акции: новая акция из админки снова видна тем,
    // кто закрыл предыдущую (djb2 — достаточно для различения, не для безопасности)
    const promoKey = computed(() => {
        const text = Object.values(props.promo).join('|');
        let hash = 5381;
        for (const char of text) {
            hash = (hash * 33) ^ char.charCodeAt(0);
        }
        return (hash >>> 0).toString(36);
    });

    // Закрытая полоса не возвращается до конца сессии браузера
    const closedKey = useCookie<string | null>('promo-closed', { default: () => null });
    const isClosed = computed(() => closedKey.value === promoKey.value);
</script>

<template>
    <aside
        v-if="!isClosed"
        :class="$style.HeaderPromo"
    >
        <div :class="['container', $style.inner]">
            <p :class="$style.title">
                <span
                    v-if="promo.label"
                    :class="$style.label"
                >
                    {{ promo.label }}
                </span>
                {{ promo.title }}
            </p>
            <p :class="$style.offer">
                <span :class="$style.highlight">{{ promo.highlight }}</span>
                {{ promo.text }}
            </p>
            <VButton
                v-if="promo.button_text && promo.url"
                :to="promo.url"
                variant="warning"
                icon="arrow-right"
                :class="$style.button"
            >
                {{ promo.button_text }}
            </VButton>
        </div>
        <button
            type="button"
            :class="$style.close"
            aria-label="Скрыть акцию"
            @click="closedKey = promoKey"
        >
            <VIcon
                name="close"
                :size="16"
            />
        </button>
    </aside>
</template>

<style lang="scss" module>
    .HeaderPromo {
        position: relative;
        background-color: color(gray, 900);
        color: color(gray, 0);
    }

    .inner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: space(4);
        min-height: 56px;
        padding-right: space(14);

        @include respond-to(lg) {
            min-height: 80px;
        }
    }

    .title {
        display: flex;
        align-items: center;
        gap: space(3);

        @include typography(body-xl, 600);

        @include respond-to(lg) {
            @include typography(heading-03);
        }
    }

    // Плашка чуть повёрнута, как стикер на макете
    .label {
        padding: space(1.5) space(2.5);
        background-color: color(warning, 300);
        color: color(gray, 900);
        transform: rotate(-3deg);

        @include typography(body-xl, 600);
    }

    .offer {
        display: none;
        align-items: center;
        gap: space(2);

        @include typography(body-xl, 600);

        @include respond-to(md) {
            display: flex;
        }
    }

    .highlight {
        font-size: fluid(28px, 40px);
        line-height: 1.2;
        color: color(warning);
    }

    .button {
        display: none;

        @include respond-to(sm) {
            display: inline-flex;
        }
    }

    .close {
        @include reset-button;

        position: absolute;
        top: 50%;
        right: space(4);
        padding: space(2);
        border-radius: radius(xs);
        background-color: color(gray, 800);
        transform: translateY(-50%);
        transition: background-color $transition-fast;

        @include focus-ring(color(warning));

        @include hover {
            background-color: color(gray, 700);
        }
    }
</style>
