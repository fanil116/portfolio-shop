<script setup lang="ts">
    import { useAuthStore } from '~/store/auth';
    import { useSiteStore } from '~/store/site';

    import CategoryMenu from '~/components/layout/header/CategoryMenu.vue';
    import HeaderPromo from '~/components/layout/header/HeaderPromo.vue';
    import SiteLogo from '~/components/layout/SiteLogo.vue';
    import SocialLinks from '~/components/layout/SocialLinks.vue';
    import VIcon from '~/components/ui/VIcon.vue';

    const authStore = useAuthStore();
    const siteStore = useSiteStore();

    const settings = computed(() => siteStore.settings);
    const quickLinks = computed(() => siteStore.menusByPlacement.header[0]?.items ?? []);
    const phoneHref = computed(() => `tel:${settings.value?.phone.replace(/[^\d+]/g, '')}`);

    // Иконки пунктов меню из админки → файлы в assets/icons
    const MENU_ICONS: Record<string, string> = { location: 'map-pin' };

    const query = ref('');

    async function onSearch(): Promise<void> {
        const q = query.value.trim();
        if (q) {
            await navigateTo({ path: '/catalog', query: { q } });
        }
    }
</script>

<template>
    <header :class="$style.TheHeader">
        <HeaderPromo
            v-if="settings?.promo"
            :promo="settings.promo"
        />

        <div :class="$style.top">
            <div :class="['container', $style.topInner]">
                <p :class="$style.welcome">{{ settings?.welcome_text }}</p>
                <div
                    v-if="settings?.socials.length"
                    :class="$style.follow"
                >
                    <span :class="$style.followLabel">Мы в соцсетях:</span>
                    <SocialLinks :socials="settings.socials" />
                </div>
            </div>
        </div>

        <div :class="$style.middle">
            <div :class="['container', $style.middleInner]">
                <SiteLogo
                    :name="settings?.site_name ?? 'Clicon'"
                    :logo="settings?.logo"
                />

                <form
                    :class="$style.search"
                    role="search"
                    @submit.prevent="onSearch"
                >
                    <label
                        for="header-search"
                        :class="$style.hidden"
                    >
                        Поиск по каталогу
                    </label>
                    <input
                        id="header-search"
                        v-model="query"
                        type="search"
                        placeholder="Искать товары…"
                        :class="$style.searchInput"
                    />
                    <button
                        type="submit"
                        :class="$style.searchButton"
                        aria-label="Найти"
                    >
                        <VIcon
                            name="search"
                            :size="20"
                        />
                    </button>
                </form>

                <nav
                    :class="$style.actions"
                    aria-label="Покупателю"
                >
                    <NuxtLink
                        to="/cart"
                        :class="$style.action"
                        aria-label="Корзина"
                    >
                        <VIcon name="cart" />
                    </NuxtLink>
                    <NuxtLink
                        to="/wishlist"
                        :class="$style.action"
                        aria-label="Избранное"
                    >
                        <VIcon name="heart" />
                    </NuxtLink>
                    <NuxtLink
                        :to="authStore.isAuthenticated ? '/lk' : '/login'"
                        :class="$style.action"
                        :aria-label="authStore.isAuthenticated ? 'Личный кабинет' : 'Войти'"
                    >
                        <VIcon name="user" />
                    </NuxtLink>
                </nav>
            </div>
        </div>

        <div :class="$style.bottom">
            <div :class="['container', $style.bottomInner]">
                <div :class="$style.bottomLeft">
                    <CategoryMenu :categories="siteStore.categories" />
                    <ul :class="$style.quickLinks">
                        <li
                            v-for="item in quickLinks"
                            :key="item.id"
                        >
                            <NuxtLink
                                :to="item.url"
                                :class="$style.quickLink"
                            >
                                <VIcon
                                    v-if="item.icon"
                                    :name="MENU_ICONS[item.icon] ?? item.icon"
                                />
                                {{ item.title }}
                            </NuxtLink>
                        </li>
                    </ul>
                </div>
                <a
                    v-if="settings?.phone"
                    :href="phoneHref"
                    :class="$style.phone"
                >
                    <VIcon name="phone" />
                    <span :class="$style.phoneNumber">{{ settings.phone }}</span>
                </a>
            </div>
        </div>
    </header>
</template>

<style lang="scss" module>
    .TheHeader {
        position: relative;
        z-index: z(header);
    }

    .hidden {
        @include visually-hidden;
    }

    // Верхняя строка: приветствие и соцсети
    .top {
        background-color: color(secondary, 700);
        box-shadow: inset 0 -1px 0 rgb(255 255 255 / 16%);
        color: color(gray, 0);

        @include respond-below(md) {
            display: none;
        }
    }

    .topInner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 44px;
    }

    .welcome {
        @include typography(body-sm);
    }

    .follow {
        display: flex;
        align-items: center;
        gap: space(3);
    }

    .followLabel {
        @include typography(body-sm);
    }

    // Средняя строка: логотип, поиск, корзина/избранное/профиль
    .middle {
        background-color: color(secondary, 700);
    }

    .middleInner {
        display: grid;
        grid-template-columns: auto auto;
        align-items: center;
        justify-content: space-between;
        gap: space(4);
        padding-top: space(4);
        padding-bottom: space(4);

        @include respond-to(md) {
            grid-template-columns: auto minmax(0, 646px) auto;
            gap: space(6);
            padding-top: space(5);
            padding-bottom: space(5);
        }
    }

    .search {
        position: relative;
        display: flex;
        grid-column: 1 / -1;
        order: 3;
        width: 100%;
        filter: drop-shadow(0 8px 16px rgb(0 0 0 / 8%));

        @include respond-to(md) {
            grid-column: auto;
            order: 0;
        }
    }

    .searchInput {
        width: 100%;
        height: 48px;
        padding: 0 space(12) 0 space(5);
        border-radius: radius(xs);
        border: none;
        background-color: color(gray, 0);
        font: inherit;
        color: color(gray, 900);

        @include typography(body-sm);

        &::placeholder {
            color: color(gray, 500);
        }

        &:focus {
            outline: 2px solid color(primary);
        }
    }

    .searchButton {
        @include reset-button;

        position: absolute;
        top: 50%;
        right: space(4);
        color: color(gray, 900);
        transform: translateY(-50%);

        @include focus-ring;
    }

    .actions {
        display: flex;
        gap: space(4);

        @include respond-to(md) {
            gap: space(6);
        }
    }

    .action {
        display: flex;
        color: color(gray, 0);
        transition: opacity $transition-fast;

        --icon-size: #{fluid(24px, 32px)};

        @include focus-ring(color(gray, 0));

        @include hover {
            opacity: 0.8;
        }
    }

    // Нижняя строка: каталог, быстрые ссылки, телефон
    .bottom {
        background-color: color(gray, 0);
        box-shadow: inset 0 -1px 0 color(gray, 100);
    }

    .bottomInner {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: space(6);
        padding-top: space(3);
        padding-bottom: space(3);

        @include respond-to(lg) {
            padding-top: space(4);
            padding-bottom: space(4);
        }
    }

    .bottomLeft {
        display: flex;
        align-items: center;
        gap: space(6);
    }

    .quickLinks {
        display: none;
        gap: space(6);

        @include reset-list;

        @include respond-to(lg) {
            display: flex;
        }
    }

    .quickLink,
    .phone {
        display: flex;
        align-items: center;
        gap: space(1.5);
        transition: color $transition-fast;

        @include focus-ring;
    }

    .quickLink {
        color: color(gray, 600);

        @include typography(body-sm);

        @include hover {
            color: color(gray, 900);
        }
    }

    .phone {
        white-space: nowrap;
        color: color(gray, 900);

        @include typography(body-md);

        @include respond-to(lg) {
            @include typography(body-lg);
        }

        @include hover {
            color: color(primary);
        }
    }

    // На телефоне — только иконка-звонилка, номер остаётся для скринридеров
    .phoneNumber {
        @include respond-below(sm) {
            @include visually-hidden;
        }
    }
</style>
