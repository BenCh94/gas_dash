

$('#autocompleteName').autocomplete({
	lookup: symbols,
	onSelect: function (suggestion) {
		var ticker = suggestion.data;
		$('#id_ticker_data').val(ticker);
		$('#id_benchmark_ticker').val(ticker);
	}
})
