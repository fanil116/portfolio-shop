export interface ICountdownParts {
    days: number;
    hours: number;
    minutes: number;
    seconds: number;
}

const SECOND = 1000;
const MINUTE = 60 * SECOND;
const HOUR = 60 * MINUTE;
const DAY = 24 * HOUR;

function split(ms: number): ICountdownParts {
    const rest = Math.max(ms, 0);
    return {
        days: Math.floor(rest / DAY),
        hours: Math.floor((rest % DAY) / HOUR),
        minutes: Math.floor((rest % HOUR) / MINUTE),
        seconds: Math.floor((rest % MINUTE) / SECOND),
    };
}

/**
 * Обратный отсчёт до даты. Тикает только на клиенте: на сервере и до гидрации
 * значение null, чтобы разметка SSR и клиента совпадала.
 */
export function useCountdown(endsAt: MaybeRefOrGetter<string | null>) {
    const now = ref<number | null>(null);
    let timer: ReturnType<typeof setInterval> | undefined;

    const parts = computed<ICountdownParts | null>(() => {
        const target = toValue(endsAt);
        if (now.value === null || !target) {
            return null;
        }
        return split(new Date(target).getTime() - now.value);
    });

    const isFinished = computed(() => {
        const value = parts.value;
        return value !== null && Object.values(value).every((part) => part === 0);
    });

    onMounted(() => {
        now.value = Date.now();
        timer = setInterval(() => {
            now.value = Date.now();
            if (isFinished.value) {
                clearInterval(timer);
            }
        }, SECOND);
    });
    onBeforeUnmount(() => clearInterval(timer));

    return { parts, isFinished };
}
