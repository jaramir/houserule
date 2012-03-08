(function( $ ) {

$.widget( "hr.game_finder", {
    _create: function() {
        var o = this.options;
        var e = this.element;
    },
    search: function( term ) {
        var hdlr = this;
        $.getJSON(
            "/search/game", { term: term },
            function( data, textStatus, jqXHR ) {
                $.each( data, function( idx, item ) {
                    hdlr.add_item( item );
                } );
            }
        );
    },
    add_item: function( item ) {
        if( item.image )
            $(this.element).append( '<div class="game"><img src="' + item.image + '" /><span>' + item.name + '</span></div>' );
        else
            $(this.element).append( '<div class="game"><span>' + item.name + '</span></div>' );
    },
    destroy: function() {
        this.element.children().remove();
    }
} );

})( jQuery );
