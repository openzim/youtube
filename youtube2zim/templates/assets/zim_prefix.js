
/* Generic Zimwriterfs-related properties */
function isInZIM() { return document.getElementById("favicon").getAttribute("href").indexOf("/I/") !== -1; }
IS_IN_ZIM = isInZIM();

function getImageNamespacePrefix() { return document.getElementById("favicon").getAttribute("href").replace("profile.jpg", ""); }
ZIM_IMG_NS = getImageNamespacePrefix();

function getMetaNamespacePrefix() { return ZIM_IMG_NS.replace("/I/", "/-/"); }
ZIM_META_NS = getMetaNamespacePrefix();

function hasImageNamespacePrefix(target) { return target.indexOf(ZIM_IMG_NS) !== -1;}
function hasMetaNamespacePrefix(target) { return target.indexOf(ZIM_META_NS) !== -1;}
function changeNamespacePrefix(target, new_ns) {
	let avail_ns = ["A", "-", "I"];
	new_ns = new_ns.toUpperCase();
	if (avail_ns.indexOf(new_ns) == -1) {
		throw ("Invalid NS: " + new_ns);
	}
	let ns_char = -1;
	avail_ns.forEach(function (namespace) {
		if (ns_char == -1) {
			ns_char = target.indexOf("/" + namespace + "/");
		}
	});
	if (ns_char == -1) {
		// missing prefix
		return target;
	}

	return target.slice(0, ns_char + 1) + new_ns + target.slice(ns_char + 2);
}

/* ogv.js related bits */
function zim_fix_wasm_target(target) {
	console.log("zim_fix_wasm_target:", target);
	if (!IS_IN_ZIM) {
		console.log("..not in zim");
		return target;
	}
	if (hasImageNamespacePrefix(target)) {
		// we already have a good path, leave it
	}
	else if (hasMetaNamespacePrefix(target)) {
		// we have a prefix, just replace it
		target = changeNamespacePrefix(target, "I");
	}
	else {
		// we lack the prefix, add it
		target = ZIM_IMG_NS + "assets/ogvjs/" + target;
	}
	console.log("..target:", target);
	return target;
}
