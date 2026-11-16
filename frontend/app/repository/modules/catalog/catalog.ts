import type { ICategoryNode } from './types';

import HttpFactory from '~/repository/factory';

export default class CatalogModule extends HttpFactory {
    categoryTree(): Promise<ICategoryNode[]> {
        return this.call<ICategoryNode[]>('GET', '/api/catalog/categories/');
    }
}
