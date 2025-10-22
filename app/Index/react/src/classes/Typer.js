export class Typer {
    type() {
        let interval1 = setInterval(() => {
            if (this.el.innerText.length > 0)
                this.el.innerText = this.el.innerText.slice(0, -1);
            else if (this.el.innerText.length === 0) {
                clearInterval(interval1);
                let str = this.tog.get();
                let count = 0;
                let interval2 = setInterval(() => {
                    count++;
                    if (count <= str.length)
                        this.el.innerText = str.slice(0, count);
                    else
                        clearInterval(interval2);
                }, this.lag);
            }
        }, this.lag);
        return;
    }
    constructor(el, tog, sec = 4000, lag = 75) {
        this.el = el;
        this.tog = tog;
        this.lag = lag;
        this.interval = setInterval(() => {
            this.type();
        }, sec);
        return;
    }
}
