export class Item {
    ["constructor"](jsonfile, item) {
        fetch(jsonfile).then(res => res.json()).then(data => {
            if (item) {
                this.id = item;
                Object.assign(this, data[item]);
            }
            else
                Object.assign(this, data);
        });
    }
    constructor(jsonobj, id) {
        this.coworkers = [];
        this.langs = [];
        if (id)
            this.id = id;
        Object.assign(this, jsonobj);
    }
    /**
     * createNode
     */
    createNode() {
        let el = document.createElement("div");
        let tmp;
        el.classList.add(...["card", "item"]);
        if (this.link)
            el.addEventListener("click", () => window.location.href = `${this.link}`);
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
            let tmptmp;
            tmptmp = document.createElement("small");
            tmptmp.textContent = `${this.auth} | ${this.coworkers}`;
            tmp.appendChild(tmptmp);
        }
        el.appendChild(tmp);
        tmp = document.createElement("div");
        {
            let tmptmp;
            tmptmp = document.createElement("small");
            tmptmp.textContent = ``;
            tmp.appendChild(tmptmp);
        }
        el.appendChild(tmp);
        // buttons
        tmp = document.createElement("div");
        tmp.classList.add(...["button", "set"]);
        {
            let tmptmp;
            tmptmp = document.createElement("button");
            if (this.link)
                tmptmp.addEventListener("click", () => window.location.href = `${this.link_outside}`);
            else
                tmptmp.classList.add("disabled");
            tmp.appendChild(tmptmp);
        }
        {
            let tmptmp;
            tmptmp = document.createElement("button");
            if (this.link_outside)
                tmptmp.addEventListener("click", () => window.location.href = `${this.link_outside}`);
            else
                tmptmp.classList.add("disabled");
            tmp.appendChild(tmptmp);
        }
        el.appendChild(tmp);
        return el;
    }
}
