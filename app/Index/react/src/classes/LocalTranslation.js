export class LocalTranslation {
    constructor(data) {
        this.HERO_TIPS = [""];
        this.HERO_BTN = "";
        this.DESC_TITLE = "";
        this.DESC_INNER = "";
        this.WHATS_TITLE = "";
        this.WHATS_DESC = "";
        this.FIND = "";
        this.HOME = "";
        this.PROJECTS = "";
        this.ABOUT = "";
        this.CONTACT = "";
        if (data)
            Object.assign(this, data);
        LocalTranslation.listener();
    }
    static value(data) {
        if (!LocalTranslation.instance)
            LocalTranslation.instance = new LocalTranslation(data);
        else if (data) {
            Object.assign(LocalTranslation.instance, data);
            this.listener();
        }
        return LocalTranslation.instance;
    }
    static listener(OldVal, newVal) {
        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.getAttribute('data-i18n');
            if (this.instance && key && typeof this.instance[key] == "string")
                el.textContent = this.instance[key]?.toString();
        });
        if (window.hero_tips)
            window.hero_tips.tog.upload(this.instance.HERO_TIPS);
    }
}
