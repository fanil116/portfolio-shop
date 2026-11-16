<script setup lang="ts">
    import type { BadgeTone } from '~/components/ui/VBadge.vue';
    import type { IProductCard } from '~/repository/modules/catalog/types';

    import VBadge from '~/components/ui/VBadge.vue';
    import VButton from '~/components/ui/VButton.vue';
    import VIcon from '~/components/ui/VIcon.vue';
    import VPrice from '~/components/ui/VPrice.vue';
    import VRating from '~/components/ui/VRating.vue';

    const props = withDefaults(
        defineProps<{
            product: IProductCard;
            /** grid — плитка в сетке, featured — крупная с описанием, row — строка в колонке */
            variant?: 'grid' | 'featured' | 'row';
            showRating?: boolean;
        }>(),
        { variant: 'grid', showRating: false }
    );

    const BADGE_LABELS: Record<string, string> = {
        hot: 'Хит',
        sale: 'Распродажа',
        best_deal: 'Лучшая цена',
        new: 'Новинка',
    };

    const url = computed(() => `/product/${props.product.slug}`);

    const badges = computed(() => {
        const list: { tone: BadgeTone; text: string }[] = [];
        if (!props.product.in_stock) {
            list.push({ tone: 'sold', text: 'Нет в наличии' });
        }
        if (props.product.discount_percent) {
            list.push({ tone: 'discount', text: `−${props.product.discount_percent}%` });
        }
        if (props.product.badge) {
            list.push({ tone: props.product.badge, text: BADGE_LABELS[props.product.badge] ?? '' });
        }
        // В плитке места на одну плашку, в крупной карточке — на все
        return props.variant === 'featured' ? list : list.slice(0, 1);
    });
</script>

<template>
    <article :class="[$style.ProductCard, $style[`_${variant}`]]">
        <div :class="$style.media">
            <img
                v-if="product.image"
                :src="product.image"
                :alt="product.name"
                :class="$style.image"
                loading="lazy"
                decoding="async"
            />
            <div
                v-if="variant !== 'row' && badges.length"
                :class="$style.badges"
            >
                <VBadge
                    v-for="badge in badges"
                    :key="badge.tone"
                    :tone="badge.tone"
                >
                    {{ badge.text }}
                </VBadge>
            </div>
            <div
                v-if="variant === 'grid'"
                :class="$style.overlay"
            >
                <NuxtLink
                    v-for="action in ['heart', 'cart', 'eye']"
                    :key="action"
                    :to="url"
                    :class="$style.overlayButton"
                    tabindex="-1"
                    aria-hidden="true"
                >
                    <VIcon :name="action" />
                </NuxtLink>
            </div>
        </div>

        <div :class="$style.body">
            <VRating
                v-if="showRating || variant === 'featured'"
                :rating="product.rating"
                :count="product.reviews_count"
            />
            <!-- Ссылка растянута на всю карточку через :after — кликабельна вся плитка -->
            <NuxtLink
                :to="url"
                :class="$style.name"
            >
                {{ product.name }}
            </NuxtLink>
            <VPrice
                :price="product.price"
                :old-price="product.old_price"
                :size="variant === 'featured' ? 'md' : 'sm'"
            />
        </div>

        <div
            v-if="variant === 'featured'"
            :class="$style.footer"
        >
            <VButton
                :to="url"
                icon="cart"
                :class="$style.buy"
            >
                В корзину
            </VButton>
        </div>
    </article>
</template>

<style lang="scss" module>
    .ProductCard {
        position: relative;
        display: flex;
        flex-direction: column;
        gap: space(3);
        padding: space(4);
        border: 1px solid color(gray, 100);
        background-color: color(gray, 0);
        transition: box-shadow $transition-base;

        @include hover {
            box-shadow: $shadow-card-hover;
        }
    }

    .media {
        position: relative;
        overflow: hidden;
        aspect-ratio: 216 / 188;
    }

    .image {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    .badges {
        position: absolute;
        top: 0;
        left: 0;
        z-index: z(badge);
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: space(2);
    }

    // Затемнение с кнопками появляется при наведении на плитку
    .overlay {
        position: absolute;
        inset: 0;
        z-index: z(overlay);
        display: none;
        align-items: center;
        justify-content: center;
        gap: space(2);
        background-color: rgb(0 0 0 / 20%);
        opacity: 0;
        transition: opacity $transition-base;

        @media (hover: hover) and (pointer: fine) {
            display: flex;

            .ProductCard:hover & {
                opacity: 1;
            }
        }
    }

    .overlayButton {
        display: flex;
        padding: space(3);
        border-radius: radius(round);
        background-color: color(gray, 0);
        color: color(gray, 900);
        transition:
            background-color $transition-fast,
            color $transition-fast;

        @include hover {
            background-color: color(primary);
            color: color(gray, 0);
        }
    }

    .body {
        display: flex;
        flex-direction: column;
        gap: space(2);
    }

    .name {
        color: color(gray, 900);

        @include typography(body-sm);
        @include line-clamp(2);
        @include focus-ring;

        &:after {
            content: '';
            position: absolute;
            inset: 0;
        }
    }

    // Кнопки поверх растянутой ссылки
    .overlay,
    .footer {
        z-index: z(overlay);
    }

    // Крупная карточка: рейтинг, цена крупнее, кнопка «В корзину»
    ._featured {
        gap: space(6);
        padding: space(6);

        .name {
            @include typography(body-md);
        }

        .media {
            aspect-ratio: 1;
        }
    }

    .footer {
        position: relative;
        margin-top: auto;
    }

    .buy {
        width: 100%;
    }

    // Строка: картинка 80px слева, текст справа
    ._row {
        flex-direction: row;
        align-items: center;
        padding: space(3);
        border-radius: radius(sm);

        .media {
            flex-shrink: 0;
            width: 80px;
            aspect-ratio: 1;
        }
    }
</style>
