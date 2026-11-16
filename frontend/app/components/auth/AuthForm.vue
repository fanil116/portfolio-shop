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
        gap: space(4);
        width: 100%;
        max-width: 424px;
        margin: space(10) auto;
        padding: space(8);
        border-radius: radius(sm);
        border: 1px solid color(gray, 100);
        background-color: color(gray, 0);
        box-shadow: $shadow-dropdown;

        label {
            display: flex;
            flex-direction: column;
            gap: space(2);
            color: color(gray, 900);

            @include typography(body-sm);
        }

        input {
            height: 44px;
            padding: 0 space(4);
            border-radius: radius(xs);
            border: 1px solid color(gray, 100);
            background-color: color(gray, 0);
            font: inherit;
            color: color(gray, 900);
            transition: border-color $transition-fast;

            &:focus {
                border-color: color(primary);
                outline: none;
            }
        }
    }

    .title {
        text-align: center;

        @include typography(body-xl, 600);
    }

    .error {
        color: color(danger);

        @include typography(body-sm);
    }

    .submit {
        @include reset-button;

        height: 48px;
        border-radius: radius(xs);
        background-color: color(primary);
        color: color(gray, 0);
        transition: background-color $transition-fast;

        @include typography(caption);
        @include focus-ring;

        @include hover {
            background-color: color(primary, 600);
        }

        &:disabled {
            opacity: 0.6;
            cursor: default;
        }
    }
</style>
