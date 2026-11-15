# RANCANGAN ALGORITMA GENETIKA (GA) – CASE BASED SEARCHING
**Mata Kuliah:** Kecerdasan Buatan (RPL) – Semester Genap 2025/2026
**Referensi Materi:** Slide Pertemuan 2 (*Uninformed Search*) & Pertemuan 4 (*Metaheuristic Search – Tim Dosen RPL*)
**Anggota Kelompok:**
1. **Farhan Kurniawan**
2. **Ammar Dzaki**

> **Tips Membaca File Ini di Editor:**
> Tekan **`Ctrl + Shift + V`** (atau klik ikon kaca pembesar di pojok kanan atas tab) untuk membuka tampilan **Markdown Preview**, atau baca langsung di bawah karena tabel dan diagram sudah dirapikan.

---

## 1. DESKRIPSI MASALAH & LATAR BELAKANG METODE SEARCHING

### 1.1 Definisi Masalah
Diberikan suatu fungsi matematis dua variabel untuk dicari nilai **x1** dan **x2** sehingga diperoleh **nilai minimum** dari fungsi berikut:

```text
f(x1, x2) = -( sin(x1) * cos(x2) * tan(x1 + x2)  +  0.5 * exp(1 - sqrt(x2^2)) )
```

dengan domain (batas nilai) untuk `x1` dan `x2`:
* `rb = -10` (batas bawah) dan `ra = 10` (batas atas), yaitu `-10 <= x1 <= 10` dan `-10 <= x2 <= 10`.

### 1.2 Keterkaitan dengan Materi Searching (Pertemuan 2 & Pertemuan 4)
* Berdasarkan materi **Pertemuan 2 (Uninformed Search)** dan **Pertemuan 4 (Slide 2–10)**, penyelesaian masalah dengan teknik *searching* dimulai dengan mendefinisikan **ruang keadaan (*state space*)** dan **operator** pencarian.
* Namun, metode *Uninformed Search* (BFS, DFS, IDS) maupun *Informed Search* (`A*`) tidak efisien untuk permasalahan optimasi fungsi kontinu dengan **ruang solusi yang sangat besar (*Large Solution Space*, Slide 3–9)**.
* Oleh karena itu, sesuai taksonomi optimasi pada **Pertemuan 4 (Slide 10, 18, 19, & 20)**, digunakan pendekatan *Probabilistic -> Evolutionary Computation (EC) -> Evolutionary Algorithms (EAs) ->* **Genetic Algorithms (GA)** dengan representasi *binary strings*.

---

## 2. ANALISIS KARAKTERISTIK FUNGSI (Bahan Laporan & Presentasi)

1. **Suku Eksponensial:**
   Bentuk `sqrt(x2^2)` ekuivalen dengan nilai mutlak `|x2|`. Suku `0.5 * exp(1 - |x2|)` hanya bernilai positif kecil di rentang `(0 s.d. 1.359]`, sehingga pengaruhnya jauh lebih kecil dibandingkan suku `tan(x1 + x2)`.

2. **Suku Tangen (Asimtot Vertikal):**
   Fungsi `tan(x1 + x2)` memiliki **asimtot vertikal** pada setiap garis:
   ```text
   x1 + x2 = (pi / 2) + k * pi     (dengan k = ..., -2, -1, 0, 1, 2, ...)
   ```
   Di dekat garis asimtot tersebut, nilai `tan(x1 + x2)` membesar menuju tak hingga, sehingga nilai `f(x1, x2)` turun menuju **minus tak hingga (-inf)**.

3. **Konsekuensi pada Algoritma Genetika:**
   Karena kromosom biner (*genotype*) merepresentasikan titik-titik diskrit dengan presisi terbatas, ruang pencarian GA bersifat berhingga. Akibatnya, GA akan konvergen menuju **titik grid diskrit yang paling dekat dengan salah satu garis asimtot** `x1 + x2 ≈ pi/2 + k*pi`.

---

## 3. RINGKASAN PARAMETER & DESAIN GA (Sesuai Skema Umum EAs – Slide 19)

| No | Komponen Desain GA       | Pilihan Metode (Acuan Slide Pertemuan 4)        | Nilai Parameter                          |
|----|--------------------------|-------------------------------------------------|------------------------------------------|
| 1  | Representasi Kromosom    | Representasi Biner (Slide 20, 23, & 75)         | 36 bit (N = 18 bit x1 + N = 18 bit x2)   |
| 2  | Ukuran Populasi          | Populasi Tetap / Fixed Size (Slide 36 & 78)     | u_p = 100 individu                       |
| 3  | Rumus Decode (Phenotype) | Decode Biner ke Kontinu (Slide 24, 79, & 81)    | rb = -10, ra = 10, ketelitian ≈ 0.000076 |
| 4  | Fungsi Fitness           | Transformasi Minimasi ( Analisis Slide 28 & 76) | fitness = -f(x1, x2)                     |
| 5  | Pemilihan Orangtua       | Tournament Selection (Slide 31 & 36)            | Ukuran turnamen k = 3                    |
| 6  | Rekombinasi (Crossover)  | Rekombinasi Satu Titik / 1-Point (Slide 39–40)  | Pc = 0.80 (80% – sesuai Slide 78)        |
| 7  | Mutasi                   | Mutasi Biner / Bit-Flip (Slide 55–56)           | Pm = 1/36 ≈ 0.0278 (kondisi a <= Pm)     |
| 8  | Seleksi Survivor         | Generational Model + Elitisme (Slide 68–70, 77) | 2 individu elit terbaik dipertahankan    |
| 9  | Kriteria Terminasi       | Batas Generasi atau Stagnasi (Slide 19 & 83)    | Maks 200 generasi / 50 generasi stagnan  |

---

## 4. RINCIAN ANALISIS & DESAIN (Sesuai Poin Wajib Laporan)

### 4.1 Ukuran Populasi, Rancangan Kromosom (Genotype), dan Cara Decode (Phenotype)

#### A. Ukuran Populasi (`u_p = 100`)
* Digunakan **100 kromosom/individu** dalam satu generasi (mengikuti ilustrasi populasi `N = 100` pada **Slide 36**).
* **Alasan:** Fungsi memiliki banyak lembah curam di sekitar garis asimtot `tan(x1 + x2)`. Populasi 100 individu menjaga keberagaman genetik (*diversity*) agar tidak cepat terjebak di minimum lokal, sekaligus tetap cepat dieksekusi (`100 x 200 = 20.000` evaluasi fungsi, waktu jalan `< 0.2 detik`).

#### B. Rancangan Kromosom / Genotype (Representasi Biner 36 Bit – Slide 23 & 75)
Mengacu pada **Slide 22, 23, dan 75**, setiap individu dikodekan sebagai **Genotype** berupa *binary string* sepanjang **36 bit** yang dibagi menjadi dua segmen sama panjang (`N = 18` bit untuk `x1` dan `N = 18` bit untuk `x2`):

```text
+--------------------------------------+--------------------------------------+
|       Genotype Segmen x1 (N=18)      |       Genotype Segmen x2 (N=18)      |
+--------------------------------------+--------------------------------------+
|  g1   g2   g3   ...             g18  |  g19  g20  g21  ...             g36  |
+--------------------------------------+--------------------------------------+
```

**Alasan memilih `N = 18` bit per variabel:**
Rentang domain adalah `ra - rb = 10 - (-10) = 20`. Dengan `N = 18` bit, terdapat `2^18 - 1 = 262.143` interval diskrit sehingga resolusi/ketelitian nilai **Phenotype** (`x1` dan `x2`) mencapai:

```text
Ketelitian = (ra - rb) / (2^N - 1) = 20 / 262143 ≈ 0.0000763  (4 s.d. 5 angka desimal)
```

#### C. Cara Decode Kromosom (Genotype -> Phenotype, Slide 24, 79, & 81)
Sesuai rumus resmi pada **Slide 24 dan Slide 79**, konversi segmen biner `[g_1, g_2, ..., g_N]` menjadi nilai riil (*Phenotype*) `x` pada rentang `[rb, ra]` adalah:

```text
               (ra - rb)
x = rb + --------------------- * ( g_1 * 2^(-1) + g_2 * 2^(-2) + ... + g_N * 2^(-N) )
          sum_{i=1..N} 2^(-i)
```

**Keterangan Notasi (Slide 24):**
* `rb = -10` : batas bawah domain (*lower bound*)
* `ra = 10`  : batas atas domain (*upper bound*)
* `N = 18`   : jumlah bit untuk setiap variabel (`x1` maupun `x2`)
* `g_i`      : nilai bit ke-`i` (`0` atau `1`)
* Nilai penyebut `sum_{i=1..18} 2^(-i) = 1 - 2^(-18) = 262143 / 262144 ≈ 0.999996185`.

**Contoh Perhitungan Decode (Genotype -> Phenotype):**

| Variabel | Genotype (18 bit)    | Nilai `sum(g_i * 2^-i)` | Rumus Decode Slide 24 & 79                     | Phenotype |
|----------|----------------------|-------------------------|------------------------------------------------|-----------|
| x1       | `110010000000000000` | `0.78125000`            | `-10 + (20 / 0.999996185) * 0.78125000`        | `5.62506` |
| x2       | `011001100110011001` | `0.39999771`            | `-10 + (20 / 0.999996185) * 0.39999771`        | `-2.00002`|

*Keunggulan:* Dengan rumus decode biner pada **Slide 24**, berapa pun kombinasi bit `0` dan `1` hasil rekombinasi maupun mutasi, nilai *phenotype* `x1` dan `x2` **dijamin selalu berada di dalam domain `[-10, 10]`**.

---

### 4.2 Perhitungan Fungsi Fitness (Analisis Slide 28, 29, & 76)

* Pada **Slide 28 dan Slide 76**, dijelaskan bahwa untuk masalah **minimasi fungsi** `h`, fungsi fitness dapat dirumuskan sebagai `f = 1 / (h + a)` apabila batas bawah nilai fungsi diketahui tidak negatif (seperti contoh `h = x1^2 + x2^2 >= 0` di Slide 74–76 dengan `a = 0.01`).
* Namun pada tugas ini, fungsi objektif `f(x1, x2)` mengandung suku `tan(x1 + x2)` yang nilainya dapat mencapai **negatif puluhan ribu** di dekat asimtot. Apabila digunakan rumus `1 / (f + a)` dengan `a` kecil, maka penyebut `(f + a)` akan bernilai nol (*division by zero*) atau negatif sehingga membalik urutan kualitas individu.
* Oleh karena itu, agar urutan kualitas selalu konsisten untuk seluruh nilai negatif, digunakan fungsi fitness:

```text
fitness(x1, x2) = -f(x1, x2)
```

Semakin kecil (semakin negatif) nilai `f(x1, x2)`, semakin besar nilai `fitness` individu tersebut.

---

### 4.3 Metode Pemilihan Orangtua (Slide 31–36)

* **Metode:** **Tournament Selection** (**Slide 31 & 36**) dengan ukuran turnamen `k = 3`.
* **Langkah Kerja:**
  1. Ambil `k = 3` individu secara acak dari populasi (`u_p = 100`).
  2. Pilih individu dengan nilai `fitness` tertinggi di antara ke-3 kandidat tersebut sebagai **Orangtua 1**.
  3. Ulangi langkah yang sama untuk memilih **Orangtua 2**.
* **Alasan Pemilihan (Mengacu pada Slide 34–35):**
  * Pada **Slide 34–35**, ditunjukkan bahwa metode proporsional (*Roulette Wheel* dan *Baker's SUS*) memiliki kelemahan ketika terdapat satu individu dengan fitness sangat besar dibandingkan individu lain (contoh di Slide 35: `K4` memiliki fitness `17` dari total `20` sehingga mendominasi seluruh putaran seleksi).
  * Selain itu, *Roulette Wheel* tidak dapat bekerja langsung jika terdapat nilai fitness negatif. *Tournament Selection* (**Slide 36**) hanya membandingkan urutan besar-kecil fitness antar-kandidat, sehingga bebas dari masalah nilai negatif dan menjaga tekanan seleksi tetap seimbang.

---

### 4.4 Metode Operasi Genetik (Rekombinasi & Mutasi – Slide 39–40 & 55–56)

#### A. Rekombinasi Satu Titik / 1-Point Crossover (`Pc = 0.8`, Slide 39, 40, & 78)
1. Bangkitkan bilangan acak `r` di rentang `[0, 1)`.
2. Jika `r <= Pc`:
   * Pilih satu **titik potong** acak `t` dari `1` sampai `35` (**Slide 40**).
   * **Anak 1** menerima bit `1..t` dari Orangtua 1 dan bit `(t+1)..36` dari Orangtua 2.
   * **Anak 2** menerima bit `1..t` dari Orangtua 2 dan bit `(t+1)..36` dari Orangtua 1.
3. Jika `r > Pc`: kedua anak menyalin langsung kromosom kedua orangtua.

```text
Ilustrasi Rekombinasi Satu Titik (Slide 40) pada titik potong t = 2:
Orangtua 1 : [ 1  0 | 1  1  0  1  0  1 ... ]   --->   Anak 1 : [ 1  0 | 1  0  1  1  1  0 ... ]
Orangtua 2 : [ 0  1 | 1  0  1  1  1  0 ... ]   --->   Anak 2 : [ 0  1 | 1  1  0  1  0  1 ... ]
```

#### B. Mutasi untuk Representasi Biner (`Pm = 1/36 ≈ 0.0278`, Slide 56)
Sesuai **Slide 56 (*Mutasi untuk Representasi Biner*)**:
* Untuk setiap posisi bit ke-1 s.d. ke-36 pada kromosom anak, bangkitkan bilangan acak `a` di rentang `[0, 1)`.
* Jika `a <= Pm`, balik nilai bit tersebut: **`1 -> 0` dan `0 -> 1`**.

```text
Ilustrasi Mutasi Biner (Slide 56):
Kromosom awal         : [ 0  1  1  0  1  1  1  0 ... ]
                             ^ (a <= Pm, bit ke-2 dibalik: 1 -> 0)
Kromosom hasil mutasi : [ 0  0  1  0  1  1  1  0 ... ]
```

---

### 4.5 Probabilitas Operasi Genetik (`Pc` dan `Pm` – Slide 78)

* **Probabilitas Rekombinasi (`Pc = 0.8`):** Mengikuti nilai yang dicontohkan pada **Slide 78** (`pc = 0,8`), artinya 80% pasangan orangtua di dalam *mating pool* mengalami rekombinasi satu titik potong, sementara 20% sisanya diteruskan secara utuh.
* **Probabilitas Mutasi (`Pm = 1/36 ≈ 0.0278`):** Mengacu pada prinsip mutasi di **Slide 53 & 56** bahwa mutasi harus bersifat **kecil dan jarang terjadi** agar tidak merusak kromosom yang sudah baik. Dengan `Pm = 1/36` (panjang kromosom `L = 36`), rata-rata hanya **1 bit per kromosom anak** yang mengalami pembalikan bit.

---

### 4.6 Metode Pergantian Generasi / Seleksi Survivor (Slide 68–70 & 77–78)

* **Metode:** **Generational Model + Elitisme** (**Slide 68–70 & Slide 77–78**).
* **Langkah Kerja:**
  1. Urutkan populasi generasi saat ini (`u_p = 100`) berdasarkan nilai fitness dari tertinggi ke terendah.
  2. **Elitisme (Slide 77–78):** Salin langsung **2 individu terbaik** ke populasi generasi baru agar solusi terbaik tidak pernah hilang akibat rekombinasi atau mutasi.
  3. **Generational Replacement (Slide 69–70):** Bentuk **98 individu anak baru** dari *mating pool* melalui proses seleksi orangtua, rekombinasi, dan mutasi hingga populasi baru berjumlah `N = 100` kromosom, lalu gantikan populasi lama dengan populasi baru.

---

### 4.7 Kriteria Penghentian Evolusi / Terminasi (Slide 19 & 83)

Siklus evolusi dihentikan (*Terminasi*, **Slide 19**) apabila **salah satu** kondisi terpenuhi:
1. Evolusi telah mencapai batas maksimum **200 generasi** (`MAX_GEN = 200`), ATAU
2. Nilai fitness terbaik tidak mengalami peningkatan selama **50 generasi berturut-turut** (`MAX_STALL = 50`).

---

## 5. ALUR PROGRAM (SESUAI SKEMA UMUM EAs – SLIDE 19)

```text
+-------------------------------------------------------------------+
| 1. INISIALISASI POPULASI (Slide 19 & 75)                          |
|    Bangkitkan u_p = 100 kromosom biner acak (36 bit / individu)   |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 2. DECODE KROMOSOM & HITUNG FITNESS (Slide 24, 28, & 79)          |
|    - Decode Genotype (36 bit) -> Phenotype (x1, x2) di [-10, 10]  |
|    - Hitung fitness = -f(x1, x2) untuk ke-100 individu            |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 3. CEK KRITERIA TERMINASI (Slide 19)                              |
|    Apakah generasi == 200 ATAU stagnan selama 50 generasi?        |
+-------------------------------------------------------------------+
         |                                               |
         | TIDAK                                         | YA
         v                                               v
+---------------------------------------+   +-----------------------+
| 4. EVOLUSI POPULASI BARU (100 Ind.)   |   | 5. TAMPILKAN OUTPUT   |
|    a. Elitisme: simpan 2 ind. terbaik |   |    - Kromosom terbaik |
|    b. Ulangi 49 pasangan:             |   |      (Genotype 36bit) |
|       - Seleksi Ortu (Tournament k=3) |   |    - Nilai x1 dan x2  |
|       - Rekombinasi 1-Titik (Pc=0.8)  |   |      (Phenotype)      |
|       - Mutasi Biner a<=Pm (Pm=1/36)  |   |    - Nilai f(x1, x2)  |
|    c. Seleksi Survivor (Generational) |   +-----------------------+
|    d. Kembali ke Langkah 2            |                |
+---------------------------------------+                v
                                            +-----------------------+
                                            | 6. SELESAI            |
                                            +-----------------------+
```

---

## 6. HASIL UJI COBA PROTOTIPE (5 Nilai Seed Berbeda)

| Seed | Generasi Berhenti | Phenotype x1 | Phenotype x2 | Nilai Minimum f(x1, x2) | Nilai x1 + x2 (Dekat Asimtot) |
|------|-------------------|--------------|--------------|-------------------------|-------------------------------|
| 0    | 128               |  7.85895     | -9.42970     | -19766.7445             | -1.57075  (≈ -pi/2)           |
| 1    | 124               |  7.85369     |  9.42512     | -18560.6934             |  17.27881 (≈ 11*pi/2)         |
| 2    | 169               | -4.81787     |  3.24712     | -19548.0701             | -1.57075  (≈ -pi/2)           |
| 3    | 156               |  1.87512     |  9.12048     | -33280.7181             |  10.99560 (≈ 7*pi/2)          |
| 4    | 200               |  4.66673     | -3.09598     | -19726.1503             |  1.57075  (≈ +pi/2)           |

**Kesimpulan untuk Presentasi ("Pendapat terhadap Hasil"):**
Dari kelima percobaan di atas, program GA selalu berhasil menemukan *phenotype* `(x1, x2)` yang jumlahnya mendekati `pi/2 + k*pi` (`-1.5708`, `+1.5708`, `10.9956`, atau `17.2788`). Ini membuktikan bahwa algoritma bekerja dengan tepat menuju lokasi asimtot fungsi `tan(x1 + x2)` tempat nilai `f(x1, x2)` paling minimum.

---

## 7. PEMBAGIAN PERAN ANGGOTA KELOMPOK (50% : 50%)

Bagian ini wajib dicantumkan di dalam **Laporan Tugas (.PDF)** sesuai aturan penilaian.

| Nama Anggota     | Tanggung Jawab Kode Program (Python)                                                                 | Tanggung Jawab Laporan (.PDF) & Slide Presentasi                                                                                      |
|------------------|------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------|
| Farhan Kurniawan | 1. Definisi parameter & fungsi objektif `f(x1, x2)`<br>2. Inisialisasi populasi (`inisialisasi_populasi`)<br>3. Dekode kromosom biner Slide 24 (`dekode_kromosom`)<br>4. Perhitungan fitness (`hitung_fitness`)<br>5. Seleksi orangtua Tournament Slide 36 (`pilih_orangtua`) | 1. Bab Deskripsi Masalah & keterkaitan materi Searching<br>2. Analisis ukuran populasi, rancangan kromosom (*Genotype*), dan rumus decode (*Phenotype*)<br>3. Analisis fungsi fitness & pemilihan orangtua<br>4. Presentasi bagian 1 (masalah, kromosom, decode, fitness, seleksi) |
| Ammar Dzaki      | 1. Rekombinasi satu titik Slide 40 (`pindah_silang`)<br>2. Mutasi biner Slide 56 (`mutasi`)<br>3. Seleksi survivor Generational + Elitisme (`pergantian_generasi`)<br>4. Loop utama evolusi, kriteria terminasi, & output (`main`) | 1. Analisis metode operasi genetik (rekombinasi & mutasi) serta nilai `Pc` dan `Pm`<br>2. Analisis seleksi survivor (elitisme) & kriteria penghentian loop<br>3. Pengujian program, screenshot output, & pendapat hasil<br>4. Presentasi bagian 2 (crossover, mutasi, generasi, hasil & kesimpulan) |
