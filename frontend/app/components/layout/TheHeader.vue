<script setup lang="ts">
    import { useAuthStore } from '~/store/auth';

    const authStore = useAuthStore();
</script>

<template>
    <header :class="$style.TheHeader">
        <div :class="['container', $style.inner]">
            <NuxtLink
                to="/"
                :class="$style.logo"
            >
                Portfolio
            </NuxtLink>

            <nav :class="$style.nav">
                <NuxtLink
                    v-if="authStore.isAuthenticated"
                    to="/lk"
                >
                    Личный кабинет
                </NuxtLink>
                <NuxtLink
                    v-else
                    to="/login"
                >
                    Войти
                </NuxtLink>
            </nav>
        </div>
    </header>
</template>

<style lang="scss" module>
    .TheHeader {
        border-bottom: 1px solid $color-border;
        background-color: $color-surface;
    }

    .inner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 64px;
    }

    .logo {
        text-decoration: none;
        font-size: 20px;
        font-weight: 700;
    }

    .nav {
        display: flex;
        gap: 24px;

        a {
            text-decoration: none;
            color: $color-muted;
            transition: color $transition;

            &:hover {
                color: $color-text;
            }
        }
    }
</style>
