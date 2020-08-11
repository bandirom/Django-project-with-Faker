$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});


$(function() {
    $('[data-action="edit_company"]').click(edit_company_data);
    $('[data-action="remove_company"]').click(remove_company);
    $('[data-action="add_company"]').click(add_form_company);
    $('#save_company').click(save_company);

});

function add_form_company(e){
	e.preventDefault();
	document.getElementById("new_company_form").style.display="block";
}

function save_company(e) {
    e.preventDefault();
    var href = document.getElementById("save_form_company").action
	$.ajax({
			type: 'POST',
			url: href,
			data: {
				data:"company",
				name:$("[name='name']").val(),
				quota:$("[name='quota']").val(),
				size:$("[name='size']").val(),
			},
			success: function(data){
				add_to_company_table(data.company)
			},
			error: function(e){
				console.log('ERROR')
			},

		});

}

function edit_company_data(e) {
    e.preventDefault();
    console.log('edit company')
    var form = $(this)
    var action = form.data('action');
    var href = form.data('href');
	var company_id = form.data('id');
	var row = document.getElementById("company_table").rows.namedItem(form.data('id')).cells;
	if (form.text() === ' Edit') {
		form.html('<i class="fa fa-save"></i> Save')
		fields_edit_to_save(row)
	}
	else {
		if (validate_size(row)){  // Could be added other validation functions
			update_company_data(row, href)
			form.html('<i class="fas fa-edit"></i> Edit')
		}
		else
			alert('Wrong company data');
	}
}


function fields_edit_to_save(row){
	row[2].innerHTML = "<input name='quota' class='form-control' type='number' min='0' value=" + row[2].innerHTML +">"
	row[3].innerHTML = size_list
}


function validate_size(row){
	if (row[3].children[0].innerHTML == '---------'){
		return false
	}
	if (row[3].children[0].value) {
		return true
	}
	return false
}


function update_company_data(row, href){
	$.ajax({
		type: 'PATCH',
		url: href,
		data: {
			data:"update_company",
			id:row[0].innerHTML,
			name:row[1].innerHTML,
			quota:row[2].children[0].value,
			size:row[3].children[0].value,
		},
		success: function(data){
			console.log(data.company)
			update_row_company(data.company, row)
		},
		error: function(e){
			console.log('ERROR');
		},
	});
}

function update_row_company(company, row){
	row[2].innerHTML = company.quota
	row[3].innerHTML = company.size
	return true
}

function remove_company(e) {
    e.preventDefault();
    var form = $(this)
    var action = form.data('action');
	var company_id = form.data('id');
	var href = form.attr('href');
	$.ajax({
			type: 'POST',
			url: href,
			data: {
				data:"company",
				id: company_id
			},
			success: function(data){
				delete_from_company_table(company_id)

			},
			error: function(e){
				console.log('ERROR');
			},

		});

}


function add_to_company_table(company){
	$('#company_table tbody').prepend('<tr />').children('tr:first').append(row_generate_company(company))
}

function delete_from_company_table(id){
	$('#company_table tr#'+ id).remove();
	console.log('removed')
}


function row_generate_company(company) {
 return "<td>" + company.id + "</td>" +
        "<td>" + company.name + "</td>" +
        "<td>" + company.quota + "</td>" +
        "<td><span class='tag tag-success'>" + company.size + "</span></td>" +
        "<td>" +
			"<div class='btn-group'>" +
				"<button type='button' data-action='edit_company' data-id=" + company.id + " class='btn btn-default'><i class='fas fa-edit'></i>  Edit</button>" +
				"<button type='button' class='btn btn-default dropdown-toggle dropdown-icon' data-toggle='dropdown'>" +
					 "<span class='sr-only'>Toggle Dropdown</span>" +
					 "<div class='dropdown-menu' role='menu'>" +
						  "<a data-action='remove_company' data-id=" + company.id + " class='dropdown-item' href='#'>Remove</a>" +
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