<script setup lang="ts">
    import { useAuthStore } from '~/store/auth';

    import AuthForm from '~/components/auth/AuthForm.vue';

    import { getApiErrorMessage } from '~/composables/common/useApiErrors';
    import { getSafeRedirect } from '~/composables/common/useSafeRedirect';

    definePageMeta({ middleware: 'guest' });
    useHead({ title: 'Вход' });

    const authStore = useAuthStore();
    const route = useRoute();

    const form = reactive({ email: '', password: '' });
    const error = ref('');
    const pending = ref(false);

    async function onSubmit(): Promise<void> {
        error.value = '';
        pending.value = true;
        try {
            await authStore.login(form);
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
            title="Вход"
            submit-text="Войти"
            :error="error"
            :pending="pending"
            @submit="onSubmit"
        >
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
                    autocomplete="current-password"
                    required
                />
            </label>

            <template #footer>
                <p>
                    Нет аккаунта?
                    <NuxtLink :to="{ path: '/register', query: route.query }">
                        Зарегистрироваться
                    </NuxtLink>
                </p>
            </template>
        </AuthForm>
    </div>
</template>
