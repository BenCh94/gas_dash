function setSidebarStatus(status){
	$.get(`/dash/set_menu_status_${status}`, function(response){
		console.log(response);
	})

}

$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip()

	$('.price_gain_box').click(function(event){
		event.stopPropagation();
		console.log('test');
	});
	
	$('#dashMenu').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');		
	});

	$('.overlay').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');
	})

	$('#graph_timelines').on('click', function(){
		$('#time_btns').show()
	})

	$("#closeMenu").click(function(){
		$('.sidebar').removeClass('open');
		$('.main').removeClass('narrow');
		$('.sidebar').addClass('closed');
		$('.main').addClass('wide');
		setSidebarStatus('closed');
	})

	$('#openMenu').click(function(){
		$('.sidebar').removeClass('closed');
		$('.main').removeClass('wide');
		$('.sidebar').addClass('open');
		$('.main').addClass('narrow');
		setSidebarStatus('open');
	})
})
