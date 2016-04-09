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
