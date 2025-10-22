export class Toggler {

	private inner: string[] = [""];

	private point: number = 0;

	constructor(tips: string[]) {
		this.inner = tips;
	}

	get (): string{
		if (this.point < this.inner.length) return this.inner[this.point++];
		this.point = 1;
		return this.inner[0];
	}

	upload (tips: string[]): void{
		this.inner = tips;
		this.point = 0;
	}

}