# rmt_game
Igra pong za dva igraca sa client-server arhitekturom, grafickim interfejsom, i bazom podataka.

server.py treba prvo pokrenuti, nakon toga pong.py <br>
Povezivanje sa mySQL bazom i fje za manipulaciju bazom se nalaze u fajlu db.py (klasa DB)
Graficki interfejs je implementiran pomocu biblioteke tkinter u fajlu login.py (klasa MainScreen), moguce je napraviti novog korisnika i prijaviti se, 
nakon cega se pokrece jedna instanca igre.
U fajlu network.py (klasa Network) su definisane fje sa klijentske strane, tj povezivanje na server i slanje podataka
Sama igra je definisan u game.py, igra je napravljena pomocu pygame biblioteke, sadrzi 4 klase: Player, Ball, Game, Canvas.


