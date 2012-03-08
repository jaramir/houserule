$.mockjax( {
    url: '/search/game', // ?term=catan
    proxy: '/static/fixture/search_game.json'
} );

module( "game_finder", {
    setup: function() {
        var onclick = "$('#finder').data('game_finder').search($('#term').val());"
        $("#qunit-fixture").html(
            '<div id="finder"></div>' +
            '<input type="text" id="term" />' +
            '<input type="button" id="goto" onclick="' + onclick + '" />'
        );
        $("#finder").game_finder();
    }
} );

test( "we can search for catan", function() {
    $( '#term', $("#qunit-fixture") ).val( "catan" );
    $( '#goto', $("#qunit-fixture") ).click();

    expect( 3 );
    stop(); // give it some time..

    setTimeout( function() {
        equal(
            $( '.game', $("#finder") ).length, 7,
            "game_finder should contain seven .game elements"
        );
        equal(
            $( '.game img', $("#finder") ).first().attr( "src" ),
            "http://cf.geekdo-images.com/images/pic1115825_t.jpg",
            "game_finder should contain 7 Wonders: Catan Island (image)"
        );
        equal(
            $( '.game span', $("#finder") ).first().html(),
            "7 Wonders: Catan Island",
            "game_finder should contain 7 Wonders: Catan Island (text)"
        );
        start();
    }, 750 );

} );
