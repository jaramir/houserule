// questa funzione serve per recuperare l'intero utente sapendone il nome
function( doc )
{ 
    if( doc.doc_type == "User" && doc.username )
        emit( doc.username, doc );
}
