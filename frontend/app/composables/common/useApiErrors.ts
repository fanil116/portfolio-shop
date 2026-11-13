import { FetchError } from 'ofetch';

const CSRF_FAILED_PREFIX = 'CSRF Failed';

/**
 * Собирает все строки из ответа DRF: ошибки полей, non_field_errors, detail,
 * в том числе вложенные ({ address: { city: ['...'] } }) и списки объектов.
 */
function collectMessages(value: unknown): string[] {
    if (typeof value === 'string') {
        return [value];
    }
    if (Array.isArray(value)) {
        return value.flatMap(collectMessages);
    }
    if (value && typeof value === 'object') {
        return Object.values(value).flatMap(collectMessages);
    }
    return [];
}

/**
 * Превращает ошибку запроса к API в текст для формы.
 */
export function getApiErrorMessage(error: unknown): string {
    if (error instanceof FetchError) {
        if (error.status === 429) {
            return 'Слишком много попыток. Попробуйте через минуту.';
        }

        const messages = collectMessages(error.data);

        if (messages.some((message) => message.startsWith(CSRF_FAILED_PREFIX))) {
            return 'Сессия устарела. Обновите страницу и попробуйте снова.';
        }
        if (messages.length) {
            return messages.join(' ');
        }
    }

    console.error('[api] необработанная ошибка', error);
    return 'Не удалось выполнить запрос. Попробуйте позже.';
}
