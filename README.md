# Retrieval Augmented Generation Fundamental
Ini adalah Repository tentang penerapan RAG menggunakan Langchain, tujuan utama dalam pembangunan RAG ini adalah hanya untuk kebutuhan edukasi menambahkan pengetahuan tentang bagaimanana implementasi terhadap pipeline untuk merancang sebuah aplikasi yang berkekuatan LLM

Langkah - langkah dalam membangun pipeline di repository ini adalah sebagai berikut:
- `Dockerfile` adalah file berisi image untuk menginstall `uv` dari debian trixie.
- menyediakan beberapa kebutuhan dokumen sebagai pengetahuan utama yang disimpan ke dalam database.
- menggunakan API pathlib sebagai pembaca sebuah dokumen.
- penggunaan postgresql dan psycopg2 sebagai penyimpan konteks yang disimpan dalam query language dengan beberapa kolom seperti `chunk_id`, `context`, `source`, `filename` dan `embedding`.
- menghasilkan embedding dari API client `gemini-embedding-001`

Cara untuk menggunakannya:
- `docker build -t pyimage:latest .`
- 
```
    mkdir /to/path
    docker run -d --rm --name pyrag -v $(pwd):/workspace pyimage:latest
    docker run -d --rm --name postgresql \
    -e POSTGRESQL_USER="user" \
    -e POSTGRESQL_PASSWORD="pass" \
    -e POSTGRESQL_DB="nama_db"
    -v /to/path:/var/lib/postgresql \
    -p 5432:5432 \
    pgvector/pgvector:pg18-trixie
```

- Jika mempunyai konfigurasi lain silahkan untuk menambahkan sesuai dengan kebutuhan developer
