import { FetchError } from 'ofetch';

type FieldErrors = Record<string, string[] | string>;

/**
 * Превращает ошибку DRF в текст для формы: ошибки полей и non_field_errors.
 */
export function getApiErrorMessage(error: unknown): string {
    if (error instanceof FetchError) {
        if (error.status === 429) {
            return 'Слишком много попыток. Попробуйте через минуту.';
        }

        const data = error.data as FieldErrors | undefined;
        if (data && typeof data === 'object') {
            const messages = Object.values(data).flatMap((value) =>
                Array.isArray(value) ? value : [value]
            );
            if (messages.length) {
                return messages.join(' ');
            }
        }
    }

    console.error('[api] необработанная ошибка', error);
    return 'Не удалось выполнить запрос. Попробуйте позже.';
}
