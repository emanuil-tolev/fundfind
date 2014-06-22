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
		$( '#' + to_which_field + '_container' ).width(curwidth + 120);
		$( '#' + to_which_field + '_description' ).addClass('controls');
		return false; // prevent form submission
	});
}

// facetview customisations
// pass in as render_search_options
function fvc_searchOptions(options) {
    /*****************************************
     * overrides must provide the following classes and ids
     *
     * class: facetview_startagain - reset the search parameters
     * class: facetview_pagesize - size of each result page
     * class: facetview_order - ordering direction of results
     * class: facetview_orderby - list of fields which can be ordered by
     * class: facetview_searchfield - list of fields which can be searched on
     * class: facetview_freetext - input field for freetext search
     *
     * should (not must) respect the following configs
     *
     * options.search_sortby - list of sort fields and directions
     * options.searchbox_fieldselect - list of fields search can be focussed on
     * options.sharesave_link - whether to provide a copy of a link which can be saved
     */
    
    // initial button group of search controls
    var thefacetview = '<div class="btn-group" style="display:inline-block; margin-right:5px;"> \
        <button type="button" class="btn btn-sm btn-default facetview_startagain" title="clear all search settings and start again" href=""><span class="glyphicon glyphicon-remove"></span></button> \
        <button type="button" class="btn btn-sm btn-default facetview_pagesize" title="change result set size" href="#"></a>';
        
    if (options.search_sortby.length > 0) {
        thefacetview += '<button type="button" class="btn btn-sm facetview_order" title="current order descending. Click to change to ascending" \
            href="desc"><span class="glyphicon glyphicon-arrow-down"></span></a>';
    }
    thefacetview += '</div>';
    
    // selection for search ordering
    if (options.search_sortby.length > 0) {
        thefacetview += '<select class="facetview_orderby" style="border-radius:5px; \
            -moz-border-radius:5px; -webkit-border-radius:5px; width:100px; background:#eee; margin:0 5px 21px 0; padding: 3px;"> \
            <option value="">order by ... relevance</option>';
        
        for (var each = 0; each < options.search_sortby.length; each++) {
            var obj = options.search_sortby[each];
            var sortoption = '';
            if ($.type(obj['field']) == 'array') {
                sortoption = sortoption + '[';
                sortoption = sortoption + "'" + obj['field'].join("','") + "'";
                sortoption = sortoption + ']';
            } else {
                sortoption = obj['field'];
            }
            thefacetview += '<option value="' + sortoption + '">' + obj['display'] + '</option>';
        };
        thefacetview += '</select>';
    }
    
    // select box for fields to search on
    if ( options.searchbox_fieldselect.length > 0 ) {
        thefacetview += '<select class="facetview_searchfield" style="border-radius:5px 0px 0px 5px; \
            -moz-border-radius:5px 0px 0px 5px; -webkit-border-radius:5px 0px 0px 5px; width:100px; margin:0 -2px 0px 0; background-color:inherit; \
            padding:6px; width: 33%;">';
        thefacetview += '<option value="">search everywhere</option>';
        
        for (var each = 0; each < options.searchbox_fieldselect.length; each++) {
            var obj = options.searchbox_fieldselect[each];
            thefacetview += '<option value="' + obj['field'] + '">' + obj['display'] + '</option>';
        };
        thefacetview += '</select>';
    };
    
    // text search box
    thefacetview += '<input type="text" class="facetview_freetext" style="border-radius:5px; \
        -moz-border-radius:5px; -webkit-border-radius:5px; \
        display:inline-block; width: 55%; margin:0 0 0 0; background-color:inherit; padding: 6px;" \
        name="q" value="" placeholder="search term" />';
    
    // share and save link
    if (options.sharesave_link) {
        thefacetview += '<a class="btn facetview_sharesave" title="share or save this search" style="margin:0 0 21px 5px;" href=""><i class="icon-share-alt"></i></a>';
        thefacetview += '<div class="facetview_sharesavebox alert alert-info" style="display:none;"> \
            <button type="button" class="facetview_sharesave close">×</button> \
            <p>Share or save this search:</p> \
            <textarea class="facetview_sharesaveurl" style="width:100%;height:100px;">' + shareableUrl(options) + '</textarea> \
            </div>';
    }
    return thefacetview
}

// pass in as render_terms_facet
function fvc_renderTermsFacet(facet, options) {
    /*****************************************
     * overrides must provide the following classes and ids
     *
     * id: facetview_filter_<safe filtername> - table for the specific filter
     * class: facetview_morefacetvals - for increasing the size of the facet
     * id: facetview_facetvals_<safe filtername> - id of anchor for changing facet vals
     * class: facetview_sort - for changing the facet ordering
     * id: facetview_sort_<safe filtername> - id of anchor for changing sorting
     * class: facetview_or - for changing the default operator
     * id: facetview_or_<safe filtername> - id of anchor for changing AND/OR operator
     *
     * each anchor must also have href="<filtername>"
     */
     
    // full template for the facet - we'll then go on and do some find and replace
    var filterTmpl = '<table id="facetview_filter_{{FILTER_NAME}}" class="facetview_filters table table-striped" data-href="{{FILTER_EXACT}}"> \
        <thead><tr><th><a class="facetview_filtershow" title="filter by {{FILTER_DISPLAY}}" \
        style="color:#333; font-weight:bold;" href="{{FILTER_EXACT}}"><span class="glyphicon glyphicon-plus"></span> {{FILTER_DISPLAY}} \
        </a> \
        <div class="btn-group facetview_filteroptions" style="display:none; margin-top:5px;"> \
            <button type="button" class="btn btn-sm btn-default facetview_morefacetvals" id="facetview_facetvals_{{FILTER_NAME}}" title="filter list size" href="{{FILTER_EXACT}}">0</button> \
            <button type="button" class="btn btn-sm btn-default facetview_sort" id="facetview_sort_{{FILTER_NAME}}" title="filter value order" href="{{FILTER_EXACT}}"></button> \
            <button type="button" class="btn btn-sm btn-default facetview_or" id="facetview_or_{{FILTER_NAME}}" href="{{FILTER_EXACT}}">OR</button> \
        </div> \
        </th></tr></thead> \
        </table>';
    
    // put the name of the field into FILTER_NAME and FILTER_EXACT
    filterTmpl = filterTmpl.replace(/{{FILTER_NAME}}/g, safeId(facet['field'])).replace(/{{FILTER_EXACT}}/g, facet['field']);
    
    // set the display name of the facet in FILTER_DISPLAY
    if ('display' in facet) {
        filterTmpl = filterTmpl.replace(/{{FILTER_DISPLAY}}/g, facet['display']);
    } else {
        filterTmpl = filterTmpl.replace(/{{FILTER_DISPLAY}}/g, facet['field']);
    };
    
    return filterTmpl
}

// pass in as render_results_metadata
function fvc_basicPager(options) {
    /*****************************************
     * overrides must provide the following classes and ids
     *
     * class: facetview_decrement - anchor to move the page back
     * class: facetview_increment - anchor to move the page forward
     * class: facetview_inactive_link - for links which should not have any effect (helpful for styling bootstrap lists without adding click features)
     *
     * should (not must) respect the config
     *
     * options.from - record number results start from (may be a string)
     * options.page_size - number of results per page
     * options.data.found - the total number of records in the search result set
     */
     
    // ensure our starting points are integers, then we can do maths on them
    var from = parseInt(options.from)
    var size = parseInt(options.page_size)
    
    // calculate the human readable values we want
    var to = from + size
    from = from + 1 // zero indexed
    if (options.data.found < to) { to = options.data.found }
    var total = options.data.found
    
    // forward and back-links, taking into account start and end boundaries
    var backlink = '<a class="facetview_decrement">&laquo; back</a>'
    if (from < size) { backlink = "<a class='facetview_decrement facetview_inactive_link'>..</a>" }
    
    var nextlink = '<a class="facetview_increment">next &raquo;</a>'
    if (options.data.found <= to) { nextlink = "<a class='facetview_increment facetview_inactive_link'>..</a>" }
    
    var meta = '<div class="pagination"><ul>'
    meta += '<li class="prev">' + backlink + '</li>'
    meta += '<li class="active"><a>' + from + ' &ndash; ' + to + ' of ' + total + '</a></li>'
    meta += '<li class="next">' + nextlink + '</li>'
    meta += "</ul></div>"
    
    return meta
}

// pass in as render_result_record
function fvc_renderResultRecord(options, record) {
    /*****************************************
     * overrides must provide the following classes and ids
     *
     * none - no specific requirements
     *
     * should (not must) use the config
     *
     * options.resultwrap_start - starting elements for any result object
     * options.resultwrap_end - closing elements for any result object
     * options.result_display - line-by-line display commands for the result object
     */
     
    // get our custom configuration out of the options
    var result = options.resultwrap_start;
    var display = options.result_display;
    
    // build up a full string representing the object
    var lines = '';
    for (var lineitem = 0; lineitem < display.length; lineitem++) {
        line = "";
        for (var object = 0; object < display[lineitem].length; object++) {
            var thekey = display[lineitem][object]['field'];
            var thevalue = ""
            if (typeof options.results_render_callbacks[thekey] == 'function') {
                // a callback is defined for this field so just call it
                thevalue = options.results_render_callbacks[thekey].call(this, record);
            } else {
                // split the key up into its parts, and work our way through the
                // tree until we get to the node to display.  Note that this will only
                // work with a string hierarchy of dicts - it can't have lists in it
                parts = thekey.split('.');
                var res = record
                for (var i = 0; i < parts.length; i++) {
                    res = res[parts[i]]
                }
                
                // just get a string representation of the object
                if (res) {
                    thevalue = res.toString()
                }
            }
            
            // if we have a value to display, sort out the pre-and post- stuff and build the new line
            if (thevalue && thevalue.toString().length) {
                if (display[lineitem][object]['pre']) {
                    line += display[lineitem][object]['pre']
                }
                line += thevalue;

                if (display[lineitem][object]['post']) {
                    line += display[lineitem][object]['post'];
                } else if(!display[lineitem][object]['notrailingspace']) {
                    line += ' ';
                }
            }
        }
        
        // if we have a line, append it to the full lines and add a line break
        if (line) {
            lines += line.replace(/^\s/,'').replace(/\s$/,'').replace(/\,$/,'') + "<br />";
        }
    }
    
    // if we have the lines, append them to the result wrap start
    if (lines) {
        result += lines
    }
    
    // close off the result with the ending strings, and then return
    result += options.resultwrap_end;
    return result;
}

// pass in as render_active_terms_filter
function fvc_renderActiveTermsFilter(options, facet, field, filter_list) {
    /*****************************************
     * overrides must provide the following classes and ids
     *
     * class: facetview_filterselected - anchor tag for any clickable filter selection
     * class: facetview_clear - anchor tag for any link which will remove the filter (should also provide data-value and data-field)
     * class: facetview_inactive_link - any link combined with facetview_filterselected which should not execute when clicked
     *
     * should (not must) respect the config
     *
     * options.show_filter_field - whether to include the name of the field the filter is active on
     * options.show_filter_logic - whether to include AND/OR along with filters
     */
    var clean = safeId(field)
    var display = facet.display ? facet.display : facet.field
    var logic = facet.logic ? facet.logic : options.default_facet_operator
    
    var frag = "<div id='facetview_filter_group_'" + clean + "' class='btn-group'>"
    
    if (options.show_filter_field) {
        frag += '<a class="btn btn-default facetview_inactive_link facetview_filterselected" href="' + field + '">'
        frag += '<span class="facetview_filterselected_text"><strong>' + display + '</strong></span>'
        frag += "</a>"
    }
        
    for (var i = 0; i < filter_list.length; i++) {
        var value = filter_list[i]
        frag += '<a class="facetview_filterselected facetview_clear btn btn-default" data-field="' + field + '" data-value="' + value + '" alt="remove" title="remove" href="' + value + '">'
        frag += '<span class="facetview_filterselected_text">' + value + '</span> <i class="icon-white icon-remove" style="margin-top:1px;"></i>'
        frag += "</a>"
        
        if (i !== filter_list.length - 1 && options.show_filter_logic) {
            frag += '<a class="btn btn-default facetview_inactive_link facetview_filterselected" href="' + field + '">'
            frag += '<span class="facetview_filterselected_text"><strong>' + logic + '</strong></span>'
            frag += "</a>"
        }
    }
    frag += "</div>"
    
    return frag        
}

// called when a request to open or close the facet is received
// this should move the facet to the state dictated by facet.open
function fvc_setFacetOpenness(options, context, facet) {
    var el = context.find("#facetview_filter_" + safeId(facet.field))
    var open = facet["open"]
    if (open) {
        el.find(".facetview_filtershow").find(".glyphicon").removeClass("glyphicon-plus")
        el.find(".facetview_filtershow").find(".glyphicon").addClass("glyphicon-minus")
        el.find(".facetview_filteroptions").show()
        el.find(".facetview_filtervalue").show()
    } else {
        el.find(".facetview_filtershow").find(".glyphicon").removeClass("glyphicon-minus")
        el.find(".facetview_filtershow").find(".glyphicon").addClass("glyphicon-plus")
        el.find(".facetview_filteroptions").hide()
        el.find(".facetview_filtervalue").hide()
    }
}

fv_result_fundopp_details = (function (resultobj) {
    var that = function(resultobj) {
        if (resultobj.id) {
            var url = '/funding_opportunities/' + resultobj.id;
            return '<a target="_blank" class="view_details" href="' + url + '">View full details</a>'
        }
        return false
    };
    return that;
})();
