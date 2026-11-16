<script setup lang="ts">
    import { useAuthStore } from '~/store/auth';

    import AuthForm from '~/components/auth/AuthForm.vue';

    import { getApiErrorMessage } from '~/composables/common/useApiErrors';

    definePageMeta({ middleware: 'auth' });
    useHead({ title: 'Личный кабинет' });

    const authStore = useAuthStore();

    const form = reactive({
        first_name: authStore.user?.first_name ?? '',
        last_name: authStore.user?.last_name ?? '',
    });
    const error = ref('');
    const saved = ref(false);
    const pending = ref(false);

    async function onSave(): Promise<void> {
        error.value = '';
        saved.value = false;
        pending.value = true;
        try {
            await authStore.updateProfile(form);
            saved.value = true;
        } catch (e) {
            error.value = getApiErrorMessage(e);
        } finally {
            pending.value = false;
        }
    }

    async function onLogout(): Promise<void> {
        try {
            await authStore.logout();
            await navigateTo('/');
        } catch (e) {
            error.value = getApiErrorMessage(e);
        }
    }
</script>

<template>
    <div class="container">
        <AuthForm
            title="Профиль"
            submit-text="Сохранить"
            :error="error"
            :pending="pending"
            @submit="onSave"
        >
            <p :class="$style.email">{{ authStore.user?.email }}</p>
            <label>
                Имя
                <input
                    v-model.trim="form.first_name"
                    type="text"
                    name="first_name"
                    autocomplete="given-name"
                />
            </label>
            <label>
                Фамилия
                <input
                    v-model.trim="form.last_name"
                    type="text"
                    name="last_name"
                    autocomplete="family-name"
                />
            </label>
            <p
                v-if="saved"
                :class="$style.saved"
            >
                Сохранено
            </p>

            <template #footer>
                <button
                    type="button"
                    :class="$style.logout"
                    @click="onLogout"
                >
                    Выйти
                </button>
            </template>
        </AuthForm>
    </div>
</template>

<style lang="scss" module>
    .email {
        text-align: center;
        color: color(gray, 600);
    }

    .saved {
        color: color(success);

        @include typography(body-sm);
    }

    .logout {
        @include reset-button;

        align-self: center;
        color: color(gray, 600);

        @include typography(body-sm, 500);
        @include focus-ring;

        @include hover {
            color: color(danger);
        }
    }
</style>
