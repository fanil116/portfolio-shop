<script setup lang="ts">
    import type { IHomeBlock } from '~/repository/modules/content/types';

    import { useAuthStore } from '~/store/auth';

    import VButton from '~/components/ui/VButton.vue';

    import { getApiErrorMessage } from '~/composables/common/useApiErrors';

    defineProps<{ block: IHomeBlock }>();

    const { $fetchData } = useNuxtApp();
    const authStore = useAuthStore();

    const email = ref('');
    const status = ref<'idle' | 'pending' | 'done' | 'error'>('idle');
    const error = ref('');

    async function onSubmit(): Promise<void> {
        status.value = 'pending';
        error.value = '';
        try {
            await authStore.ensureCsrf();
            await $fetchData.content.subscribe(email.value.trim());
            status.value = 'done';
            email.value = '';
        } catch (e) {
            status.value = 'error';
            error.value = getApiErrorMessage(e);
        }
    }
</script>

<template>
    <section :class="$style.HomeNewsletter">
        <div :class="['container', $style.inner]">
            <h2 :class="$style.title">{{ block.title || 'Подпишитесь на рассылку' }}</h2>
            <p
                v-if="block.subtitle"
                :class="$style.subtitle"
            >
                {{ block.subtitle }}
            </p>

            <form
                :class="$style.form"
                @submit.prevent="onSubmit"
            >
                <label
                    for="newsletter-email"
                    :class="$style.hidden"
                >
                    Email
                </label>
                <input
                    id="newsletter-email"
                    v-model="email"
                    type="email"
                    required
                    autocomplete="email"
                    placeholder="Ваш email"
                    :class="$style.input"
                />
                <VButton
                    type="submit"
                    icon="arrow-right"
                    :disabled="status === 'pending'"
                >
                    Подписаться
                </VButton>
            </form>
            <p
                :class="[$style.status, { [$style._error]: status === 'error' }]"
                role="status"
            >
                <template v-if="status === 'done'">Готово! Проверьте почту.</template>
                <template v-else-if="status === 'error'">{{ error }}</template>
            </p>

            <ul
                v-if="block.brands.length"
                :class="$style.brands"
            >
                <li
                    v-for="brand in block.brands"
                    :key="brand.id"
                >
                    <img
                        v-if="brand.logo"
                        :src="brand.logo"
                        :alt="brand.name"
                        :class="$style.logo"
                        loading="lazy"
                    />
                    <span
                        v-else
                        :class="$style.brandName"
                    >
                        {{ brand.name }}
                    </span>
                </li>
            </ul>
        </div>
    </section>
</template>

<style lang="scss" module>
    .HomeNewsletter {
        background-color: color(secondary, 700);
        color: color(gray, 0);
    }

    .inner {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: space(3);
        padding-top: fluid(48px, 72px);
        padding-bottom: fluid(48px, 72px);
        text-align: center;
    }

    .hidden {
        @include visually-hidden;
    }

    .title {
        font-size: fluid(24px, 32px);
        font-weight: 600;
        line-height: 1.25;
    }

    .subtitle {
        max-width: 536px;
        opacity: 0.7;
    }

    .form {
        display: flex;
        flex-wrap: wrap;
        gap: space(3) space(4);
        width: 100%;
        max-width: 624px;
        margin-top: space(5);
        padding: space(3);
        border-radius: radius(sm);
        background-color: color(gray, 0);
        box-shadow: 0 12px 12px rgb(0 0 0 / 12%);

        > button {
            flex: 1 0 auto;

            @include respond-to(sm) {
                flex: none;
            }
        }
    }

    .input {
        flex: 1 1 260px;
        min-width: 0;
        height: 48px;
        padding: 0 space(4);
        border: none;
        font: inherit;
        color: color(gray, 900);

        &::placeholder {
            color: color(gray, 500);
        }

        &:focus {
            outline: none;
        }
    }

    .status {
        min-height: 24px;

        @include typography(body-sm);

        &._error {
            color: color(warning, 300);
        }
    }

    .brands {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: center;
        gap: space(6) space(12);
        margin-top: space(4);
        padding-top: space(8);
        border-top: 1px solid rgb(255 255 255 / 16%);
        opacity: 0.6;

        @include reset-list;
    }

    .logo {
        max-width: 120px;
        max-height: 40px;
    }

    .brandName {
        @include typography(body-lg, 600);
    }
</style>
