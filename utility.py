import os
import logging

logging.getLogger('img2pdf').setLevel(logging.ERROR)

# mengurutkan file didalam folder
def file_sort(folder_path):
     filenames = []
     for file in os.listdir(folder_path):
          filenames.append(folder_path+'/'+file)
     filepop = filenames.pop()
     filenames.insert(0, filepop)
     return filenames

# mengambil daftar folder
# menggabung nama file dan folder tempatnya
def separate_files_and_folders(folder_path):
     folders = []
     files = []
     for file in os.listdir(folder_path):
          if os.path.isdir(folder_path+'/'+file):
               folders.append(folder_path+'/'+file)
          else:
               files.append(folder_path+'/'+file)
     return {
          'folders': folders,
          'files': files
     }

# membuat file
def make_text_file(path, file_name, text):
     validate_directory(path)
     with open(path+'/'+file_name+'.txt', 'w', encoding='utf-8') as history_file:
          history_file.write(text)

# Periksa apakah folder sudah ada
def validate_directory(folder_path):
     if not os.path.exists(folder_path):
          os.makedirs(folder_path) # Buat folder jika belum ada