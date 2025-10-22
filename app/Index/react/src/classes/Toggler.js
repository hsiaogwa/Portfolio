export class Toggler {
    constructor(tips) {
        this.inner = [""];
        this.point = 0;
        this.inner = tips;
    }
    get() {
        if (this.point < this.inner.length)
            return this.inner[this.point++];
        this.point = 1;
        return this.inner[0];
    }
    upload(tips) {
        this.inner = tips;
        this.point = 0;
    }
}
