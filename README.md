# Pacman Project

## Group 3
5025211015&emsp;Muhammad Daffa 'Ashdaqfillah <br/>
5025211051&emsp;Hanun Shaka Puspa <br/>
5025211113&emsp;Revanantyo Dwigantara <br/>

## Brief Description
This repository contains Greedy Best-First Search path finding implementation on Pacman using single language Python. The algorithm is implemented on the movements of the ghost to chase the player. The use of single language Python shows high and stable performance. But sometimes objects tends to overlap on each other while moving, caused by the inaccuracy of the tilemap.

## Latar Belakang
Kami membuat program ke dua untuk game PACMAN ini menggunakan implementasi kode python secara keseluruhan, hal ini dikarenakan :

1. Terdapat kendala dalam pencarian algoritma AStar (A*) pada program yang dijalankan     menggunakan Unity (C#)
2. Untuk mengatasi keakuratan dari algoritma GBFS dan AStar supaya dapat dijalankan secara realtime tanpa adanya lagging

## Kendala
### Posisi object pada tilemap yang tidak selalu tepat

Posisi player dan ghost pada tilemap di python ini diinput berdasarkan panjang frame yaitu 900x950, sedangkan arah gerakan pada ghost dan player ini di set terbatas yaitu dengan panjang 30x32 tile. Sehingga, untuk pergerakan yang mulus dan teratur, kami tetap menggunakan pergerakan tiap panjang frame yaitu per satu tile frame. 

Hal ini menimbulkan konsekuensi terhadap pergerakan arah dari pergerakan ghost dan player yang terbatas pada map (30x32) sehingga dalam beberapa kondisi membuat object tersangkut dan tidak mengikuti arah tile yang seharusnya. Karena dalam perhitungan gbfs, arah ditentukan tiap 1 frame. Sehingga kondisi ini sedikit menyulitkan player dan ghost untuk mendapat arah gbfs yang tepat.

