
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

    // search for collection id similar to that provided, and warn of duplicates controlled by third parties
    var checkcoll = function(event) {
        jQuery.ajax({
            url: '/collections.json?q=id:"' + jQuery(this).val() + '"'
            , type: 'GET'
            , success: function(json, statusText, xhr) {
                if (json.records.length != 0) {
                    if (json.records[0]['owner'] != jQuery('#current_user').val()) {
                        if (jQuery('#collwarning').length == 0) {
                            var where = json.records[0]['owner'] + '/' + json.records[0]['id']
                            jQuery('#collection').after('&nbsp;&nbsp;<span id="collwarning" class="label warning"><a href="/' + where + '">sorry, in use</a>. Please change.</span>');
                        }
                    }
                } else {
                    jQuery('#collwarning').remove();
                }
            }
            , error: function(xhr, message, error) {
            }
        });
        
    }
    jQuery('#collection').bind('keyup',checkcoll);
	
});


