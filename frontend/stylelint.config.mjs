// @ts-check
import { readFileSync } from 'node:fs';

// Функции дизайн-системы (color, space, fluid…) берутся прямо из _functions.scss:
// новая @function сразу разрешена линтером, без ручного списка в конфиге.
// Приватные функции (с префиксом -) снаружи модуля недоступны и в список не попадают.
const functionsSource = readFileSync(
    new URL('./app/assets/scss/shared/_functions.scss', import.meta.url),
    'utf8'
);
const designSystemFunctions = [...functionsSource.matchAll(/@function\s+([a-z][\w-]*)/g)].map(
    ([, name]) => name
);

/** @type {import('stylelint').Config} */
export default {
    customSyntax: 'postcss-scss',
    overrides: [
        {
            files: ['**/*.vue'],
            customSyntax: 'postcss-html',
        },
    ],
    extends: ['stylelint-config-standard', 'stylelint-config-standard-scss'],
    plugins: ['stylelint-scss', 'stylelint-order'],
    rules: {
        'selector-class-pattern': null,
        'at-rule-no-unknown': null,
        'scss/at-rule-no-unknown': true,
        'declaration-no-important': true,
        'no-descending-specificity': null,
        'selector-pseudo-element-colon-notation': 'single',
        'order/properties-order': [
            'content',
            'position',
            'top',
            'right',
            'bottom',
            'left',
            'z-index',
            'box-sizing',
            'overflow',
            'display',
            'flex-direction',
            'flex-wrap',
            'align-items',
            'justify-content',
            'gap',
            'flex',
            'width',
            'min-width',
            'max-width',
            'height',
            'min-height',
            'max-height',
            'margin',
            'padding',
            'border-radius',
            'border',
            'background',
            'background-color',
            'outline',
            'text-align',
            'text-decoration',
            'font',
            'font-family',
            'font-size',
            'font-weight',
            'line-height',
            'color',
            'opacity',
            'transform',
            'transition',
            'cursor',
        ],
        'function-no-unknown': null,
        'scss/function-no-unknown': [
            true,
            { ignoreFunctions: ['v-bind', ...designSystemFunctions] },
        ],
    },
};
