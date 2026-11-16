<script setup lang="ts">
    import VIcon from '~/components/ui/VIcon.vue';

    const props = defineProps<{ rating: string | number; count?: number }>();

    const STARS = 5;
    // Ширина закрашенного слоя — рейтинг в процентах от пяти звёзд (4.5 → 90%)
    const fill = computed(() => `${(Math.min(Number(props.rating), STARS) / STARS) * 100}%`);
    const countText = computed(() =>
        props.count === undefined ? '' : `(${new Intl.NumberFormat('ru-RU').format(props.count)})`
    );
</script>

<template>
    <span :class="$style.VRating">
        <span
            :class="$style.stars"
            :style="{ '--fill': fill }"
            role="img"
            :aria-label="`Рейтинг ${rating} из ${STARS}`"
        >
            <span
                v-for="layer in ['base', 'filled']"
                :key="layer"
                :class="$style[layer]"
            >
                <VIcon
                    v-for="index in STARS"
                    :key="index"
                    name="star"
                    :size="16"
                />
            </span>
        </span>
        <span
            v-if="countText"
            :class="$style.count"
        >
            {{ countText }}
        </span>
    </span>
</template>

<style lang="scss" module>
    .VRating {
        display: inline-flex;
        align-items: center;
        gap: space(1);
    }

    // Два одинаковых ряда звёзд: серый снизу и жёлтый сверху, обрезанный по --fill.
    // Дробный рейтинг даёт частично закрашенную звезду без лишней разметки.
    .stars {
        position: relative;
        display: inline-flex;
    }

    .base,
    .filled {
        display: inline-flex;
        gap: space(0.5);
    }

    .base {
        color: color(gray, 200);
    }

    .filled {
        position: absolute;
        top: 0;
        left: 0;
        overflow: hidden;
        width: var(--fill);
        color: color(warning, 400);
    }

    .count {
        color: color(gray, 500);

        @include typography(body-tiny);
    }
</style>
