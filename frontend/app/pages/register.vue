<script setup lang="ts">
    import { useAuthStore } from '~/store/auth';

    import AuthForm from '~/components/auth/AuthForm.vue';

    import { getApiErrorMessage } from '~/composables/common/useApiErrors';
    import { getSafeRedirect } from '~/composables/common/useSafeRedirect';

    definePageMeta({ middleware: 'guest' });
    useHead({ title: 'Регистрация' });

    const authStore = useAuthStore();
    const route = useRoute();

    const form = reactive({ first_name: '', email: '', password: '' });
    const error = ref('');
    const pending = ref(false);

    async function onSubmit(): Promise<void> {
        error.value = '';
        pending.value = true;
        try {
            await authStore.register(form);
            await navigateTo(getSafeRedirect(route.query.next));
        } catch (e) {
            error.value = getApiErrorMessage(e);
        } finally {
            pending.value = false;
        }
    }
</script>

<template>
    <div class="container">
        <AuthForm
            title="Регистрация"
            submit-text="Создать аккаунт"
            :error="error"
            :pending="pending"
            @submit="onSubmit"
        >
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
                Email
                <input
                    v-model.trim="form.email"
                    type="email"
                    name="email"
                    autocomplete="email"
                    required
                />
            </label>
            <label>
                Пароль
                <input
                    v-model="form.password"
                    type="password"
                    name="password"
                    autocomplete="new-password"
                    required
                />
            </label>

            <template #footer>
                <p>
                    Уже есть аккаунт?
                    <NuxtLink :to="{ path: '/login', query: route.query }">Войти</NuxtLink>
                </p>
            </template>
        </AuthForm>
    </div>
</template>
