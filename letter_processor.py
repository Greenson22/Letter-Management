import os
from tqdm import tqdm
import google.generativeai as genai
from utility import make_text_file, validate_directory
import csv
import json
import time

# Kelas LetterProcessor ini dirancang untuk memproses surat-surat pdf dan txt
# dan mengkategorikannya menggunakan model AI Gemini
class LetterProcessor:
    def __init__(self, folder_path='Sample', dataset_path='Dataset/surat.csv'):
        self.folder_path = folder_path
        self.dataset_path = dataset_path
        self.history = []

    # menulis ke history
    def write_history(self, text):
        with open(self.folder_path + '/history.text', 'a') as history_file:
            history_file.write(text + '\n')

    # menulis error ke history
    def write_error_history(self, text):
        with open(self.folder_path + '/error_history.text', 'a') as history_file:
            history_file.write(text + '\n')

    # membuat dataset dari file-file leter text
    def make_datasets(self, model):
        archive = [['no', 'category', 'letter_content']] # menyimpan semua text surat yang ada
        # melakukan iterasi terhadap semua file yang ada di folder
        for index, file in enumerate(tqdm(os.listdir(self.folder_path+'/letter_text'))):
            if file.endswith('.txt'):
                with open(self.folder_path+'/letter_text/'+file, 'r', encoding='utf-8') as text_file:
                    letter_content = text_file.read() # mengambil isi dari file letter
                    
                    # melakukan generate content dengan gemini api
                    # untuk melakukan clasifikasi
                    status = {'running': True, 'error':False}
                    while status['running']:
                        status['error'] = False
                        try:
                            response = model.generate_content([letter_content])# melakukan clasifikasi terhadap surat
                        except Exception as e: #jika terjadi error
                            print(f"\nError processing {file}: {e}")
                            status['error'] = True # mengubah ke error, agar program tidak keluar dari loop
                            time.sleep(10) # menunggu sedikit terhadap api
                        # jika tidak terjadi error maka running dijadikan false
                        if not status['error']:
                            status['running'] = False
                        
                    # menyimpan sementara ke variable archive
                    archive.append([
                        index+1, json.loads(response.text)['category'], letter_content
                    ])
        # membuat file dataset csv di folder dataset
        validate_directory(self.folder_path+'/dataset')
        with open(self.folder_path+'/dataset/mydataset.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerows(archive)

    # membuat file text dari pdf
    def make_letter_text(self, ocr_model):
        for file in tqdm(os.listdir(self.folder_path)):
            if file.endswith('.pdf') and not (file in self.history):
                error = False # untuk mengetahui apakah proses error atau tidak
                try:
                    upload_file = genai.upload_file(self.folder_path + '/' + file)
                    response = ocr_model.generate_content(['', upload_file])
                except Exception as e:
                    print(f"Error processing {file}: {e}")
                    error = True
                
                # pencatatan history dijalankan jika tidak terjadi error
                if not error:
                    self.write_history(file)
                    make_text_file(self.folder_path+'/letter_text', file.replace('.pdf', ''), response.text)
                else:
                    self.write_error_history(file)