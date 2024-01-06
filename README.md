# microservice-system-design-tutorial
Mengikuti tutorial Learn Microservice Architecture and System Design with Python &amp; Kubernetes from freecodecamp videos: https://youtu.be/hmkF77F9TLw?si=Z8SQ10JUeZEw2o3Q

API ini adalah MP3 converter. 
Framework dan tools yang digunakan adalah flask, mysql, mongodb, rabbitmq, docker, minikube, kubectl, k9s.


## Service yang ada
### Gateway service
Service ini adalah entrypoint terhadap API ini, yang akan menerima request dari client. Service yang juga akan berkomunikasi dengan internal service dari API ini untuk memenuhi request dari client. 

Endpoint yang terdapat pada service in
- `/login`, `POST`
    Client login melalui endpoint ini, untuk mendapatkan token
- `/upload`, `POST`
    Client upload video melalui endpoint ini. File ini akan disimpan pada mongodb dan pesan akan dibuat pada queue yang akan diconsume oleh service lain
- `/download`, `POST`
    Client mendownload mp3 hasil konversi melalui endpoint ini.
### Authentication service
Server yang berisi logic untuk proses autentikasi
### Converter service
Service berisi logic consumer queue(yang berisi informasi tentang video yang disimpan di mongodb(yang akan dikonversi)), yang akan mengkonversi video
### Notification service
Service berisi logic consumer queue(yang berisi informasi tentang video yang sudah selesai dikonversi), yang akan mengirim notifikasi pada client 
### rabbitmq

Setiap service akan di-containerize menggunakan Docker dan diupload pada dockerhub. Deployment menggunakan minikube. Konfigurasi untuk masing-masing service ditulis pada folder `manifests`

