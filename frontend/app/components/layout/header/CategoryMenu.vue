<script setup lang="ts">
    import type { ICategoryNode } from '~/repository/modules/catalog/types';

    import VIcon from '~/components/ui/VIcon.vue';

    defineProps<{ categories: ICategoryNode[] }>();

    const isOpen = ref(false);
    const root = ref<HTMLElement | null>(null);
    const route = useRoute();

    // Закрываем при переходе, клике снаружи и по Escape
    watch(
        () => route.fullPath,
        () => (isOpen.value = false)
    );

    function onDocumentClick(event: MouseEvent): void {
        if (root.value && !root.value.contains(event.target as Node)) {
            isOpen.value = false;
        }
    }

    function onKeydown(event: KeyboardEvent): void {
        if (event.key === 'Escape') {
            isOpen.value = false;
        }
    }

    onMounted(() => {
        document.addEventListener('click', onDocumentClick);
        document.addEventListener('keydown', onKeydown);
    });
    onBeforeUnmount(() => {
        document.removeEventListener('click', onDocumentClick);
        document.removeEventListener('keydown', onKeydown);
    });
</script>

<template>
    <div
        ref="root"
        :class="$style.CategoryMenu"
    >
        <button
            type="button"
            :class="[$style.toggle, { [$style._open]: isOpen }]"
            :aria-expanded="isOpen"
            aria-controls="category-menu"
            @click="isOpen = !isOpen"
        >
            Все категории
            <VIcon
                name="caret-down"
                :size="16"
                :class="$style.caret"
            />
        </button>

        <nav
            id="category-menu"
            :class="[$style.dropdown, { [$style._visible]: isOpen }]"
            aria-label="Каталог"
            :inert="!isOpen"
        >
            <ul :class="$style.list">
                <li
                    v-for="category in categories"
                    :key="category.id"
                    :class="$style.item"
                >
                    <NuxtLink
                        :to="`/catalog/${category.slug}`"
                        :class="$style.link"
                    >
                        {{ category.name }}
                        <VIcon
                            v-if="category.children.length"
                            name="arrow-right"
                            :size="16"
                        />
                    </NuxtLink>
                    <ul
                        v-if="category.children.length"
                        :class="$style.submenu"
                    >
                        <li
                            v-for="child in category.children"
                            :key="child.id"
                        >
                            <NuxtLink
                                :to="`/catalog/${child.slug}`"
                                :class="$style.link"
                            >
                                {{ child.name }}
                            </NuxtLink>
                        </li>
                    </ul>
                </li>
            </ul>
        </nav>
    </div>
</template>

<style lang="scss" module>
    .CategoryMenu {
        position: relative;
    }

    .toggle {
        @include reset-button;

        display: inline-flex;
        align-items: center;
        gap: space(2);
        height: 48px;
        white-space: nowrap;
        padding: 0 space(6);
        border-radius: radius(xs);
        background-color: color(gray, 50);
        color: color(gray, 900);
        transition:
            background-color $transition-fast,
            color $transition-fast;

        @include typography(body-sm, 500);
        @include focus-ring;

        &._open {
            background-color: color(primary);
            color: color(gray, 0);
        }
    }

    .caret {
        transition: transform $transition-fast;

        ._open & {
            transform: rotate(180deg);
        }
    }

    .dropdown {
        position: absolute;
        top: calc(100% + #{space(2)});
        left: 0;
        z-index: z(dropdown);
        width: 264px;
        padding: space(3) 0;
        border-radius: radius(sm);
        border: 1px solid color(gray, 100);
        background-color: color(gray, 0);
        box-shadow: $shadow-dropdown;
        visibility: hidden;
        opacity: 0;
        transform: translateY(-4px);
        transition:
            opacity $transition-fast,
            transform $transition-fast,
            visibility $transition-fast;

        &._visible {
            visibility: visible;
            opacity: 1;
            transform: none;
        }
    }

    .list,
    .submenu {
        @include reset-list;
    }

    .item {
        position: relative;
    }

    .link {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: space(2) space(4);
        color: color(gray, 600);
        transition:
            background-color $transition-fast,
            color $transition-fast;

        @include typography(body-sm);
        @include focus-ring;

        @include hover {
            background-color: color(gray, 50);
            color: color(gray, 900);
        }
    }

    // Подкатегории: справа на десктопе, вложенным списком на узких экранах
    .submenu {
        padding-left: space(4);

        @include respond-to(lg) {
            position: absolute;
            top: 0;
            left: 100%;
            visibility: hidden;
            width: 240px;
            padding: space(3) 0;
            border-radius: radius(sm);
            border: 1px solid color(gray, 100);
            background-color: color(gray, 0);
            box-shadow: $shadow-dropdown;
            opacity: 0;
            transition: opacity $transition-fast;

            .item:hover > &,
            .item:focus-within > & {
                visibility: visible;
                opacity: 1;
            }
        }
    }
</style>
