export class Item {

	public index: number;
	private id: string;
	private link?: string;
	private link_outside?: string;
	private auth: string;
	private like?: number;
	private shortcut?: string;
	private coworkers: string[] = [];
	private langs?: string[] = [];

	["constructor"] (jsonfile: string, item?: string) {
		fetch(jsonfile).then(res => res.json()).then(
			data => {
				if (item) {
					this.id = item;
					Object.assign(this, data[item]);
				}
				else Object.assign(this, data);
			}
		)
	}

	constructor (jsonobj: Partial<Item>, id?: string) {
		if (id) this.id = id;
		Object.assign(this, jsonobj);
	}

	/**
	 * createNode
	 */
	public createNode(): HTMLDivElement {
		let el: HTMLDivElement = document.createElement("div");
		let tmp: HTMLElement;
		el.classList.add(...["card", "item"]);
		if (this.link) el.addEventListener("click", () => window.location.href = `${this.link}`);
		// icon photo
		tmp = document.createElement("icon");
		tmp.setAttribute("data-icon-src", `public/${this.shortcut ? this.shortcut : "undefined"}`);
		el.appendChild(tmp);
		// title
		tmp = document.createElement("h2");
		tmp.setAttribute("data-i18n", `ITEM_TITLE_${this.id}`);
		el.appendChild(tmp);
		// description
		tmp = document.createElement("p");
		tmp.setAttribute("data-i18n", `ITEM_DESC_${this.id}`);
		el.appendChild(tmp);
		// infomation (small font size)
		tmp = document.createElement("div");
		{
			let tmptmp: HTMLElement;
			tmptmp = document.createElement("small");
			tmptmp.textContent = `${this.auth} | ${this.coworkers}`;
			tmp.appendChild(tmptmp);
		}
		el.appendChild(tmp);
		tmp = document.createElement("div");
		{
			let tmptmp: HTMLElement;
			tmptmp = document.createElement("small");
			tmptmp.textContent = ``;
			tmp.appendChild(tmptmp);
		}
		el.appendChild(tmp);
		// buttons
		tmp = document.createElement("div");
		tmp.classList.add(...["button", "set"]);
		{
			let tmptmp: HTMLButtonElement;
			tmptmp = document.createElement("button");
			tmptmp.setAttribute("data-i18n", `ITEM_BUTTON_INFO`);
			if (this.link) tmptmp.addEventListener("click", () => window.location.href = `${this.link}`);
			else tmptmp.classList.add("disabled");
			tmp.appendChild(tmptmp);
		} {
			let tmptmp: HTMLButtonElement;
			tmptmp = document.createElement("button");
			tmptmp.setAttribute("data-i18n", `ITEM_BUTTON_OUTSIDE`);
			if (this.link_outside) tmptmp.addEventListener("click", () => window.location.href = `${this.link_outside}`);
			else tmptmp.classList.add("disabled");
			tmp.appendChild(tmptmp);
		}
		el.appendChild(tmp);
		return el;
	}

}