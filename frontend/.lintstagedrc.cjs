module.exports = {
    '*.(ts|js|mjs|vue|scss|css|json)': ['prettier --write'],
    '*.(ts|js|mjs|vue)': ['eslint --cache'],
    '*.(scss|vue)': ['stylelint --allow-empty-input'],
};
