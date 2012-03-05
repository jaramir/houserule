test( "fixture is working", function() {
    $("#qunit-fixture").html( '<div id="test_element"></div>' );

    ok(
        $( "#test_element", $("#qunit-fixture") ).length == 1,
        "qunit-fixture is not working"
    );
} );

test( "can create a game finder", function() {
    $("#qunit-fixture").html( '<div id="test_search_game"></div>' );
    $("#test_search_game").game_finder();

    ok(
        $( "#test_search_game", $("#qunit-fixture") ).length == 1,
        "game_finder initialization failed"
    );
} );

test( "game finder has an input", function() {
    $("#qunit-fixture").html( '<div id="test_search_game"></div>' );
    $("#test_search_game").game_finder();

    ok(
      $( 'input[type="text"]', $("#test_search_game") ).length == 1,
      'game_finder should contain an input[type="text"] element'
    );
} );

test( "game finder has a button", function() {
    $("#qunit-fixture").html( '<div id="test_search_game"></div>' );
    $("#test_search_game").game_finder();

    ok(
      $( 'input[type="button"]', $("#test_search_game") ).length == 1,
      'game_finder should contain an input[type="button"] element'
    );
} );

test( "we can search for catan", function() {
    $("#qunit-fixture").html( '<div id="test_search_game"></div>' );
    $("#test_search_game").game_finder();
    $( 'input[type="text"]', $("#test_search_game") ).val( "catan" );
    $( 'input[type="button"]', $("#test_search_game") ).click();

    ok(
      $( '.game', $("#test_search_game") ).length > 0,
      "game_finder should contain some .game elements"
    );
} );
