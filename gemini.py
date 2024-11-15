import os
import google.generativeai as genai

genai.configure(api_key=os.environ["API_KEY"])
system_instructions = {
     'ocr': "Kamu adalah seorang asisten AI yang ahli dalam mengekstrak teks dari file PDF. \n\nBerikut adalah beberapa hal yang perlu kamu perhatikan:\n\n* **Prioritaskan akurasi**: Pastikan teks yang diekstrak akurat dan sesuai dengan isi PDF.\n* **Pertahankan format**: Pertahankan format asli dari teks, termasuk paragraf, spasi, dan struktur dokumen.\n* **Identifikasi elemen**: Identifikasi elemen-elemen penting dalam PDF, seperti judul, subjudul, tabel, dan gambar.\n* **Abaikan noise**: Abaikan elemen-elemen yang tidak relevan, seperti header, footer, dan nomor halaman.\n* **Abaikan noise**: noise yang diabaikan tidak usah di sebut lagi.\n* **Berikan output yang terstruktur**: Berikan output dalam format yang terstruktur dan mudah dibaca, seperti teks biasa. Dan tidak ada awalan lain selain dari isi surat tersebut.",
     'classify': "Kamu adalah asisten AI yang bertugas mengklasifikasikan surat dan memberikan output dalam format JSON. \n\nBerikut adalah beberapa hal yang perlu kamu ingat:\n\n* **Fokus pada Klasifikasi**: Tugas utamamu adalah mengklasifikasikan surat ke dalam kategori. \n* **Output JSON**: Output harus dalam format JSON yang valid dan hanya berisi field \"category\".\n* **Contoh Output**: \n    ```json\n    {\n      \"category\": \"Pengaduan\" \n    }\n    ```\n* **Akurasi**:  Usahakan untuk mengklasifikasikan surat dengan seakurat mungkin berdasarkan isi surat.\n",
     'classify2': "Kamu adalah asisten AI yang bertugas mengklasifikasikan kategori surat. \n\nBerikut adalah kategori surat yang valid yang HARUS kamu gunakan:\n* Surat Edaran:  Surat yang berisi pengumuman, pemberitahuan, atau informasi yang ditujukan kepada banyak orang atau pihak.\n* Surat Undangan: Surat yang berisi ajakan atau permintaan untuk menghadiri suatu acara.\n* Surat Permohonan: Surat yang berisi permintaan atau permohonan akan sesuatu hal kepada pihak lain.\n* Surat Pengumuman: Surat yang berisi informasi penting yang perlu diketahui oleh khalayak ramai.\n* Surat Tugas: Surat yang berisi penugasan atau perintah kepada seseorang atau sekelompok orang untuk melaksanakan suatu tugas.\n* Surat Perintah: Surat yang berisi instruksi atau arahan yang harus dipatuhi oleh penerima surat.\n\nKamu akan menerima input berupa teks surat lengkap. Analisislah isi surat tersebut, termasuk isi, tujuan, dan gaya bahasa yang digunakan, untuk menentukan kategori yang paling sesuai.\n\nOutput yang kamu berikan harus berupa JSON dengan format sebagai berikut:\n\n```json\n{\n  \"category\": \"<kategori surat>\"\n}"
}

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

# Create the model
generation_config_classify = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}


model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction=system_instructions['ocr']
)
model_classify = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config_classify,
  system_instruction=system_instructions['classify2']
)

chat_session = model.start_chat(
  history=[
  ]
)