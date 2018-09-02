

$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip()
	
	$('#dashMenu').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');		
	});

	$('.overlay').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');
	})
})
