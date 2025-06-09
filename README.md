NubiCha Media Intelligence Dashboard - Laporan Media Intelligence

Dashboard ini dibuat sebagai bagian dari tugas UAS mata kuliah Deploying Media Intelligence Web App yang dibimbing oleh Dr. Achmad Istamar.

Tujuan
Aplikasi ini bertujuan untuk membantu visualisasi dan analisis data media sosial NubiCha, khususnya data dari berbagai platform media sosial, berdasarkan sentimen, tingkat interaksi (engagement), dan analisis geografis.

Fitur Utama
1. Visualisasi Data Komprehensif
   * Grafik pie distribusi sentimen (positif, negatif, netral) dengan desain modern
   * Grafik batang horizontal engagement per platform dengan gradient colors
   * Grafik garis timeline perubahan engagement dari waktu ke waktu
   * Analisis dual-axis untuk tipe media (total vs rata-rata engagement)
   * Peta panas (heatmap) sentimen per platform
   * Top 10 kota dengan engagement tertinggi

2. Dashboard Overview dengan KPI Cards
   * Total postingan dengan persentase dari dataset
   * Total engagement dengan konversi ke ribuan
   * Rata-rata engagement per postingan
   * Persentase sentimen positif
   * Platform dengan performa terbaik

3. Insight Otomatis dari AI (Enhanced)
   * Analisis mendalam berdasarkan data yang diunggah
   * Rekomendasi strategis yang actionable
   * Menggunakan model gratis deepseek/deepseek-r1-0528-qwen3-8b:free via OpenRouter
   * Mode demo untuk penggunaan tanpa API key

4. Tanya Jawab Interaktif dengan AI
   * Q&A system yang dapat menjawab pertanyaan spesifik tentang data
   * Context-aware responses berdasarkan dataset yang diupload
   * Cocok untuk eksplorasi data lebih lanjut

5. Analisis Geografis
   * Breakdown engagement berdasarkan lokasi
   * Identifikasi market penetration tertinggi
   * Visualisasi top performing cities

6. Filter Data yang Canggih
   * Filter berdasarkan rentang tanggal
   * Multi-select platform, sentimen, dan lokasi
   * Real-time update visualization berdasarkan filter

7. Export & Download Lengkap
   * Download data CSV yang sudah difilter
   * Generate summary report dalam format .txt
   * Export laporan PDF dengan executive summary
   * Download AI insights dalam format .txt

8. UI/UX Modern
   * Glass morphism design pada sidebar
   * Interactive hover effects
   * Gradient color schemes
   * Card-based layout untuk better organization
   * Professional typography dengan Inter font

Cara Menggunakan
1. Jalankan perintah: py -m streamlit run streamlit_app.py
2. Upload file CSV yang berisi kolom wajib: Date, Platform, Sentiment, Engagements, Location, dan Media_Type.
3. Gunakan filter di sidebar untuk menyaring data sesuai kebutuhan.
4. Klik tombol "🚀 Generate Analisis AI" untuk mendapatkan insight mendalam.
5. Manfaatkan fitur "💬 Tanya AI" untuk pertanyaan spesifik tentang data.
6. Gunakan berbagai fitur export untuk menyimpan hasil analisis.

Format Data yang Diperlukan
* Date: Format tanggal (YYYY-MM-DD atau DD/MM/YYYY)
* Platform: Nama platform media sosial (Instagram, TikTok, Twitter, dll)
* Sentiment: Kategori sentimen (Positive, Negative, Neutral)
* Engagements: Jumlah interaksi (likes, comments, shares, dll)
* Location: Lokasi geografis postingan
* Media_Type: Jenis konten (Photo, Video, Text, dll)

Teknologi yang Digunakan
* Python 3.11+
* Streamlit (Web Framework)
* Plotly Express & Graph Objects (Data Visualization)
* Pandas (Data Processing)
* OpenRouter AI API (AI Analysis)
* FPDF (PDF Generation)
* Requests (HTTP Client)
* NumPy (Numerical Computing)

Keunggulan NubiCha Dashboard
* Design modern dengan glass morphism effects
* Comprehensive analytics dengan multiple chart types
* AI-powered insights dengan contextual analysis
* Professional reporting capabilities
* Interactive filtering dan real-time updates
* Mobile-responsive design
* Professional color schemes dan typography

Troubleshooting
* Pastikan file CSV memiliki semua kolom yang diperlukan
* Periksa format tanggal sesuai standar (YYYY-MM-DD atau DD/MM/YYYY)
* Pastikan encoding file adalah UTF-8
* Ukuran file maksimal 200MB
* Untuk fitur AI, diperlukan koneksi internet

Dikerjakan oleh: Meisya Rachmadia
Universitas Indonesia
Program Studi Produksi Media
Semester Genap 2025

---
NubiCha Media Intelligence Dashboard
Professional Social Media Analytics Platform
Version 1.0 - 2025
