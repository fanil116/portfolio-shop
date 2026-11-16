import type { IHome, ISite } from './types';

import HttpFactory from '~/repository/factory';

export default class ContentModule extends HttpFactory {
    site(): Promise<ISite> {
        return this.call<ISite>('GET', '/api/site/');
    }

    home(): Promise<IHome> {
        return this.call<IHome>('GET', '/api/home/');
    }

    async subscribe(email: string): Promise<void> {
        await this.call<unknown>('POST', '/api/newsletter/subscribe/', { email });
    }
}
