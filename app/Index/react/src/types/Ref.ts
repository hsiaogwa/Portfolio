import { RefBase } from "../RefBase";

export class Ref<RefValue> {

	private __value: RefBase<RefValue>;

	public value(data?: Partial<RefValue>):RefValue {
		if (data) {
			this.__value.set(data);
			this.__value.listener();
		}
		return this.__value.get();
	}
}