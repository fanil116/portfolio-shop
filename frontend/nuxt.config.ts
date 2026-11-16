const isDev = process.env.NODE_ENV === 'development';

// Куда ходят SSR-запросы и dev-прокси: локально — backend на :8000, в docker — http://backend:8000
const apiInternalUrl = process.env.NUXT_API_INTERNAL_URL || 'http://localhost:8000';

// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
    modules: ['@pinia/nuxt', '@nuxt/eslint'],

    devtools: { enabled: isDev },

    telemetry: { enabled: false },

    app: {
        head: {
            htmlAttrs: { lang: 'ru' },
            title: 'Clicon — магазин электроники',
            meta: [{ name: 'viewport', content: 'width=device-width, initial-scale=1' }],
            link: [
                { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
                { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
                {
                    rel: 'stylesheet',
                    href: 'https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap',
                },
            ],
        },
    },

    css: ['~/assets/scss/default.scss'],

    runtimeConfig: {
        // Переопределяется переменной окружения NUXT_API_INTERNAL_URL
        apiInternalUrl,
    },

    // В dev браузер ходит в /api и /admin через Nuxt — один origin, cookie сессии работают.
    // В production эти пути до Nuxt не доходят: их забирает nginx.
    nitro: {
        devProxy: {
            '/api': { target: `${apiInternalUrl}/api`, changeOrigin: false },
            '/admin': { target: `${apiInternalUrl}/admin`, changeOrigin: false },
            '/s': { target: `${apiInternalUrl}/s`, changeOrigin: false },
            '/m': { target: `${apiInternalUrl}/m`, changeOrigin: false },
        },
    },

    router: {
        options: {
            linkActiveClass: '_active-link',
            linkExactActiveClass: '_exact-link',
        },
    },

    vite: {
        css: {
            preprocessorOptions: {
                scss: {
                    // Токены, функции и миксины доступны в каждом <style lang="scss">
                    additionalData: '@use "~/assets/scss/shared" as *;',
                },
            },
        },
    },

    typescript: {
        strict: true,
    },

    compatibilityDate: '2026-07-08',
});
