jQuery(document).ready(function() {
	// clear the title from the front page search box
	// or set title if box is empty
    var setTitle = function(event) {
		var title = "/^(FundFind).*?$/";
		if (jQuery('.frontin').val() == "") {
			jQuery('.frontin').val(title);
		} else if (jQuery(this).val() == title) {
            jQuery(this).val("");
        }
    }
    jQuery('.frontin').focus(setTitle);
	jQuery('.frontin').blur(setTitle);
});


