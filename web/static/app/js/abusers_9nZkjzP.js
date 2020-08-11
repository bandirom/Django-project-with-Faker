$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});


$(function() {
    $('#generate_transfer').click(generate_transfer);
	$('#show_data_form').submit(show_data_form)
});

function show_data_form(e){
	e.preventDefault()
	form = $(this)
	var href = form.attr('action')
	var month = $("#date_filter option:selected").val();
	var year = $("#date_filter option:selected").attr('data-year')
	request_transfer_data(href, month, year)
}

function request_transfer_data(href, month, year){
	$.ajax({
		type: 'POST',
		url: href,
		data: {
			data:"date_filter",
			month:month,
			year:year,
		},
		success: function(data){
			parse_data(data.transfer_data)
		},
		error: function(e){
			console.log('ERROR');
		},
	});
}

function parse_data(data){
	$("#logs_table tr>td").remove();
	notification = $('.waiting_data_load')
	notification.append("<h3 id='waiting_data'>Waiting please, data in proceed</h3>")
	for (x of data) {
  		add_to_table(x)
	}
	notification.children().remove()
}


function add_to_table(x) {
	$('#logs_table tbody').prepend('<tr />').children('tr:first').append(row_generate_transfer_logs(x))
}

function generate_transfer(e){
	console.log('generate_transfer')
	data = $(this)
	href = $(this).data('href')
	console.log(href)
	$.ajax({
		type: 'POST',
		url: href,
		data: {
			data:'transfers',
		},
		success: function(data){
			console.log("success")
			$('#generate_transfer_message').append("<h4 style='color:red;'>"+ data.message + "</h4>")
		},
		error: function(e){
			$('#autogennerate_message').append("<h4>Something wrong :( </h4>")
		},
	});
}


function row_generate_transfer_logs(x){

	return "<td>" + x.id + "</td>" +
        "<td>" + x.user + "</td>" +
        "<td>" + x.time + "</td>" +
        "<td>" + x.resource + "</td>" +
        "<td><span class='tag tag-success'>" + x.size + "</span> " + x.size_type + "</td>"

}


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}