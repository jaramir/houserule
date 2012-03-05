(function( $ ) {

$.widget( "hr.game_finder", {
    options: {
    },
    _create: function() {
        var o = this.options;
        var e = $(this.element);

        this.text = $( '<input type="text"/>' );
        e.append(this.text);

        this.button = $( '<input type="button" value="Cerca"/>' );
        e.append(this.button);

        this.button.bind( "click.game_finder", $.proxy( this, "search" ) );
    },
    search: function() {
        this.add_item( { name: "Catan", image: null } );
        /*
        $.ajax( {
            type: "GET",
            url: "/search/game",
            data: {
                term: $("#game_search").val()
            },
            dataType: "json",
            success: function( data, textStatus, jqXHR ) {
                var r = $( "#game_search_results" );
                r.html( "" );
                $.each( data, function( idx, item ) {
                    r.append( $( '<div class="game"><img src="' + item.image + '" /><span>' + item.name + '</span></div>' ) );
                } );
            }
        } );
        */
    },
    add_item: function( item ) {
        $(this.element).append( '<div class="game"><img src="' + item.iamge + '" /><span>' + item.name + '</span></div>' );
    },
    destroy: function() {
        this.element.children().remove();
    }
} );

})( jQuery );
