function conditionalInput(cond, inp) {
	if (!$(cond).prop("checked")) {
		$(inp).css("display","none");
	}
	$(cond).change(function () {
		if ($(this).prop("checked")) {
			$(inp).show(400);
		}
		else {
			$(inp).hide(400);
		}
	});
}

function setConferenceYear(year) {
	$.post("/setYear/"+year, function () {
		location.reload();
	}).fail(function () {
		alert("Unable to set conference year to " + year);
	});
}
