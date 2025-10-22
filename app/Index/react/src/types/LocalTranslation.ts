import { Typer } from "../Typer";

declare global {
	interface Window {
		hero_tips: Typer;
	}
}

export class LocalTranslation {
	// text
	[key: string]: string | string[];
	public HERO_TIPS: string[] = [""];
	private HERO_BTN: string = "";
	private DESC_TITLE: string = "";
	private DESC_INNER: string = "";
	private WHATS_TITLE: string = "";
	private WHATS_DESC: string = "";
	private FIND: string = "";
	private HOME: string = "";
	private PROJECTS: string = "";
	private ABOUT: string = "";
	private CONTACT: string = "";

	private static instance: LocalTranslation;
	
	private constructor(data?: Partial<LocalTranslation>) {
		if (data) Object.assign(this, data);
		LocalTranslation.listener();
	}

    public static value(data?: Partial<LocalTranslation>): LocalTranslation {
        if (!LocalTranslation.instance) LocalTranslation.instance = new LocalTranslation(data);
        else if (data) {
            Object.assign(LocalTranslation.instance, data);
			this.listener();
        }
        return LocalTranslation.instance;
    }

	private static listener(OldVal?: LocalTranslation, newVal?: LocalTranslation) {
		document.querySelectorAll('[data-i18n]').forEach(el => {
      		const key = el.getAttribute('data-i18n');
      		if (this.instance && key && typeof this.instance[key] == "string") el.textContent = this.instance[key]?.toString();
    	});
		if (window.hero_tips) window.hero_tips.tog.upload(this.instance.HERO_TIPS)
	}
}
