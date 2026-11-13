export interface IUser {
    id: number;
    email: string;
    first_name: string;
    last_name: string;
}

export interface ILoginPayload {
    email: string;
    password: string;
}

export interface IRegisterPayload extends ILoginPayload {
    first_name?: string;
    last_name?: string;
}

export type IProfilePayload = Partial<Pick<IUser, 'first_name' | 'last_name'>>;
