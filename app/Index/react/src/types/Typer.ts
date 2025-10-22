import { Toggler } from "../Toggler";

export class Typer {

	private el: HTMLElement;
	public tog: Toggler;
	private lag: number;

	private interval: number;

	private type (): void {
		let interval1: number = setInterval(() => {
			if (this.el.innerText.length > 0) this.el.innerText = this.el.innerText.slice(0, -1);
			else if (this.el.innerText.length === 0) {
				clearInterval(interval1);
				let str: string = this.tog.get();
				let count: number = 0;
				let interval2 = setInterval(() => {
					count ++;
					if (count <= str.length) this.el.innerText = str.slice(0, count);
					else clearInterval(interval2);
				}, this.lag);
			}
		}, this.lag)
		
		return;
	}

	constructor (el: HTMLElement, tog: Toggler, sec: number = 4000, lag: number = 75) {
		this.el = el;
		this.tog = tog;
		this.lag = lag;
		this.interval = setInterval(() => {
			this.type();
		}, sec)
		return;
	}

}