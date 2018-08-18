

$('#autocompleteName').autocomplete({
	lookup: symbols,
	onSelect: function (suggestion) {
		var ticker = suggestion.data;
		$('#id_ticker').val(ticker);
	}
})
