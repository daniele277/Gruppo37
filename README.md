L'obiettivo del progetto è creare un identity provider che gestisca l'autenticazione di diversi utenti, a diversi client web. Per semplicità abbiamo definito un unico client web chiamato "sitoQualsiasi". 

Ogni utente che vuole accedere alla propria area riservata del "sitoQualsiasi", deve prima registrarsi all'identity provider.

L'intera applicazione parte con la visualizzazione dell'homepage IDP, in cui c'è un link per la registrazione dell'utente.
Dopo la registrazione dell'utente, l'applicazione fornisce una pagina in cui l'utente può scegliere se tornare alla homepage oppure provare ad autenticarsi al "sitoQualsiasi" mediante l'identity provider sul quale si è appena registrato.

Quindi con quest'ultimo link l'utente visualizza l'homepage del "sitoQualsiasi", in cui c'è un ilnk che permette di iniziare l'autenticazione mediante l'identity provider.

Con quest'ultimo inizia il protocollo "Authorization Code Flow", previsto da OAuth 2.0. 

