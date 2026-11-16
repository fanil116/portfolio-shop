<script setup lang="ts">
    import type { NuxtError } from '#app';

    const props = defineProps<{ error: NuxtError }>();

    const title = computed(() =>
        props.error.statusCode === 404 ? 'Страница не найдена' : 'Что-то пошло не так'
    );

    function goHome(): void {
        clearError({ redirect: '/' });
    }
</script>

<template>
    <main :class="$style.ErrorPage">
        <p :class="$style.code">{{ error.statusCode }}</p>
        <h1>{{ title }}</h1>
        <button
            type="button"
            :class="$style.button"
            @click="goHome"
        >
            На главную
        </button>
    </main>
</template>

<style lang="scss" module>
    .ErrorPage {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        gap: space(6);
        min-height: 100vh;
        padding: space(4);
        text-align: center;
    }

    .code {
        font-size: fluid(64px, 120px);
        font-weight: 700;
        line-height: 1;
        color: color(primary);
    }

    .button {
        @include reset-button;

        padding: 0 space(6);
        border-radius: radius(xs);
        background-color: color(primary);
        line-height: 48px;
        color: color(gray, 0);

        @include typography(caption);
        @include focus-ring;
    }
</style>
