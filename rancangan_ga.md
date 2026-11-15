# RANCANGAN ALGORITMA GENETIKA (GA) – CASE BASED SEARCHING
**Mata Kuliah:** Kecerdasan Buatan (RPL) – Semester Genap 2025/2026

> **Tips Membaca File Ini di Editor:**
> Tekan **`Ctrl + Shift + V`** (atau klik ikon kaca pembesar di pojok kanan atas tab) untuk membuka tampilan **Markdown Preview**, atau baca langsung di bawah karena tabel dan diagram sudah dirapikan.

---

## 1. DESKRIPSI MASALAH

Mencari nilai **x1** dan **x2** yang menghasilkan **nilai minimum** dari fungsi:

```text
f(x1, x2) = -( sin(x1) * cos(x2) * tan(x1 + x2)  +  0.5 * exp(1 - sqrt(x2^2)) )
```

**Batas Domain:**
* `-10 <= x1 <= 10`
* `-10 <= x2 <= 10`

---

## 2. ANALISIS KARAKTERISTIK FUNGSI (Bahan Laporan & Presentasi)

1. **Suku Eksponensial:**
   Bentuk `sqrt(x2^2)` sama dengan nilai mutlak `|x2|`. Suku `0.5 * exp(1 - |x2|)` hanya bernilai positif kecil di rentang `(0 s.d. 1.359]`, sehingga pengaruhnya sangat kecil dibandingkan suku `tan(x1 + x2)`.

2. **Suku Tangen (Asimtot Vertikal):**
   Fungsi `tan(x1 + x2)` memiliki **asimtot vertikal** pada setiap garis:
   ```text
   x1 + x2 = (pi / 2) + k * pi     (dengan k = ..., -2, -1, 0, 1, 2, ...)
   ```
   Di dekat garis asimtot tersebut, nilai `tan(x1 + x2)` membesar menuju tak hingga, sehingga nilai `f(x1, x2)` turun menuju **minus tak hingga (-inf)**.

3. **Konsekuensi pada Algoritma Genetika:**
   Karena kromosom biner merepresentasikan titik-titik diskrit (presisi terbatas), ruang pencarian berjumlah berhingga. Oleh sebab itu, GA akan mencari **titik grid diskrit yang paling dekat dengan salah satu garis asimtot** `x1 + x2 ≈ pi/2 + k*pi`.

---

## 3. RINGKASAN PARAMETER & DESAIN GA

| No | Komponen GA            | Metode yang Dipilih                | Nilai Parameter                          |
|----|------------------------|------------------------------------|------------------------------------------|
| 1  | Representasi Kromosom  | Biner (Binary Encoding)            | 36 bit (18 bit x1 + 18 bit x2)           |
| 2  | Ukuran Populasi        | Populasi Tetap (Fixed Size)        | 100 individu                             |
| 3  | Fungsi Fitness         | Negasi Fungsi Objektif             | fitness = -f(x1, x2)                     |
| 4  | Pemilihan Orang Tua    | Tournament Selection               | Ukuran turnamen k = 3                    |
| 5  | Crossover              | Single-Point Crossover             | Pc = 0.80 (80%)                          |
| 6  | Mutasi                 | Bit-Flip Mutation (per bit)        | Pm = 1/36 ≈ 0.0278 (2.78%)               |
| 7  | Pergantian Generasi    | Generational + Elitism             | 2 individu elit terbaik dipertahankan    |
| 8  | Kriteria Penghentian   | Batas Generasi atau Stagnasi       | Maks 200 generasi / 50 generasi stagnan  |

---

## 4. RINCIAN ANALISIS & DESAIN (Sesuai Poin Laporan)

### 4.1 Ukuran Populasi, Rancangan Kromosom, dan Cara Decode

#### A. Ukuran Populasi (`POP_SIZE = 100`)
* Digunakan **100 kromosom** dalam satu generasi.
* **Alasan:** Fungsi memiliki banyak lembah curam di sekitar garis asimtot. Populasi 100 individu cukup besar untuk menjaga keragaman gen (*diversity*) agar tidak cepat terjebak di minimum lokal, sekaligus tetap ringan dihitung (maksimal `100 x 200 = 20.000` evaluasi fungsi, waktu jalan `< 0.2 detik`).

#### B. Rancangan Kromosom (Biner 36 Bit)
Setiap kromosom adalah *list* berisi **36 angka biner (0 atau 1)** yang dibagi dua:

```text
+-----------------------------------+-----------------------------------+
|         Bit 1 s.d. Bit 18         |        Bit 19 s.d. Bit 36         |
|         (18 bit untuk x1)         |         (18 bit untuk x2)         |
+-----------------------------------+-----------------------------------+
|  b1  b2  b3  ...             b18  |  b19  b20  b21  ...          b36  |
+-----------------------------------+-----------------------------------+
```

**Alasan memilih 18 bit per variabel:**
Lebar domain tiap variabel adalah `10 - (-10) = 20`. Dengan 18 bit, terdapat `2^18 - 1 = 262.143` titik pembagi, sehingga ketelitian (presisi) yang dicapai adalah:

```text
Presisi = (Batas_Atas - Batas_Bawah) / (2^18 - 1)
        = 20 / 262143
        ≈ 0.0000763   (ketelitian 4 sampai 5 angka di belakang koma)
```

#### C. Cara Decode Kromosom
Untuk mengubah 18 bit biner menjadi nilai riil `x` di dalam domain `[-10, 10]`:

1. **Ubah 18 bit biner ke bilangan bulat desimal (`g`):**
   ```text
   g = b1*(2^17) + b2*(2^16) + ... + b18*(2^0)      --> nilai g antara 0 s.d. 262143
   ```
2. **Petakan ke rentang domain `[-10, 10]`:**
   ```text
   x = Batas_Bawah + ((Batas_Atas - Batas_Bawah) * g) / (2^18 - 1)
   x = -10 + (20 * g) / 262143
   ```

**Contoh Perhitungan Decode:**

| Variabel | Potongan Bit (18 bit) | Nilai Desimal (g) | Perhitungan Decode               | Hasil Decode |
|----------|-----------------------|-------------------|----------------------------------|--------------|
| x1       | `110010000000000000`  | 204800            | `-10 + 20 * 204800 / 262143`     | `5.62506`    |
| x2       | `011001100110011001`  | 104857            | `-10 + 20 * 104857 / 262143`     | `-2.00002`   |

*Keunggulan:* Hasil decode biner **dijamin selalu berada di dalam batas `[-10, 10]`**, sehingga tidak pernah keluar domain setelah crossover maupun mutasi.

---

### 4.2 Perhitungan Fungsi Fitness

Karena tujuan soal adalah mencari **nilai minimum** `f(x1, x2)`, sedangkan GA memilih individu dengan **fitness terbesar**, maka rumus fitness yang digunakan adalah:

```text
fitness(x1, x2) = -f(x1, x2)
```

* Semakin kecil (semakin negatif) nilai `f(x1, x2)`, semakin besar nilai `fitness`.
* **Alasan tidak menggunakan `1 / (f + a)`:** Nilai `f(x1, x2)` di dekat asimtot bisa mencapai `-20.000` atau lebih rendah. Jika menggunakan `1 / (f + a)`, nilai `f + a` dapat menjadi nol (*pembagian dengan nol*) atau negatif. Rumus `fitness = -f` jauh lebih aman karena dipasangkan dengan *Tournament Selection*.

---

### 4.3 Metode Pemilihan Orang Tua (Parent Selection)

* **Metode:** **Tournament Selection** dengan ukuran turnamen `k = 3`.
* **Langkah Kerja:**
  1. Ambil `3` individu secara acak dari populasi.
  2. Pilih `1` individu dengan nilai `fitness` paling tinggi sebagai **Orang Tua 1**.
  3. Ulangi langkah 1–2 untuk mendapatkan **Orang Tua 2**.
* **Alasan:**
  * Aman untuk nilai fitness positif maupun negatif (tidak seperti *Roulette Wheel* yang gagal bila ada fitness negatif).
  * Mencegah satu individu dengan fitness ekstrem langsung mendominasi seluruh populasi pada generasi awal.

---

### 4.4 Metode Operasi Genetik (Crossover & Mutasi)

#### A. Pindah Silang – Single-Point Crossover (`Pc = 0.8`)
1. Bangkitkan angka acak `r` antara `0` sampai `1`.
2. Jika `r < 0.8`:
   * Pilih titik potong acak `t` dari `1` sampai `35`.
   * Tukar potongan bit setelah titik `t` antara kedua orang tua untuk menghasilkan 2 anak.
3. Jika `r >= 0.8`: kedua anak langsung menyalin bit kedua orang tua tanpa ditukar.

```text
Contoh pada titik potong t = 4:
Orang Tua 1 : [ 1  0  1  1 | 0  0  1 ... ]   --->   Anak 1 : [ 1  0  1  1 | 1  1  0 ... ]
Orang Tua 2 : [ 0  1  0  0 | 1  1  0 ... ]   --->   Anak 2 : [ 0  1  0  0 | 0  0  1 ... ]
```

#### B. Mutasi – Bit-Flip Mutation (`Pm = 1/36 ≈ 0.0278`)
* Untuk setiap bit ke-1 s.d. ke-36 pada kromosom anak:
  * Bangkitkan angka acak `r` antara `0` sampai `1`.
  * Jika `r < Pm`, balik nilai bit tersebut (`0` menjadi `1`, atau `1` menjadi `0`).

```text
Sebelum Mutasi : [ 1  0  1  1  0  0  1  0 ... ]
                            | (bit ke-4 terkena mutasi)
Sesudah Mutasi : [ 1  0  1  0  0  0  1  0 ... ]
```

---

### 4.5 Probabilitas Operasi Genetik (`Pc` dan `Pm`)

* **`Pc = 0.8` (80%):** Sebagian besar pasangan orang tua melakukan rekombinasi gen untuk menjelajahi ruang solusi baru, sedangkan 20% sisanya dipertahankan utuh.
* **`Pm = 1 / 36 ≈ 0.0278` (2.78% per bit):** Menggunakan kaidah standar `Pm = 1 / panjang_kromosom`. Rata-rata hanya **1 bit dari 36 bit** yang berubah pada tiap anak, sehingga keragaman terjaga tanpa merusak solusi yang sudah bagus.

---

### 4.6 Metode Pergantian Generasi (Survivor Selection)

* **Metode:** **Generational Replacement + Elitisme (`ELITISM = 2`)**
* **Langkah Kerja:**
  1. Urutkan seluruh individu pada generasi saat ini dari fitness tertinggi ke terendah.
  2. Ambil **2 individu terbaik (elit)** dan langsung masukkan ke populasi generasi baru tanpa diubah.
  3. Buat **98 individu anak** dari proses *seleksi orang tua -> crossover -> mutasi* hingga populasi baru berjumlah 100 individu.
* **Alasan:** Dengan elitisme, solusi terbaik yang sudah ditemukan **tidak pernah hilang**, sehingga nilai terbaik dijamin selalu membaik atau tetap di setiap generasi.

---

### 4.7 Kriteria Penghentian Evolusi (Stopping Criteria)

Perulangan evolusi berhenti jika **salah satu** syarat berikut terpenuhi:
1. Jumlah generasi mencapai **200 generasi** (`MAX_GEN = 200`), ATAU
2. Nilai fitness terbaik tidak membaik selama **50 generasi berturut-turut** (`MAX_STALL = 50`).

---

## 5. ALUR PROGRAM (FLOWCHART TEKS)

```text
+-------------------------------------------------------------------+
| 1. MULAI                                                          |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 2. INISIALISASI POPULASI                                          |
|    Bangkitkan 100 kromosom acak, masing-masing 36 bit (0 atau 1)  |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 3. DECODE & HITUNG FITNESS                                        |
|    - Decode 18 bit pertama -> x1, 18 bit kedua -> x2              |
|    - Hitung fitness = -f(x1, x2) untuk ke-100 individu            |
+-------------------------------------------------------------------+
                                 |
                                 v
+-------------------------------------------------------------------+
| 4. CEK KRITERIA BERHENTI                                          |
|    Apakah generasi == 200 ATAU stagnan selama 50 generasi?        |
+-------------------------------------------------------------------+
         |                                               |
         | TIDAK                                         | YA
         v                                               v
+---------------------------------------+   +-----------------------+
| 5. BUAT GENERASI BARU (100 Individu)  |   | 6. TAMPILKAN OUTPUT   |
|    a. Salin 2 individu terbaik (Elit) |   |    - Kromosom terbaik |
|    b. Ulangi 49 kali:                 |   |    - Nilai x1 dan x2  |
|       - Pilih 2 ortu (Tournament k=3) |   |    - Nilai f(x1, x2)  |
|       - Crossover (Pc = 0.8)          |   +-----------------------+
|       - Mutasi bit-flip (Pm = 1/36)   |                |
|    c. Ganti populasi lama -> baru     |                v
|    d. Kembali ke Langkah 3            |   +-----------------------+
+---------------------------------------+   | 7. SELESAI            |
                                            +-----------------------+
```

---

## 6. HASIL UJI COBA PROTOTIPE (5 Nilai Seed Berbeda)

| Seed | Generasi Berhenti | Nilai x1  | Nilai x2  | Nilai f(x1, x2) | Nilai x1 + x2 (Dekat Asimtot) |
|------|-------------------|-----------|-----------|-----------------|-------------------------------|
| 0    | 128               |  7.85895  | -9.42970  | -19766.7445     | -1.57075  (≈ -pi/2)           |
| 1    | 124               |  7.85369  |  9.42512  | -18560.6934     |  17.27881 (≈ 11*pi/2)         |
| 2    | 169               | -4.81787  |  3.24712  | -19548.0701     | -1.57075  (≈ -pi/2)           |
| 3    | 156               |  1.87512  |  9.12048  | -33280.7181     |  10.99560 (≈ 7*pi/2)          |
| 4    | 200               |  4.66673  | -3.09598  | -19726.1503     |  1.57075  (≈ +pi/2)           |

**Kesimpulan untuk Presentasi ("Pendapat terhadap Hasil"):**
Dari kelima percobaan di atas, program GA selalu berhasil menemukan pasangan `(x1, x2)` yang jumlahnya mendekati `pi/2 + k*pi` (`-1.5708`, `+1.5708`, `10.9956`, atau `17.2788`). Ini membuktikan bahwa algoritma bekerja dengan tepat menuju lokasi asimtot fungsi `tan(x1 + x2)` tempat nilai `f(x1, x2)` paling minimum.
