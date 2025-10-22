export interface RefBase<T> {

	get(): T;

	set(data?: Partial<T>): void;

	listener(oldVal?: T, newVal?: T): void;

}