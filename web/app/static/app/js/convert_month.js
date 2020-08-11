function option_insert(str_month, month_value, year){
	var select = document.getElementById("date_filter");
	var option = document.createElement("option");
	option.text = str_month + "/" + year;
	option.value = month_value;
	option.setAttribute('data-year', year);
	select.appendChild(option);
}

function get_month(month_number, year_number){
	switch (month_number) {
		case 1:
			return option_insert("January", 1, year_number)
		case 2:
			return option_insert("February", 2, year_number)
		case 3:
			return option_insert("March", 3, year_number)
		case 4:
			return option_insert("April", 4, year_number)
		case 5:
			return option_insert("May", 5, year_number)
		case 6:
			return option_insert("June", 6, year_number)
		case 7:
			return option_insert("July", 7, year_number)
		case 8:
			return option_insert("August", 8, year_number)
		case 9:
			return option_insert("September", 9, year_number)
		case 10:
			return option_insert("October", 10, year_number)
		case 11:
			return option_insert("November", 11, year_number)
		case 12:
			return option_insert("December", 12, year_number)
		default:
			return option_insert("--------", 0, year_number)
	}
}