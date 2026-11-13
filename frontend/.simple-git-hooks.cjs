const path = require('path');

// Хуки ставятся в корень репозитория, поэтому пути до frontend/backend — абсолютные
const frontendDir = path.resolve(__dirname).replace(/\\/g, '/');
const backendDir = path.resolve(__dirname, '../backend').replace(/\\/g, '/');

module.exports = {
    'pre-commit': [
        `cd "${frontendDir}" && ./node_modules/.bin/lint-staged -c .lintstagedrc.cjs`,
        `cd "${backendDir}" && uv run ruff check . && uv run ruff format --check .`,
    ].join(' && '),
    'commit-msg': `cd "${frontendDir}" && ./node_modules/.bin/commitlint --config ./commitlint.config.mjs --edit "$1"`,
};
