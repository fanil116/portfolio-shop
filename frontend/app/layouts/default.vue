<script setup lang="ts">
    import TheHeader from '~/components/layout/TheHeader.vue';
</script>

<template>
    <div :class="$style.DefaultLayout">
        <TheHeader />
        <main :class="$style.main">
            <slot />
        </main>
    </div>
</template>

<style lang="scss" module>
    .DefaultLayout {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    .main {
        flex: 1;
        padding: 40px 0;
    }
</style>
