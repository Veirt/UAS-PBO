# Penjelasan

1. Admin
2. User
3. Dokter

Admin:

- Manajemen User (CRUD user/akun)
- Manajemen Produk (CRUD produk. Produk akan tampil di toko, dan bisa dibeli oleh user)
- Manajemen Hewan Adopsi (CRUD hewan adopsi. Nanti bisa diadopsi oleh user)
- Riwayat Layanan (Bisa lihat riwayat layanan yang dilakukan oleh user, bisa print struk lagi)

User:

- Toko / Belanja (Beli produk, hasil CRUD produk oleh admin)
- Layanan (Cek kesehatan hewan, perawatan hewan. Layanan ini nanti diproses oleh dokter)
- Adopsi (Adopsi hewan, hasil CRUD hewan adopsi oleh admin)

Dokter:

- Lihat Antrean kesehatan (Lihat antrean kesehatan hewan yang akan diperiksa)
- Lihat Antrean perawatan (Lihat antrean perawatan hewan yang akan dirawat)
- Proses Antrean Kesehatan (Memproses/diagnosa hewan. Nanti akan diisi data diagnosa, obat, dll)
- Proses Antrean Perawatan (Memproses/perawatan hewan. Tidak ada input)

## Alur Belanja

1. Admin membuat produk di manajemen produk (jika belum ada datanya sama sekali. cek di data/products.tsv)

---

2. User login
3. User masuk menu "Toko / Belanja"
4. User memasukkan produk ke keranjang (bisa banyak produk)
5. User checkout
6. User memilih metode pembayaran
7. User akan ditampilkan struk pembayaran
8. Selesai

## Alur Adopsi

1. Admin membuat data hewan adopsi di manajemen hewan adopsi (jika belum ada datanya sama sekali. cek di data/pets.tsv)

---

2. User login
3. User masuk menu "Adopsi"
4. User pilih hewan yang ingin diadopsi
5. Data akan tampil dan gambar hewan akan ditampilkan
6. Jika user memilih adopsi, maka lanjut pilih metode pembayaran
   (Perlu kah ada struk pembayaran?)
7. Selesai

## Alur Layanan Cek Kesehatan

1. User login
2. User masuk menu "Layanan"
3. User pilih "Pengecekan Kesehatan Hewan"
4. User pilih "Tambah Antrean Pengecekan Kesehatan"
5. User akan ditampilkan nomor antrean yang diterima

---

6. Dokter Login
7. Dokter bisa cek antrean kesehatan yang ada (menu "Lihat Antrean Kesehatan")
8. Dokter bisa memproses antrean kesehatan (menu "Proses Antrean Kesehatan")
9. Dokter memilih nomor antrean yang akan diproses. (Note: Disini bisa pilih nomor antrean yang mana yang akan diproses, jadi gak harus urut, misal ada emergency mungkin)
10. Dokter mengisi data diagnosa (jenis hewan, nama penyakit, obat, harga)
11. Dokter selesai memproses antrean kesehatan

---

12. User login
13. User masuk menu "Layanan" -> "Pengecekan Kesehatan Hewan"
14. User melakukan pembayaran dengan masuk menu "Pembayaran Penanganan Kesehatan"
15. User memilih data diagnosa yang akan dibayar
16. User memilih metode pembayaran
17. User akan ditampilkan struk pembayaran
18. Selesai

Note: untuk alur perawatan hewan, sama seperti alur kesehatan hewan, hanya saja beda menu & pilih per paket. Tidak ada input diagnosa.
