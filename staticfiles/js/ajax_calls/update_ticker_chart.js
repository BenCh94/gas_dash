// File can be included and used anywhere as long as tickerUuid is set in the head

function requestTickerUpdate(uuid){
    $.get(`/dash/ticker/request_update/${uuid}`, function(response){
        console.log(response);
        location.reload();
    })
}

$(document).ready(function(){
    $('#updateTicker').click(function(){
        console.log('Clicked update');
        requestTickerUpdate(tickerUuid);
    })
})