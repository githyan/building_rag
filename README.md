# Retrieval Augmented Generation Fundamental
Ini adalah Repository tentang penerapan RAG menggunakan Langchain, tujuan utama dalam pembangunan RAG ini adalah hanya untuk kebutuhan edukasi menambahkan pengetahuantentang bagaimanana implementasi terhadap pipeline untuk merancang sebuah aplikasi yang berkekuatan LLM

Langkah - langkah dalam membangun pipeline di repository ini adalah sebagai berikut:
- menyediakan beberapa kebutuhan dokumen sebagai pengetahuan utama yang disimpan ke dalam database
- menggunakan API pathlib sebagai pembaca sebuah dokumen 
- penggunaan postgresql dan psycopg2 sebagai penyimpan konteks yang disimpan dalam query language dengan beberapa kolom seperti `chunk_id`, `context`, `source`, `filename` dan `embedding` 
- menghasilkan embedding dari API client `gemini-embedding-001`

