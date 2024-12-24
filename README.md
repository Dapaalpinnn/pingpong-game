# Pingpong Game

Game table tennis sederhana yang dibuat menggunakan bahasa pemrograman Python dengan menerapkan konsep pemrograman berorientasi objek, serta library Pygame. Tersedia mode pemain tunggal melawan CPU dan mode dua pemain.

## Features

- Mode pemain tunggal melawan CPU
- Mode multiplayer lokal untuk dua pemain
- Sistem penghitungan skor
- Layar kemenangan dengan opsi main ulang
- Kontrol yang sederhana
- Fisika bola realistis dengan peningkatan kecepatan saat memantul

## Requirement
- Python 3.x
- Library Pygame

## Installation

Clone repository:

```sh
https://github.com/MuhammadDafaAlvin/pingpong-game.git
```

Pindah ke folder proyek
```sh
cd pingpong-game
```

Install Pygame:

```sh
pip install pygame
```

Jalankan game:
```sh
python main.py
```

# Controls
> Menu
- Gunakan mouse untuk memilih mode permainan atau keluar

> Kontrol Dalam Game
- Pemain 1:
  - W: Gerak paddle ke atas
  - S: Gerak paddle ke bawah
- Pemain 2:
  - ↑ (Panah Atas): Gerak paddle ke atas
  - ↓ (Panah Bawah): Gerak paddle ke bawah

> Layar Kemenangan
  - SPACE: Main lagi
  - ESC: Kembali ke menu utama

> Aturan Permainan
  - Pemain pertama yang mencapai 5 poin menang
  - Kecepatan bola meningkat setiap kali memantul di paddle
  - Poin didapat ketika lawan gagal mengembalikan bola
  - Pada mode pemain tunggal, CPU mengendalikan paddle kanan

# Credit
> Lusida Cynthia Winayu (23091397075) |
> Muhammad Dafa Alvin Zuhdi (23091397083) |
> Bahauddin Rahman Hakim (23091397093) 
