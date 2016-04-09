$.tablesorter.addParser({
	id: "eudate",
	is: function(s) {
		return /\d{1,2}\.\d{1,2}\.\d{2,4}/.test(s);
	},
	format: function(s,table) {
		s = s.replace(/\-/g,"/");
		s = s.replace(/(\d{1,2})[\/\.](\d{1,2})[\/\.](\d{4})/, "$3/$2/$1");
		return $.tablesorter.formatFloat(new Date(s).getTime());
	},
	type: "numeric"
 });
$.tablesorter.addParser({
	id: "currency",
	is: function(s) {
		return false; // no autodetection
	},
	format: function(s,table) {
		s = s.replace(/€/g,"");
		return s
	},
	type: "numeric"
 });
