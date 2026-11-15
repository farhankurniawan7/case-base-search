import math   
import random  


# ==============================================================================
# CREATEDBY FARHAN KURNIAWAN
# Mencakup:
#   1. Konfigurasi Parameter GA & Fungsi Objektif f(x1, x2)
#   2. Proses 1: Inisialisasi Populasi
#   3. Proses 2: Dekode Kromosom 
#   4. Proses 3: Perhitungan Fitness
#   5. Proses 4: Pemilihan Orangtua 
# ==============================================================================

# --- 1.1 KONFIGURASI PARAMETER ALGORITMA GENETIKA ---
UKURAN_POPULASI = 100          # Ukuran populasi (u_p = 100 individu per generasi)
BIT_PER_VARIABEL = 18          # Jumlah bit (N = 18 bit) untuk masing-masing x1 dan x2
PANJANG_KROMOSOM = 36          # Total panjang kromosom biner (18 bit x1 + 18 bit x2)
BATAS_BAWAH = -10.0            # Batas bawah domain (r_b = -10) untuk x1 dan x2
BATAS_ATAS = 10.0              # Batas atas domain (r_a = 10) untuk x1 dan x2
UKURAN_TURNAMEN = 3            # Ukuran turnamen (k = 3) pada Tournament Selection
PROB_CROSSOVER = 0.80          # Probabilitas pindah silang (P_c = 0.80, Slide 78)
PROB_MUTASI = 1.0 / 36.0       # Probabilitas mutasi biner per gen (P_m = 1/36 ≈ 0.0278)
JUMLAH_ELIT = 2                # Jumlah individu terbaik yang dipertahankan (Elitisme = 2)
MAKS_GENERASI = 200            # Batas maksimum generasi evolusi (kriteria berhenti 1)
MAKS_STAGNAN = 50              # Batas generasi tanpa perbaikan fitness (kriteria berhenti 2)
RANDOM_SEED = 0                # Nilai seed agar hasil running konsisten saat di-screenshot


# --- 1.2 FUNGSI MATEMATIS OBJEKTIF f(x1, x2) ---
def hitung_fungsi_objektif(x1, x2):
    # Menghitung bagian trigonometri: sin(x1) * cos(x2) * tan(x1 + x2)
    suku_trigonometri = math.sin(x1) * math.cos(x2) * math.tan(x1 + x2)
    # Menghitung bagian eksponensial: 1/2 * exp(1 - sqrt(x2^2))
    suku_eksponensial = 0.5 * math.exp(1.0 - math.sqrt(x2 ** 2))
    # Mengembalikan nilai fungsi f(x1, x2) = -(suku_trigonometri + suku_eksponensial)
    nilai_f = -(suku_trigonometri + suku_eksponensial)
    # Mengembalikan hasil akhir perhitungan f(x1, x2)
    return nilai_f


# --- 1.3 PROSES 1: INISIALISASI POPULASI 
def inisialisasi_populasi(ukuran_pop, panjang_krom):
    # Menyiapkan list kosong untuk menampung seluruh individu dalam populasi
    populasi = []
    # Melakukan perulangan sebanyak ukuran populasi (100 individu)
    for _ in range(ukuran_pop):
        # Menyiapkan list kosong untuk menampung gen-gen biner pada satu kromosom
        kromosom = []
        # Melakukan perulangan sebanyak panjang kromosom (36 bit)
        for _ in range(panjang_krom):
            # Membangkitkan nilai bit acak 0 atau 1 untuk setiap posisi gen
            bit_acak = random.randint(0, 1)
            # Menambahkan bit acak tersebut ke dalam kromosom
            kromosom.append(bit_acak)
        # Menambahkan kromosom yang sudah terbentuk ke dalam list populasi
        populasi.append(kromosom)
    # Mengembalikan populasi awal yang berisi 100 kromosom biner (Genotype)
    return populasi


# --- 1.4 PROSES 2: DEKODE KROMOSOM BINER KE RIIL 
def dekode_satu_segmen(segmen_bit, r_b, r_a):
    # Mengetahui jumlah bit (N) pada segmen variabel (N = 18 bit)
    n_bit = len(segmen_bit)
    # Menyiapkan variabel penampung pembilang: sum_{i=1..N} (g_i * 2^(-i))
    jumlah_pembilang = 0.0
    # Menyiapkan variabel penampung penyebut: sum_{i=1..N} (2^(-i))
    jumlah_penyebut = 0.0
    # Melakukan perulangan untuk setiap gen dari indeks 0 sampai N-1 (i = 1 s.d. N)
    for indeks in range(n_bit):
        # Menentukan urutan posisi bit i (dimulai dari i = 1 sampai i = N)
        i = indeks + 1
        # Mengambil nilai gen biner g_i (0 atau 1) pada posisi tersebut
        g_i = segmen_bit[indeks]
        # Menghitung nilai bobot pangkat negatif 2^(-i) sesuai rumus Slide 24
        bobot_dua = 2.0 ** (-i)
        # Menambahkan hasil kali g_i * 2^(-i) ke dalam jumlah pembilang
        jumlah_pembilang = jumlah_pembilang + (g_i * bobot_dua)
        # Menambahkan nilai 2^(-i) ke dalam jumlah penyebut
        jumlah_penyebut = jumlah_penyebut + bobot_dua
    # Menghitung nilai riil (Phenotype) x = r_b + ((r_a - r_b) / penyebut) * pembilang
    nilai_x = r_b + ((r_a - r_b) / jumlah_penyebut) * jumlah_pembilang
    # Mengembalikan nilai riil hasil dekode yang berada di dalam rentang [r_b, r_a]
    return nilai_x


def dekode_kromosom(kromosom, n_bit_var, r_b, r_a):
    # Memisahkan 18 bit pertama (indeks 0 s.d. 17) sebagai segmen gen untuk x1
    segmen_x1 = kromosom[:n_bit_var]
    # Memisahkan 18 bit kedua (indeks 18 s.d. 35) sebagai segmen gen untuk x2
    segmen_x2 = kromosom[n_bit_var:]
    # Melakukan proses decode segmen pertama menjadi nilai riil (Phenotype) x1
    x1 = dekode_satu_segmen(segmen_x1, r_b, r_a)
    # Melakukan proses decode segmen kedua menjadi nilai riil (Phenotype) x2
    x2 = dekode_satu_segmen(segmen_x2, r_b, r_a)
    # Mengembalikan pasangan nilai riil (x1, x2) hasil dekode kromosom
    return x1, x2


# --- 1.5 PROSES 3: PERHITUNGAN FITNESS 
def hitung_fitness(kromosom, n_bit_var, r_b, r_a):
    # Mendekode kromosom biner menjadi nilai riil x1 dan x2 terlebih dahulu
    x1, x2 = dekode_kromosom(kromosom, n_bit_var, r_b, r_a)
    # Menghitung nilai fungsi objektif f(x1, x2) dari nilai x1 dan x2 tersebut
    nilai_f = hitung_fungsi_objektif(x1, x2)
    # Mengubah masalah minimasi menjadi maksimasi fitness dengan rumus fitness = -f(x1, x2)
    nilai_fitness = -nilai_f
    # Mengembalikan nilai fitness individu tersebut
    return nilai_fitness


# --- 1.6 PROSES 4: PEMILIHAN ORANGTUA - TOURNAMENT SELECTION 
def pilih_orangtua(populasi, daftar_fitness, ukuran_turnamen):
    # Menghitung jumlah total individu di dalam populasi
    jumlah_individu = len(populasi)
    # Menyiapkan variabel untuk menyimpan indeks pemenang turnamen sementara
    indeks_pemenang = -1
    # Melakukan pemilihan acak sebanyak ukuran turnamen (k = 3 kandidat)
    for _ in range(ukuran_turnamen):
        # Memilih satu indeks kandidat secara acak dari rentang 0 s.d. jumlah_individu - 1
        indeks_kandidat = random.randint(0, jumlah_individu - 1)
        # Jika belum ada pemenang atau fitness kandidat lebih tinggi dari pemenang saat ini
        if indeks_pemenang == -1 or daftar_fitness[indeks_kandidat] > daftar_fitness[indeks_pemenang]:
            # Menetapkan kandidat tersebut sebagai pemenang turnamen sementara
            indeks_pemenang = indeks_kandidat
    # Menyalin gen-gen dari kromosom pemenang agar tidak mengubah populasi asli
    kromosom_orangtua = populasi[indeks_pemenang][:]
    # Mengembalikan kromosom orangtua terpilih hasil Tournament Selection
    return kromosom_orangtua


# ==============================================================================
# CREATED BY: AMMAR DZAKI
# Mencakup:
#   1. Proses 5: Crossover / Rekombinasi Satu Titik 
#   2. Proses 6: Mutasi Representasi Biner 
#   3. Proses 7: Pergantian Generasi / Seleksi Survivor 
#   4. Loop Utama Evolusi, Kriteria Penghentian (Terminasi), & Output Program
# ==============================================================================

# --- 2.1 PROSES 5: CROSSOVER / REKOMBINASI SATU TITIK (Slide 39-40) ---
def pindah_silang(orangtua_1, orangtua_2, prob_crossover):
    # Menghitung panjang kromosom dari orangtua (36 bit)
    panjang = len(orangtua_1)
    # Membangkitkan bilangan acak r di rentang [0, 1) untuk menguji peluang crossover
    r = random.random()
    # Memeriksa apakah bilangan acak r lebih kecil atau sama dengan P_c (0.80)
    if r <= prob_crossover:
        # Memilih titik potong acak antara indeks 1 sampai panjang kromosom - 1 (1 s.d. 35)
        titik_potong = random.randint(1, panjang - 1)
        # Membentuk Anak 1: bagian kiri dari Orangtua 1 + bagian kanan dari Orangtua 2
        anak_1 = orangtua_1[:titik_potong] + orangtua_2[titik_potong:]
        # Membentuk Anak 2: bagian kiri dari Orangtua 2 + bagian kanan dari Orangtua 1
        anak_2 = orangtua_2[:titik_potong] + orangtua_1[titik_potong:]
    else:
        # Jika tidak terjadi crossover, Anak 1 menyalin utuh kromosom Orangtua 1
        anak_1 = orangtua_1[:]
        # Jika tidak terjadi crossover, Anak 2 menyalin utuh kromosom Orangtua 2
        anak_2 = orangtua_2[:]
    # Mengembalikan sepasang kromosom anak hasil pindah silang
    return anak_1, anak_2


# --- 2.2 PROSES 6: MUTASI REPRESENTASI BINER (Slide 56) ---
def mutasi(kromosom, prob_mutasi):
    # Membuat salinan kromosom agar proses mutasi aman dilakukan per bit
    kromosom_mutasi = kromosom[:]
    # Melakukan perulangan untuk memeriksa setiap posisi bit dari 0 sampai 35
    for i in range(len(kromosom_mutasi)):
        # Membangkitkan bilangan acak a di rentang [0, 1) sesuai notasi Slide 56
        a = random.random()
        # Jika nilai acak a <= P_m (probabilitas mutasi), maka bit pada posisi i dibalik
        if a <= prob_mutasi:
            # Membalik bit: jika 1 menjadi 0, jika 0 menjadi 1 (1 - bit)
            kromosom_mutasi[i] = 1 - kromosom_mutasi[i]
    # Mengembalikan kromosom yang telah melalui proses mutasi biner
    return kromosom_mutasi


# --- 2.3 FUNGSI BANTU: PENGURUTAN INDEKS POPULASI SECARA MANUAL ---
def urutkan_indeks_berdasarkan_fitness(daftar_fitness):
    # Membuat daftar indeks awal [0, 1, 2, ..., ukuran_populasi - 1]
    jumlah = len(daftar_fitness)
    indeks_terurut = list(range(jumlah))
    # Mengurutkan indeks dari fitness terbesar ke terkecil dengan Selection Sort manual
    for i in range(jumlah - 1):
        # Menganggap posisi i memiliki nilai fitness terbesar sementara
        posisi_terbesar = i
        # Mencari apakah ada nilai fitness yang lebih besar di sebelah kanan posisi i
        for j in range(i + 1, jumlah):
            # Membandingkan nilai fitness pada indeks j dengan posisi_terbesar
            if daftar_fitness[indeks_terurut[j]] > daftar_fitness[indeks_terurut[posisi_terbesar]]:
                # Memperbarui posisi_terbesar jika ditemukan fitness yang lebih tinggi
                posisi_terbesar = j
        # Menukar posisi indeks agar individu dengan fitness tertinggi berada di depan
        sementara = indeks_terurut[i]
        indeks_terurut[i] = indeks_terurut[posisi_terbesar]
        indeks_terurut[posisi_terbesar] = sementara
    # Mengembalikan daftar indeks individu yang sudah terurut menurun berdasarkan fitness
    return indeks_terurut


# --- 2.4 PROSES 7: PERGANTIAN GENERASI / SELEKSI SURVIVOR 
def pergantian_generasi(populasi_lama, daftar_fitness, ukuran_pop, jumlah_elit,
                        ukuran_turnamen, prob_crossover, prob_mutasi):
    # Mengurutkan indeks populasi lama dari fitness tertinggi ke terendah
    indeks_urut = urutkan_indeks_berdasarkan_fitness(daftar_fitness)
    # Menyiapkan list kosong untuk populasi generasi baru (Generational Model)
    populasi_baru = []

    # Tahap Elitisme (Slide 77-78): menyalin langsung individu terbaik ke populasi baru
    for i in range(jumlah_elit):
        # Mengambil indeks individu terbaik ke-i
        indeks_elit = indeks_urut[i]
        # Menyalin kromosom elit ke dalam populasi generasi baru tanpa diubah
        populasi_baru.append(populasi_lama[indeks_elit][:])

    # Tahap Pembentukan Anak Baru hingga jumlah populasi baru mencapai ukuran_pop (100)
    while len(populasi_baru) < ukuran_pop:
        # Memilih Orangtua 1 menggunakan Tournament Selection
        orangtua_1 = pilih_orangtua(populasi_lama, daftar_fitness, ukuran_turnamen)
        # Memilih Orangtua 2 menggunakan Tournament Selection
        orangtua_2 = pilih_orangtua(populasi_lama, daftar_fitness, ukuran_turnamen)
        # Melakukan pindah silang (Single-Point Crossover) untuk menghasilkan 2 anak
        anak_1, anak_2 = pindah_silang(orangtua_1, orangtua_2, prob_crossover)
        # Melakukan mutasi biner (Bit-Flip Mutation) pada Anak 1
        anak_1 = mutasi(anak_1, prob_mutasi)
        # Melakukan mutasi biner (Bit-Flip Mutation) pada Anak 2
        anak_2 = mutasi(anak_2, prob_mutasi)
        # Memasukkan Anak 1 ke dalam populasi generasi baru
        populasi_baru.append(anak_1)
        # Jika populasi baru masih kurang dari ukuran_pop, masukkan juga Anak 2
        if len(populasi_baru) < ukuran_pop:
            populasi_baru.append(anak_2)

    # Mengembalikan populasi generasi baru yang siap menggantikan populasi lama
    return populasi_baru


# --- 2.5 LOOP UTAMA EVOLUSI & PENCETAKAN OUTPUT PROGRAM ---
def jalankan_algoritma_genetika():
    # Menetapkan seed bilangan acak agar hasil eksekusi konsisten dengan laporan
    random.seed(RANDOM_SEED)

    # Menampilkan header informasi program dan parameter GA
    print("=" * 76)
    print("  PROGRAM ALGORITMA GENETIKA - CASE BASED SEARCHING (MINIMASI FUNGSI)")
    print("  Anggota Kelompok: 1. Farhan Kurniawan  |  2. Ammar Dzaki")
    print("=" * 76)
    print(f"  Ukuran Populasi (u_p)    : {UKURAN_POPULASI} individu")
    print(f"  Panjang Kromosom         : {PANJANG_KROMOSOM} bit ({BIT_PER_VARIABEL} bit x1 + {BIT_PER_VARIABEL} bit x2)")
    print(f"  Domain Variabel [rb, ra] : [{BATAS_BAWAH}, {BATAS_ATAS}]")
    print(f"  Seleksi Orangtua         : Tournament Selection (k = {UKURAN_TURNAMEN})")
    print(f"  Rekombinasi & Mutasi     : 1-Point (Pc = {PROB_CROSSOVER}) & Bit-Flip (Pm = 1/{PANJANG_KROMOSOM})")
    print(f"  Seleksi Survivor         : Generational Replacement + Elitisme ({JUMLAH_ELIT} elit)")
    print(f"  Kriteria Penghentian     : Maks {MAKS_GENERASI} generasi atau {MAKS_STAGNAN} generasi stagnan")
    print("=" * 76)

    # Langkah 1: Membangkitkan populasi awal secara acak
    populasi = inisialisasi_populasi(UKURAN_POPULASI, PANJANG_KROMOSOM)

    # Menyiapkan variabel pelacak solusi terbaik sepanjang evolusi
    kromosom_terbaik_global = None
    fitness_terbaik_global = None
    hitung_stagnan = 0
    generasi_terakhir = 0

    print("\n  [PROGRES EVOLUSI PER GENERASI]")
    print("  --------------------------------------------------------------------------")
    print("  Generasi |     Phenotype x1 |     Phenotype x2 |    Nilai Min f(x1, x2)")
    print("  --------------------------------------------------------------------------")

    # Langkah 2: Memulai perulangan evolusi dari generasi ke-1 sampai MAKS_GENERASI
    for generasi in range(1, MAKS_GENERASI + 1):
        # Menyimpan nomor generasi saat ini
        generasi_terakhir = generasi

        # Menghitung nilai fitness untuk seluruh individu di dalam populasi
        daftar_fitness = []
        for individu in populasi:
            nilai_fit = hitung_fitness(individu, BIT_PER_VARIABEL, BATAS_BAWAH, BATAS_ATAS)
            daftar_fitness.append(nilai_fit)

        # Mencari individu dengan nilai fitness tertinggi pada generasi saat ini secara manual
        indeks_terbaik_gen = 0
        for i in range(1, len(daftar_fitness)):
            if daftar_fitness[i] > daftar_fitness[indeks_terbaik_gen]:
                indeks_terbaik_gen = i

        fitness_terbaik_gen = daftar_fitness[indeks_terbaik_gen]
        kromosom_terbaik_gen = populasi[indeks_terbaik_gen]

        # Memeriksa apakah ditemukan solusi baru yang lebih baik dari generasi sebelumnya
        if fitness_terbaik_global is None or fitness_terbaik_gen > fitness_terbaik_global:
            # Memperbarui nilai fitness dan kromosom terbaik global
            fitness_terbaik_global = fitness_terbaik_gen
            kromosom_terbaik_global = kromosom_terbaik_gen[:]
            # Mereset penghitung stagnasi kembali ke 0 karena ada peningkatan fitness
            hitung_stagnan = 0
        else:
            # Jika tidak ada perbaikan fitness terbaik, tambah penghitung stagnasi
            hitung_stagnan = hitung_stagnan + 1

        # Menampilkan log progres pada generasi awal, kelipatan 20, atau saat berhenti
        if generasi == 1 or generasi % 20 == 0 or hitung_stagnan >= MAKS_STAGNAN or generasi == MAKS_GENERASI:
            x1_log, x2_log = dekode_kromosom(kromosom_terbaik_global, BIT_PER_VARIABEL, BATAS_BAWAH, BATAS_ATAS)
            f_log = hitung_fungsi_objektif(x1_log, x2_log)
            print(f"     {generasi:3d}   |    {x1_log:13.6f} |    {x2_log:13.6f} |       {f_log:16.6f}")

        # Langkah 3: Memeriksa kriteria penghentian evolusi akibat stagnasi (50 generasi)
        if hitung_stagnan >= MAKS_STAGNAN:
            break

        # Langkah 4: Melakukan pergantian generasi untuk membentuk populasi generasi berikutnya
        if generasi < MAKS_GENERASI:
            populasi = pergantian_generasi(
                populasi,
                daftar_fitness,
                UKURAN_POPULASI,
                JUMLAH_ELIT,
                UKURAN_TURNAMEN,
                PROB_CROSSOVER,
                PROB_MUTASI,
            )

    print("  --------------------------------------------------------------------------")

    # Langkah 5: Mendekode kromosom terbaik untuk memperoleh nilai x1 dan x2 akhir
    x1_terbaik, x2_terbaik = dekode_kromosom(
        kromosom_terbaik_global, BIT_PER_VARIABEL, BATAS_BAWAH, BATAS_ATAS
    )
    nilai_f_minimum = hitung_fungsi_objektif(x1_terbaik, x2_terbaik)

    # Mengubah list biner kromosom terbaik menjadi untai teks (string) agar rapi ditampilkan
    untai_kromosom_utuh = "".join(str(bit) for bit in kromosom_terbaik_global)
    untai_gen_x1 = "".join(str(bit) for bit in kromosom_terbaik_global[:BIT_PER_VARIABEL])
    untai_gen_x2 = "".join(str(bit) for bit in kromosom_terbaik_global[BIT_PER_VARIABEL:])

    # Menampilkan Output Utama Program sesuai ketentuan soal Case Based - Searching
    print("\n" + "=" * 76)
    print("  OUTPUT PROGRAM (HASIL AKHIR OPTIMASI ALGORITMA GENETIKA)")
    print("=" * 76)
    print(f"  Evolusi Berhenti pada      : Generasi ke-{generasi_terakhir}")
    print(f"  1. Kromosom Terbaik (36bit): {untai_kromosom_utuh}")
    print(f"     - Segmen Bit x1 (18bit) : {untai_gen_x1}")
    print(f"     - Segmen Bit x2 (18bit) : {untai_gen_x2}")
    print("  2. Hasil Dekode Kromosom Terbaik (Phenotype):")
    print(f"     - Nilai x1              : {x1_terbaik:.8f}")
    print(f"     - Nilai x2              : {x2_terbaik:.8f}")
    print("  3. Evaluasi Fungsi & Fitness:")
    print(f"     - Nilai Minimum f(x1,x2): {nilai_f_minimum:.8f}")
    print(f"     - Nilai Fitness Terbaik : {fitness_terbaik_global:.8f}")
    print(f"     - Nilai (x1 + x2)       : {x1_terbaik + x2_terbaik:.8f} rad (dekat asimtot -pi/2)")
    print("=" * 76)


# Menjalankan fungsi utama program ketika file dieksekusi langsung
if __name__ == "__main__":
    jalankan_algoritma_genetika()

