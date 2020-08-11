/*!
 *  <ul class="nav nav-tabs">
 * 		<li class="nav-item active" id="active_users">
 *			<a class="nav-link active" data-toggle="tab" href="#users">Users</a>
 * 		</li>
 *  </ul>
 * ID of <li> classes should start with 'active_<tab-pane_id>
 * <div class="tab-pane active" id="users"> </div>
 *
 *  for example:
 *  	<li class="nav-item" id="active_companies"></li>
 *
 *		<div class="tab-pane " id="companies"></div>
 */


$(".nav-tabs a.nav-link").click(function(){
	var x = $(this).attr("href");
	x = x.replace("#", "");
	$(".nav-item").each(function(){
		var y = $(this).attr("id");
		y = y.replace("active_", "");
		$(this).removeClass("active");
		if (x == y) $(this).addClass("active");
	});
});