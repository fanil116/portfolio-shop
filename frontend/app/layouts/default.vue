<script setup lang="ts">
    import TheFooter from '~/components/layout/TheFooter.vue';
    import TheHeader from '~/components/layout/TheHeader.vue';
</script>

<template>
    <div :class="$style.DefaultLayout">
        <TheHeader />
        <main :class="$style.main">
            <slot />
        </main>
        <TheFooter />
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
    }
</style>
