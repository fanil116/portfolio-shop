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
        min-height: 100vh;
        padding: $gutter;
        text-align: center;
    }

    .code {
        margin: 0;
        font-size: 64px;
        font-weight: 700;
        color: $color-accent;
    }

    .button {
        padding: 12px 24px;
        border-radius: $radius;
        border: none;
        background-color: $color-accent;
        font: inherit;
        color: #fff;
        cursor: pointer;
    }
</style>
