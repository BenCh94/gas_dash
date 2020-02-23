

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
		$('.sidebar').css('width', '3vw');
		$('.main').css('width', '95vw');
		$('#sidebar_nav').hide();
		$('#sidebar_icons').show();
		$('#iex_attr').hide();
		$(this).hide();
	})

	$('#openMenu').click(function(){
		$('.sidebar').css('width', '12vw');
		$('.main').css('width', '85vw');
		$('#sidebar_nav').show();
		$('#sidebar_icons').hide();
		$('#iex_attr').show();
		$('#closeMenu').show();
	})
})
