// @ts-check
import eslintConfigPrettier from 'eslint-config-prettier/flat';
import eslintPluginPrettierRecommended from 'eslint-plugin-prettier/recommended';
import simpleImportSort from 'eslint-plugin-simple-import-sort';

import withNuxt from './.nuxt/eslint.config.mjs';

export default withNuxt(
    eslintPluginPrettierRecommended,
    eslintConfigPrettier,
    {
        files: ['app/**/*.{js,ts,mjs,vue}'],
        rules: {
            'no-restricted-imports': [
                'error',
                {
                    patterns: [
                        {
                            group: ['../**'],
                            message:
                                'Импорты через ../ в app/ запрещены. Используйте ~/...; ./ — только внутри своей папки.',
                        },
                    ],
                },
            ],
        },
    },
    {
        plugins: {
            'simple-import-sort': simpleImportSort,
        },
        rules: {
            complexity: ['error', { max: 10 }],
            'max-lines': ['error', 700],
            'no-console': ['error', { allow: ['info', 'warn', 'error'] }],
            'no-debugger': 'error',
            'no-eval': 'error',
            'no-implicit-coercion': 'error',
            'no-return-await': 'error',
            'no-useless-return': 'error',
            'one-var': ['error', 'never'],
            radix: 'error',
            '@typescript-eslint/no-explicit-any': 'error',
            '@typescript-eslint/no-unused-vars': 'error',
            'vue/multi-word-component-names': 'off',
            'vue/no-v-html': 'error',
            'vue/component-definition-name-casing': ['error', 'PascalCase'],
            'vue/padding-line-between-blocks': 'error',
            'simple-import-sort/imports': [
                'error',
                {
                    groups: [
                        // Type-импорты
                        ['^.*\\u0000$'],
                        // Node built-ins
                        ['^node:'],
                        // npm-пакеты
                        ['^@?\\w'],
                        // Виртуальные модули Nuxt (#app, #imports)
                        ['^#'],
                        // Store, components, composables, repository, types
                        ['^~/store/'],
                        ['^~/components/'],
                        ['^~/composables/'],
                        ['^~/repository/'],
                        ['^~/types/'],
                        // Прочие пути проекта
                        ['^~/', '^~~/'],
                        // Относительные
                        ['^\\./'],
                    ],
                },
            ],
            'simple-import-sort/exports': 'error',
        },
    }
);
