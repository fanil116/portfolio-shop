<script setup lang="ts">
    // Любой неизвестный путь (в том числе ещё не сделанные каталог, товар, корзина) —
    // штатная 404 через error.vue, а не пустая страница и предупреждения роутера
    throw createError({ statusCode: 404, statusMessage: 'Страница не найдена', fatal: true });
</script>

<template>
    <div />
</template>
