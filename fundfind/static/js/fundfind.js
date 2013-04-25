jQuery(document).ready(function() {
// All of these will run for ANY page.
/* There is very little possibility that any pages will break due to the class
 * names used (specific enough). Where the selectors are more general, this is
 * intentional - the point is to enable quick and easy re-use of code. If a
 * "Tags" field is needed then it will likely need an "add more" [tags] button
 * no matter which page it is on. Copying the relevant HTML is all which will
 * be necessary since the code below runs for all pages.
 */ 
	
	// "add more" button for Useful links
	$('#more_links').click( function () {
        
        // Insert a copy of the useful link <input> tag right before the 
		// "add more" button.
		// getOuterHTML is a homebrew f(), not a jQuery one!
        $('#useful_links_group').append(getOuterHTML('.useful-link'));
        
		return false; // prevent form submission
	});
    
});

function getOuterHTML(selector) {
    /* There is no easy way to get the outerHTML of an element in jQuery.
     * This is needed since we want to duplicate the useful link <input>.
     * The code below does .clone().wrap('<p>').parent().html()
     *
     * The way it works is that it takes the first element with a certain
     * class, makes a clone of it in RAM, wraps with a P tag, gets the parent 
     * of it (meaning the P tag), and then gets the innerHTML property of that.
     * So we end up copying the element we just selected, which is our goal.
     
     * The clone() means we're not actually disturbing the DOM. Without it
     * all elements with a certain class will be wrapped in a P tag which is
     * undesirable.
     */
	return $(selector).clone().wrap('<p>').parent().html();
}

function use_slugify(on_which_field) {
	/* Generate short titles automatically from the passed-in input field.
	 * This is just a visualisation for the user using the server's slugify function.
	 * This gets thrown away of course (guard against malformed or crafted requests).
	 * The server will just use its slugify functionality on the field when 
	 * processing the form.
	 */
	
	$('input[name=' + on_which_field + ']').keyup( function() {
		// prepare for AJAX request
		var slugify_svc_url = 'slugify';
		var slugify_request_data = {make_into_slug: $(this).val()};
		var slugify_success = function(slug) {
			$('input[name=unique_' + on_which_field + ']').val(slug);
		};
		
		$.post(slugify_svc_url, slugify_request_data, slugify_success);
	});
}

function add_more_expand_field(to_which_field) {
	// "add more" button functionality for tags and similar fields which just
    // expand instead of creating more fields
	$( '#more_' + to_which_field ).click( function () {
		var curwidth = $( '#' + to_which_field ).width();
		/* Another 100 pixels should be good on most devices and the user
		 * shouldn't even have to click the "add more" button again, but
		 * they can if they want to - so 100 should be a good increment.
		 */
		$( '#' + to_which_field ).width(curwidth + 100);
		return false; // prevent form submission
	});
}
