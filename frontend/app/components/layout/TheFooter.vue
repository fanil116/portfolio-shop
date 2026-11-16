<script setup lang="ts">
    import { useSiteStore } from '~/store/site';

    import SiteLogo from '~/components/layout/SiteLogo.vue';
    import VIcon from '~/components/ui/VIcon.vue';

    const siteStore = useSiteStore();

    const settings = computed(() => siteStore.settings);
    const columns = computed(() => siteStore.menusByPlacement.footer);
    const tags = computed(() => siteStore.menusByPlacement.footer_tags[0]);
    // В колонке «Категории» — первые шесть корневых, как в макете
    const MAX_CATEGORIES = 6;
    const topCategories = computed(() => siteStore.categories.slice(0, MAX_CATEGORIES));

    const apps = computed(() =>
        [
            { url: settings.value?.google_play_url, icon: 'google-play', name: 'Google Play' },
            { url: settings.value?.app_store_url, icon: 'apple', name: 'App Store' },
        ].filter((app) => app.url)
    );
</script>

<template>
    <footer :class="$style.TheFooter">
        <div :class="['container', $style.grid]">
            <div :class="$style.about">
                <SiteLogo
                    :name="settings?.site_name ?? 'Clicon'"
                    :logo="settings?.logo"
                    tone="accent"
                />
                <div
                    v-if="settings?.phone"
                    :class="$style.support"
                >
                    <span :class="$style.muted">Служба поддержки:</span>
                    <a
                        :href="`tel:${settings.phone.replace(/[^\d+]/g, '')}`"
                        :class="$style.phone"
                    >
                        {{ settings.phone }}
                    </a>
                </div>
                <address
                    v-if="settings?.address"
                    :class="$style.address"
                >
                    {{ settings.address }}
                </address>
                <a
                    v-if="settings?.email"
                    :href="`mailto:${settings.email}`"
                    :class="$style.email"
                >
                    {{ settings.email }}
                </a>
            </div>

            <nav
                v-if="topCategories.length"
                :class="$style.column"
                aria-label="Категории"
            >
                <h2 :class="$style.title">Категории</h2>
                <ul :class="$style.links">
                    <li
                        v-for="category in topCategories"
                        :key="category.id"
                    >
                        <NuxtLink
                            :to="`/catalog/${category.slug}`"
                            :class="$style.link"
                        >
                            {{ category.name }}
                        </NuxtLink>
                    </li>
                    <li>
                        <NuxtLink
                            to="/catalog"
                            :class="$style.all"
                        >
                            Весь каталог
                            <VIcon
                                name="arrow-right"
                                :size="20"
                            />
                        </NuxtLink>
                    </li>
                </ul>
            </nav>

            <nav
                v-for="menu in columns"
                :key="menu.id"
                :class="$style.column"
                :aria-label="menu.title"
            >
                <h2 :class="$style.title">{{ menu.title }}</h2>
                <ul :class="$style.links">
                    <li
                        v-for="item in menu.items"
                        :key="item.id"
                    >
                        <NuxtLink
                            :to="item.url"
                            :class="$style.link"
                        >
                            {{ item.title }}
                        </NuxtLink>
                    </li>
                </ul>
            </nav>

            <div
                v-if="apps.length"
                :class="$style.column"
            >
                <h2 :class="$style.title">Приложение</h2>
                <a
                    v-for="app in apps"
                    :key="app.icon"
                    :href="app.url"
                    :class="$style.app"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    <VIcon
                        :name="app.icon"
                        :size="32"
                    />
                    <span>
                        <small :class="$style.appCaption">Скачать в</small>
                        {{ app.name }}
                    </span>
                </a>
            </div>

            <nav
                v-if="tags?.items.length"
                :class="[$style.column, $style.tagsColumn]"
                :aria-label="tags.title"
            >
                <h2 :class="$style.title">{{ tags.title }}</h2>
                <ul :class="$style.tags">
                    <li
                        v-for="item in tags.items"
                        :key="item.id"
                    >
                        <NuxtLink
                            :to="item.url"
                            :class="$style.tag"
                        >
                            {{ item.title }}
                        </NuxtLink>
                    </li>
                </ul>
            </nav>
        </div>

        <p
            v-if="settings?.copyright_text"
            :class="$style.copyright"
        >
            {{ settings.copyright_text }}
        </p>
    </footer>
</template>

<style lang="scss" module>
    .TheFooter {
        background-color: color(gray, 900);
        color: color(gray, 0);
    }

    // Колонки переносятся сами: auto-fit по минимальной ширине колонки
    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: space(10) space(6);
        padding-top: fluid(48px, 72px);
        padding-bottom: fluid(48px, 72px);
    }

    .about {
        display: flex;
        flex-direction: column;
        gap: space(3);
        grid-column: 1 / -1;

        @include respond-to(lg) {
            grid-column: span 2;
        }
    }

    .support {
        display: flex;
        flex-direction: column;
        gap: space(1);
        margin-top: space(3);
    }

    .muted {
        color: color(gray, 500);

        @include typography(body-sm);
    }

    .phone {
        @include typography(body-lg, 500);
        @include focus-ring(color(gray, 0));
    }

    .address {
        max-width: 248px;
        font-style: normal;
        color: color(gray, 300);
    }

    .email {
        @include typography(body-md, 500);
        @include focus-ring(color(gray, 0));
    }

    .column {
        display: flex;
        flex-direction: column;
        gap: space(3);
    }

    .title {
        text-transform: uppercase;

        @include typography(body-md, 500);
    }

    .links,
    .tags {
        @include reset-list;
    }

    .link,
    .all {
        display: inline-flex;
        align-items: center;
        gap: space(2);
        padding: space(1.5) 0;
        transition: color $transition-fast;

        @include typography(body-sm, 500);
        @include focus-ring(color(gray, 0));
    }

    .link {
        position: relative;
        color: color(gray, 400);

        // Акцентная черта слева появляется при наведении, как у активного пункта в макете
        &:before {
            content: '';
            width: 0;
            height: 2px;
            background-color: color(warning);
            transition: width $transition-fast;
        }

        @include hover {
            color: color(gray, 0);

            &:before {
                width: space(6);
            }
        }
    }

    .all {
        color: color(warning);
    }

    .app {
        display: inline-flex;
        align-items: center;
        gap: space(4);
        width: fit-content;
        padding: space(4) space(5);
        border-radius: radius(sm);
        background-color: color(gray, 800);
        transition: background-color $transition-fast;

        @include typography(body-sm, 600);
        @include focus-ring(color(gray, 0));

        @include hover {
            background-color: color(gray, 700);
        }
    }

    .appCaption {
        display: block;
        font-size: rem(11px);
        font-weight: 400;
        line-height: 13px;
    }

    .tagsColumn {
        grid-column: span 2;

        @include respond-below(sm) {
            grid-column: 1 / -1;
        }
    }

    .tags {
        display: flex;
        flex-wrap: wrap;
        gap: space(2);
    }

    .tag {
        display: block;
        padding: space(1.5) space(3);
        border-radius: radius(xs);
        border: 1px solid color(gray, 800);
        transition:
            background-color $transition-fast,
            border-color $transition-fast;

        @include typography(body-sm, 500);
        @include focus-ring(color(gray, 0));

        @include hover {
            border-color: color(gray, 0);
            background-color: color(gray, 800);
        }
    }

    .copyright {
        padding: space(6) space(4);
        box-shadow: inset 0 1px 0 color(gray, 800);
        text-align: center;
        color: color(gray, 300);

        @include typography(body-sm);
    }
</style>
