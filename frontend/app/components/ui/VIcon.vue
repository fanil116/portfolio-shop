<script setup lang="ts">
    // Все SVG из assets/icons как URL. Иконка рисуется через CSS mask:
    // цвет задаётся color родителя (currentColor), hover меняет его без второго файла.
    const icons = import.meta.glob<string>('~/assets/icons/*.svg', {
        eager: true,
        query: '?url',
        import: 'default',
    });

    const iconByName = Object.fromEntries(
        Object.entries(icons).map(([path, url]) => [path.replace(/^.*\/|\.svg$/g, ''), url])
    );

    // Без size размер берётся из --icon-size родителя (удобно для адаптивных размеров)
    const props = defineProps<{ name: string; size?: number }>();

    const style = computed(() => {
        const url = iconByName[props.name];
        if (!url && import.meta.dev) {
            console.warn(`[VIcon] нет иконки «${props.name}» в assets/icons`);
        }
        return {
            '--icon': url ? `url("${url}")` : 'none',
            ...(props.size ? { '--icon-size': `${props.size}px` } : {}),
        };
    });
</script>

<template>
    <span
        :class="$style.VIcon"
        :style="style"
        aria-hidden="true"
    />
</template>

<style lang="scss" module>
    .VIcon {
        display: inline-block;
        flex-shrink: 0;
        width: var(--icon-size, 24px);
        height: var(--icon-size, 24px);
        background-color: currentcolor;
        mask: var(--icon) center / contain no-repeat;
    }
</style>
