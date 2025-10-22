import { Toggler, LocalTranslation, Typer } from "./src/classes/index.js";

//****events****
//click event
window.switchLang = lang => {
	fetch(`./lang/${lang}.lang`).then(
		res => res.json()
	).then(
		data => LocalTranslation.value(data)
	);
	document.getElementById("lang_selector").classList.add("show-never");
};

//onload event
const portalyOnload = () => {
	let el = document.getElementById("portaly");
	const innerDoc = el.contentDocument || el.contentWindow.document;
    el.style.height = innerDoc.body.scrollHeight + "px";
	console.log("portaly loaded");
};
// document.getElementById("portaly").addEventListener("load", portalyOnload);
console.log("portaly listener added");

//language i18n
fetch("./lang/US.lang").then(
	res => res.json()
).then(
	data => {
		LocalTranslation.value(data);
		fetch("./lang").then(
			res => res.json()
		).then(
			data => LocalTranslation.value(data)
		)
	}
);

//load img    lazy
const loadBg = el => {
	const src = el.getAttribute('data-icon-src');
	if (!src) return;
	el.style.backgroundImage = `url("${src}")`;
	el.removeAttribute('data-icon-src');
};
window.onload = () => {
	if ('IntersectionObserver' in window) {
		const io = new IntersectionObserver(entries => {
			entries.forEach(entry => {
				if (entry.isIntersecting) {
					loadBg(entry.target);
					io.unobserve(entry.target);
				}
			});
		}, { rootMargin: '200px' }); // 提前 200px 預載
		document.querySelectorAll('[data-icon-src]').forEach(el => io.observe(el));
	} else {
		// 後備方案：不支援 IO 的瀏覽器直接載入
		document.querySelectorAll('[data-icon-src]').forEach(loadBg);
	}
};

//****load for inner_text****
//load langlist
fetch("./lang/lang.config").then(
	res => res.json()
).then(
	data => {
		let ol = document.getElementById("lang_selector");
		for (const code in data) {
			let li = document.createElement("li");
			li.appendChild(document.createTextNode(data[code]));
			li.setAttribute("onclick", `switchLang("${code}")`);
			ol.appendChild(li);
		}
	}
)

//load Items
fetch("/item").then(
	res => res.json()
).then(
	data => {
		//
	}
)

//load typer
window.hero_tips = new Typer(
	document.getElementById("togtip"),
	new Toggler(LocalTranslation.value().HERO_TIPS)
);