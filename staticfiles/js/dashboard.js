

$(document).ready(function(){
	$('#dashMenu').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');		
	});

	$('.overlay').on('click', function(){
		$('.sidebar').toggleClass('active');
		$('.overlay').toggleClass('active');
	})
})
