<script setup lang="ts">
    defineProps<{
        title: string;
        submitText: string;
        error?: string;
        pending?: boolean;
    }>();

    const emit = defineEmits<{ submit: [] }>();
</script>

<template>
    <form
        :class="$style.AuthForm"
        novalidate
        @submit.prevent="emit('submit')"
    >
        <h1 :class="$style.title">{{ title }}</h1>

        <slot />

        <p
            v-if="error"
            :class="$style.error"
            role="alert"
        >
            {{ error }}
        </p>

        <button
            type="submit"
            :class="$style.submit"
            :disabled="pending"
        >
            {{ submitText }}
        </button>

        <slot name="footer" />
    </form>
</template>

<style lang="scss" module>
    .AuthForm {
        display: flex;
        flex-direction: column;
        gap: 16px;
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        padding: 32px;
        border-radius: $radius;
        border: 1px solid $color-border;
        background-color: $color-surface;

        label {
            display: flex;
            flex-direction: column;
            gap: 6px;
            font-size: 14px;
            color: $color-muted;
        }

        input {
            padding: 10px 12px;
            border-radius: 8px;
            border: 1px solid $color-border;
            background-color: $color-bg;
            font: inherit;
            color: $color-text;
        }
    }

    .title {
        margin: 0 0 8px;
        font-size: 24px;
    }

    .error {
        margin: 0;
        font-size: 14px;
        color: $color-error;
    }

    .submit {
        padding: 12px;
        border-radius: 8px;
        border: none;
        background-color: $color-accent;
        font: inherit;
        color: #fff;
        cursor: pointer;

        &:disabled {
            opacity: 0.6;
            cursor: default;
        }
    }
</style>
