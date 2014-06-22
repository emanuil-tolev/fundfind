function suggestions_error(msg) {
	$('#suggestions').html(msg);
}

function bootstrap3_compat(next_callback) {
    $("#facetview *[class^='span']").each(function(index, elem) {
	    var e = $(elem);

	    // convert spans into medium columns under the new grid system
	    var class_str = e.attr('class')
	    class_str = class_str.replace(/( )*span([0-9])/gi, '$1col-md-$2')
	    e.attr('class', class_str);
	});

	$("#facetview .row-fluid").each(function(index, elem) {
	    var e = $(elem);
	    e.removeClass('row-fluid');
	    e.removeClass('row'); // don't double the classes e.g. "row row-fluid" must not become "row row"
	    e.addClass('row');
	});

    $('i[class^="icon-"]').each(function(index, elem) {
        var e = $(elem);
        e.addClass('glyphicon');

	    var class_str = e.attr('class')
        var classes = class_str.split(' ');
        for (var i = 0; i < classes.length; i++) {
            classes[i] = classes[i].replace(/^icon-(.+)$/gi, 'glyphicon-$1');
        }
        class_str = classes.join(' ');
	    e.attr('class', class_str);
    });


	if (typeof next_callback == 'function') {
	    next_callback();
	}
}

jQuery(document).ready(function($) {

    console.log(fvc_searchOptions);

  $('.facet-view-simple').facetview({
    search_url: 'http://' + es_host + '/' + es_index + '/funding_opportunity/_search?',
    search_index: 'elasticsearch',
    datatype: 'json',

    facets: [
        {'field': 'tags.exact', 'display': 'Tags'},
        {'field': 'funder.exact', 'display': 'Funder'},
        {'field': 'title', 'display': 'Title Keywords'},
        {'field': '_type', 'display': 'Record Type'},
        {'field': 'origin.exact', 'display': 'Origin'},
        {'field': 'owner.exact', 'display': 'Submitter'},
    ],
    sort: [{'modified':{'order':'desc'}}],
    searchbox_fieldselect: [{'display':'Opportunity Title','field':'title'},{'display':'Funder','field':'funder'}],
    paging: {
      size: 10
    },
    sharesave_link: false,
    post_render_callback: bootstrap3_compat,
    pager_on_top: false,
    render_search_options: fvc_searchOptions,
    render_terms_facet: fvc_renderTermsFacet,
    behaviour_toggle_facet_open: fvc_setFacetOpenness,
    render_active_terms_filter: fvc_renderActiveTermsFilter,
    show_filter_field: false,
    results_render_callbacks: {
        'full_details': fv_result_fundopp_details,
    },
	result_display: [
		[
			{
				"pre": "<strong>",
				"field": "name",
				"post": "</strong>"
			}
		],
		[
			{
			    "pre": "<strong>Title</strong>: ",
				"field": "title",
			}
		],
		[
			{
				"pre": "<u>Homepage</u>: ",
				"field": "homepage",
			}
		],
		[
			{
				"pre": "<u>URL</u>: ",
				"field": "url",
			}
		],
		[
			{
			    "pre": "<u>Interested in</u>: ",
				"field": "interested_in",
			}
		],
		[
			{
			    "pre": "<u>Policies</u>: ",
				"field": "policies",
			}
		],
		[
			{
			    "pre": "<u>Tags</u>: ",
				"field": "tags",
			}
		],
		[
			{
			    "pre": "<u>Useful links</u>: ",
				"field": "useful_links",
			}
		],
/*		[
			{
			    "pre": "<strong>Username / ID</strong>: ",
				"field": "id",
			}
		],
*/		[
			{
			    "pre": "<u>Interests</u>: ",
				"field": "interests",
			}
		],
		[
			{
			    "pre": "<u>Country</u>: ",
				"field": "country",
			}
		],
		[
			{
			    "pre": "<u>Affiliation</u>: ",
				"field": "organisation",
				"post": ", "
			},
			{
				"field": "department",
				"post": ", "
			},
			{
				"field": "research_group"
			}
		],
  		[
			{
				"field": "full_details",
			}
		],
	]

  });

    var timeout = null;
    function gtrDelayedSearch() {
      if (timeout) {
        clearTimeout(timeout);
      }
      timeout = setTimeout(function() {
         gtrSearch();
      }, 1000);
    }

    function gtrSearch() {
	    	facetview_query = $('input[name=q]')[0].value;

	    	if( facetview_query.trim().length ) {
	    		var url = '/suggest/projects';

	    		$.get(url, {similar_to:facetview_query}, function(data) {
	    			if(data.error) {
	    				suggestions_error(data.error);
	    				return false;
	    			}

	    			var suggestion_count = 0;

	    			var suggestions = '';
	    			suggestion_row_start = '<div class="row suggestion-row">';
	    			suggestions = suggestions + suggestion_row_start;

	    			jQuery.each(data.results, function() {
	    				suggestion_count = suggestion_count + 1;

	    				var title = this.projectComposition.project.title;
	    				var url = this.projectComposition.project.url;
	    				var suggestion = '<div class="col-md-5 suggestion column alert block-message alert-info">';
	    				suggestion = suggestion + '<a href="';
	    				suggestion = suggestion + url;
	    				suggestion = suggestion + '" target="_blank">';
	    				suggestion = suggestion + title;
	    				suggestion = suggestion + '</a>';
	    				suggestion = suggestion + '</div>';

	    				if (suggestion_count >= 2) {
	    					suggestion_count = 0;
	    					suggestion = suggestion + '</div>';
	    					suggestion = suggestion + suggestion_row_start;
	    				}

	    				suggestions = suggestions + suggestion;
	    		    });

	    			suggestions = suggestions + '</div>';
	    			$('#suggestions').html(suggestions);
	    		}) // end of .get() call
	    		.fail(function() { suggestions_error('Suggestions problem - unknown error with AJAX request.') } )
	    		; // end of .get() row above
            }; // end of check on facetview query
    } // end of gtr search function

	$(document).on('keyup', 'input[name=q]', gtrDelayedSearch);

});
