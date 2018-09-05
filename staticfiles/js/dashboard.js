

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
})
