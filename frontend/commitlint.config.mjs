export default {
    extends: ['@commitlint/config-conventional'],
    rules: {
        // Описание коммита пишем по-русски, поэтому регистр не ограничиваем
        'subject-case': [0],
    },
};
