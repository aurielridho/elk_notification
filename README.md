Panduan Menggunakan Aplikasi ELK Notification

Aplikasi ini bertujuan untuk menampilkan alert pada laptop client ketika rules pada Kibana terdeteksi. Proyek ini melibatkan penggunaan Elasticsearch dan Kibana yang diinstal menggunakan Docker di VM Ubuntu. Aplikasi pluginnya dibuat dengan Python dan juga berjalan di VM.

Prasyarat

1. Docker dan Docker Compose
   - Pastikan Docker dan Docker Compose sudah terinstal di sistem Anda. Untuk panduan instalasi, Anda dapat mengunjungi [Panduan Instalasi Docker](https://docs.docker.com/get-docker/).

2. Git
   - Pastikan Git sudah terinstal di sistem Anda. Untuk panduan instalasi, Anda dapat mengunjungi [Panduan Instalasi Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

Langkah-langkah Instalasi dan Konfigurasi

1. Instalasi ELK Stack

1. Clone Repository ELK Notification
    ```
    git clone https://github.com/aurielridho/elk_notification.git
    cd elk_notification
    ```

2. Setel Parameter Kernel untuk Elasticsearch
    ```
    sudo sysctl -w vm.max_map_count=262144
    ```

3. Download dan Jalankan Elasticsearch dengan Docker
    - Untuk detail download image dan dokumentasi lebih lanjut, kunjungi [Panduan Instalasi ELK Stack](https://www.elastic.co/guide/en/elasticsearch/reference/current/docker.html).
    ```
    docker network create elastic
    docker run --name es01 --network elastic -p 9200:9200 -e "discovery.type=single-node" -it docker.elastic.co/elasticsearch/elasticsearch:8.14.3
    ```

    Credential Elasticsearch:
    - Username: `elastic`
    - Password: `your_password`

4. Jalankan Kibana dengan Docker
    ```
    docker run --name kib01 --network elastic -p 5601:5601 docker.elastic.co/kibana/kibana:8.14.3
    ```

5. Akses Kibana
    - Buka browser dan akses Kibana melalui URL: [http://localhost:5601](http://localhost:5601).

6. Login ke Container Docker sebagai Root
    ```
    docker exec -u 0 -it kib01 bash
    ```

7. Tambahkan Enkripsi untuk Kibana
    - Tambahkan konfigurasi berikut pada file konfigurasi Kibana (`kibana.yml`):
    ```
    xpack.encryptedSavedObjects.encryptionKey: "your-encryption-key"
    ```

2. Konfigurasi Aplikasi ELK Notification

1. Masuk ke dalam Container Kibana
    ```
    docker exec -it kib01 bash
    ```

2. Install Python dan Dependencies
    ```
    apt-get update
    apt-get install -y python3 python3-pip
    pip3 install -r /path/to/your/requirements.txt
    ```

3. Jalankan Aplikasi ELK Notification
    ```
    python3 /path/to/your/application.py
    ```

Penggunaan Aplikasi

1. Mengakses Kibana
    - Buka browser dan akses Kibana melalui URL: [http://localhost:5601](http://localhost:5601).

2. Konfigurasi Rules di Kibana
    - Atur rules sesuai kebutuhan Anda di Kibana.

3. Menjalankan Aplikasi Notification
    - Pastikan aplikasi ELK Notification berjalan di VM Anda.

Troubleshooting

- Jika mengalami masalah, periksa log Docker untuk Elasticsearch, Logstash, dan Kibana:
    ```
    docker logs <container_id>
    ```
- Pastikan semua container berjalan dengan perintah:
    ```
    docker ps
    ```

---

Catatan Khusus:

1. **Credential `basic_auth` pada `elasticsearchmodule.py`:**
   - Gantilah dengan username dan password Anda sendiri yang sesuai dengan konfigurasi Elasticsearch Anda.

2. **API Key Gemini pada `geminiapimodule.py`:**
   - Gantilah dengan API key Anda sendiri. Pastikan API key tersebut valid dan memiliki izin yang diperlukan untuk mengakses Gemini API.

3. **Path Sertifikat pada `elasticsearchmodule.py`:**
   - Pastikan path ke sertifikat CA sesuai dengan lokasi sebenarnya dari sertifikat CA pada sistem Anda.

---
