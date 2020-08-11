$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});


$(function() {
    $('[data-action="edit_user"]').click(edit_user_data);
    $('[data-action="remove_user"]').click(remove_user);
    $('[data-action="add_user"]').click(add_form);
    $('#save_user').click(save_user);
    $('#generate_user_form').submit(generate_users)
});

function add_form(e){
	e.preventDefault();
	document.getElementById("new_user_form").style.display="block";
}

function save_user(e) {
    e.preventDefault();
    var href = document.getElementById("save_form_user").action
	$.ajax({
		type: 'POST',
		url: href,
		data: {
			data:"user",
			user:$("[name='user']").val(),
			email:$("[name='email']").val(),
			company:$("[name='company']").val(),
		},
		success: function(data){
			add_row_user(data.user)
		},
		error: function(e){
			console.log('ERROR');
		},

	});

}

function edit_user_data(e) {
    var form = $(this)
    var row = document.getElementById("user_table").rows.namedItem(form.data('id')).cells;

	if (form.text() === ' Edit') {
		form.html('<i class="fa fa-save"></i> Save')

		change_from_edit_to_save(row)
	}
	else{
		if (validate_company(row)){  // Could be added other validation functions
			update_user_data(row)
			form.html('<i class="fas fa-edit"></i> Edit')
		}
		else
			alert('Wrong data');

	}
}

function change_from_edit_to_save(row) {
	row[1].innerHTML = "<input name='user' class='form-control' type='text' value=" + row[1].innerHTML +" size='3'>"
	row[2].innerHTML = "<input name='email' class='form-control' type='email' value=" + row[2].innerHTML +" size='2'>"
	row[3].innerHTML = companies_list

	$("option[value='5']").attr('selected',true);
}

function change_from_save_to_edit(row) {
	row[1].innerHTML = row[1].children[0].value
	row[2].innerHTML = row[2].children[0].value
	row[3].innerHTML = row[3].children[0].value
	return true

}

// check is selected company field
function validate_company(row){
//	console.log(row[3].children[0].value)

	if (row[3].children[0].innerHTML == '---------'){
		return false
	}
	if (row[3].children[0].value) {
		return true
	}
	return false
}

function update_user_data(row){
	$.ajax({
		type: 'PATCH',
		url: "/user/",
		data: {
			data:"update",
			id:row[0].innerHTML,
			user:row[1].children[0].value,
			email:row[2].children[0].value,
			company:row[3].children[0].value,
		},
		success: function(data){
			console.log("SUCCESS PATCH")
			console.log(data.user)
			update_row_user(data.user)
		},
		error: function(e){
			console.log('ERROR');
		},

	});
}


function remove_user(e) {
    e.preventDefault();
    var form = $(this)
    var action = form.data('action');
	var user_id = form.data('id');
	var href = form.attr('href');
	$.ajax({
			type: 'POST',
			url: href,
			data: {
				data:"user",
				id: user_id
			},
			success: function(data){
				delete_from_table(user_id)
			},
			error: function(e){
				console.log('ERROR');
			},
		});
}

function generate_users(e){
	e.preventDefault()
	form = $(this)
	var values = form.serializeArray();
	console.log()
	console.log(values)
	console.log()
	$.ajax({
			type: 'POST',
			url: form.attr('action'),
			data: {
				data:values[1].value,
				amount: values[2].value
			},
			success: function(data){
				console.log('Success: ' + data.message)
			},
			error: function(e){
				console.log('ERROR');
			},
		});
}

function update_row_user(user) {
	var row = document.getElementById("user_table").rows.namedItem(user.id).cells;
	row[1].innerHTML = user.user
	row[2].innerHTML = user.email
	row[3].innerHTML = user.company
	return true
}

function add_row_user(user){
	$('#user_table tbody').prepend('<tr />').children('tr:first').append(row_generate_user(user))
}

function delete_from_table(id){
	$('#user_table tr#'+ id).remove();
}

function row_generate_user(user) {
	return "<td>" + user.id + "</td>" +
        "<td>" + user.user + "</td>" +
        "<td>" + user.email + "</td>" +
        "<td><span class='tag tag-success'>" + user.company + "</span></td>" +
        "<td>" +
			"<div class='btn-group'>" +
				"<button type='button' data-action='edit_user' data-id=" + user.id + " class='btn btn-default'><i class='fas fa-edit'></i>  Edit</button>" +
				"<button type='button' class='btn btn-default dropdown-toggle dropdown-icon' data-toggle='dropdown'>" +
					 "<span class='sr-only'>Toggle Dropdown</span>" +
					 "<div class='dropdown-menu' role='menu'>" +
						  "<a href='javascript:void(0);' data-action='remove_user' data-id=" + user.id + " class='dropdown-item remove' href='#'>Remove</a>" +
					 "</div>" +
				"</button>" +
		  	"</div>" +
		"</td>"
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