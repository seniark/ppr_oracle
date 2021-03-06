/* File: scripts.js
 *
 * Common scripts used by PPR Oracle
 */

// using jQuery
function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}

function csrfSafeMethod(method) {
	// these HTTP methods do not require CSRF protection
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function get_checked_boxes(group) {
	var container = document.getElementsByName(group)[0];
	var checkboxes = container.getElementsByTagName("INPUT");
	var checked = [];

	for (var i = 0; i < checkboxes.length; i++) {
		if (checkboxes[i].checked) {
			checked.push(checkboxes[i].name);
		}
	}

	return checked.length > 0 ? checked : null;
}

function add_player_to_team(player_id, post_url, csrf_token) {
	checked = get_checked_boxes("checkboxes-" + player_id);

	$.ajax({
		url : post_url,					// Endpoint
		type : 'POST',					// HTTP Method
		data : {						// Data sent with post,
			'team_ids[]': checked,
			'csrfmiddlewaretoken': csrf_token,
		},	

		// handle a successful response
		success: function(json) {
			for (var key in json) {
				if (json.hasOwnProperty(key)) {
					$('#alert_placeholder').append(
						"<div id='alertdiv" + key + "' class='alert alert-success'>" +
						"<a class='close' data-dismiss='alert'>&times;</a>" + 
						"<span>" + json[key] + "</span></div>"
					);
				}
			}

			setTimeout(function() {
				var placeholder = document.getElementById("alert_placeholder");
				while (placeholder.firstChild) {
					placeholder.firstChild.remove();
				}
			}, 5000);
		},

		// handle a non-successful response
		error : function(xhr, errmsg, err) {
			console.log(xhr.status + ": " + xhr.responseText);

			$('#alert_placeholder').append(
				"<div id='alertdiv' class='alert alert-error'>" +
				"<a class='close' data-dismiss='alert'>x</a>" +
				"<span>Error adding player to selected teams</span></div>"
			);
		}
	});
}
