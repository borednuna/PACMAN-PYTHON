# Pacman Project

## Group 3
5025211015&emsp;Muhammad Daffa 'Ashdaqfillah <br/>
5025211051&emsp;Hanun Shaka Puspa <br/>
5025211113&emsp;Revanantyo Dwigantara <br/>

## Brief Description
This repository contains Greedy Best-First Search path finding implementation on Pacman using single language Python. The algorithm is implemented on the movements of the ghost to chase the player. The use of single language Python shows high and stable performance. But sometimes objects tends to overlap on each other while moving, caused by the inaccuracy of the tilemap.

## Alur Kerja Program
Program kami buat dengan C# dan Python. Pada awal permainan kami menambahkan story line mengenai Pacman.

### GBFS
Sebelum masuk ke dalam fungsi python untuk menghitung fungsi heuristik dari program python, dilakukan dulu pemanggilan fungsi python pada code c# yang melemparkan argumen direction dan position ghost maupun player.

Pada code python, dilakukan pengecekan fungsi heuristik menggunakan garis lurus dari hasil phytagoras sumbu x dan y dari kedua posisi ghost dan player. Pengecekan hanya akan dilakukan pada langkah yang mungkin dilakukan oleh ghost (Up, Down, Right, Left).

Fungsi akan mengembalikan ke program c# hasil direction yang memiliki jarak paling sedikit dari available direction ghost ke player.

### A*
Pada fungsi algoritma pencarian A Star (A*) dilakukan pengecekan dengan fungsi heuristik seperti pada code gbfs, namun dengan adanya penambahan cost pada setiap perpindahan langkah.

jumlah perpindahan langkah diketahui dengan mengambil pola dari TILE yang didefinisikan dalam game.

Sehingga, pada akhir program, akan dikembalikan nilai direction dari ghost yang memiliki total cost paling sedikit.
## Kendala
### Pemanggilan program Phyton dalam C# mengakibatkan lagging

Pada implementasi program phyton dalam code C#, mengakibatkan kendala pada fungsi game yaitu lagging. Hal ini dikarenakan fungsi dipanggil setiap kali ghost memutuskan tujuan untuk bergerak. Sehingga dapat dikatakan fungsi pemanggilan python ini berjalan setiap saat (jika diasumsikan 24 frame/second) maka akan dipanggil 24 kali dalam satu detik.  Sedangkan proses pemanggilan python sendiri memakan memory dan daya yang digunakan oleh komputer, sehingga dapat mengakibatkan lagging pada game.

Solusi sementara : untuk mengurangi lagging yang diakibatkan oleh pemanggilan python setiap saat, kami membatasi ghost untuk memutuskan tujuan bergerak setiap 2 detik sekali, sehingga dapat mengurangi pemanggilan program yang terus menerus. Dengan konsekuensi untuk pergerakan dalam sebelum jangka waktu 2 detik tersebut, ghost akan menggunakan pergerakan terakhir kali dan jika bertatapan dengan wall, akan diputuskan pergerakan secara random movement.

### Implementasi algoritma AStar tidak dapat berjalan dengan baik 

Implementasi AStar dalam program ini tidak dapat berjalan dengan baik dikarenakan dalam pemetaan TILE_MAP, tidak bisa ditentukan fungsi TILE_MAP untuk memutuskan ghost bergerak sesuai dengan available_direction yang dimilikinya. Hal tersebut dikarenakan tidak ada pemeteaan yang dapat dikonversi ke dalam bentuk binary dari unity ke dalam program python.

## Latar Belakang Program Kedua
Kami membuat program ke dua untuk game PACMAN ini menggunakan implementasi kode python secara keseluruhan, hal ini dikarenakan :

1. Terdapat kendala dalam pencarian algoritma AStar (A*) pada program yang dijalankan     menggunakan Unity (C#)
2. Untuk mengatasi keakuratan dari algoritma GBFS dan AStar supaya dapat dijalankan secara realtime tanpa adanya lagging

## Kendala
### Posisi object pada tilemap yang tidak selalu tepat

Posisi player dan ghost pada tilemap di python ini diinput berdasarkan panjang frame yaitu 900x950, sedangkan arah gerakan pada ghost dan player ini di set terbatas yaitu dengan panjang 30x32 tile. Sehingga, untuk pergerakan yang mulus dan teratur, kami tetap menggunakan pergerakan tiap panjang frame yaitu per satu tile frame. 

Hal ini menimbulkan konsekuensi terhadap pergerakan arah dari pergerakan ghost dan player yang terbatas pada map (30x32) sehingga dalam beberapa kondisi membuat object tersangkut dan tidak mengikuti arah tile yang seharusnya. Karena dalam perhitungan gbfs, arah ditentukan tiap 1 frame. Sehingga kondisi ini sedikit menyulitkan player dan ghost untuk mendapat arah gbfs yang tepat.

