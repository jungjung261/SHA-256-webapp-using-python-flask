$(function() {
    $('#buttonhash').click(function() {
        $.ajax({
            url: '/hash?texttohash=' + document.getElementById('texttohash').value,
            success: function(data) {
                $('#hashresult').html(data['hash']);
                $('#hashresult2').html(data['hashsalt']);
            }
        });
    });
    $('#buttontest').click(function() {
        $.ajax({
            url: '/decode?texttotest=' + document.getElementById('texttotest').value + '&hashtotest=' + document.getElementById('hashtotest').value,
            success: function(data) {
                $('#testresult').html(data['response']);
            }
        });
    });
    $('#buttontest2').click(function() {
        $.ajax({
            url: '/decodesalt?texttotest=' + document.getElementById('texttotest').value + '&hashtotest=' + document.getElementById('hashtotest').value,
            success: function(data) {
                $('#testresult').html(data['response']);
            }
        });
    });


})