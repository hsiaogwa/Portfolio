export class Ref {
    value(data) {
        if (data) {
            this.__value.set(data);
            this.__value.listener();
        }
        return this.__value.get();
    }
}
