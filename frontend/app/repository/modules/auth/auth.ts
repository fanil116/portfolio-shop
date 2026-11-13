import type { ILoginPayload, IProfilePayload, IRegisterPayload, IUser } from './types';

import HttpFactory from '~/repository/factory';

export default class AuthModule extends HttpFactory {
    private readonly base = '/api/auth';

    // Ответ 204 без тела — результат не нужен
    async csrf(): Promise<void> {
        await this.call<unknown>('GET', `${this.base}/csrf/`);
    }

    me(): Promise<IUser> {
        return this.call<IUser>('GET', `${this.base}/me/`);
    }

    updateProfile(payload: IProfilePayload): Promise<IUser> {
        return this.call<IUser>('PATCH', `${this.base}/me/`, payload);
    }

    login(payload: ILoginPayload): Promise<IUser> {
        return this.call<IUser>('POST', `${this.base}/login/`, payload);
    }

    register(payload: IRegisterPayload): Promise<IUser> {
        return this.call<IUser>('POST', `${this.base}/register/`, payload);
    }

    async logout(): Promise<void> {
        await this.call<unknown>('POST', `${this.base}/logout/`);
    }
}
