import os 
from tqdm import tqdm
import img2pdf
from PIL import Image
from utility import separate_files_and_folders, file_sort, validate_directory

class PDFConverter:
     def __init__(self, input_dir='Data', output_dir='Hasil') -> None:
          self.input_dir = input_dir
          self.output_dir = output_dir

     # membuat pdf dari folder
     def make_pdf_from_folder(self):
          print('Membuat pdf dari file dalam folder...')
          folders = separate_files_and_folders(self.input_dir)['folders'] #mengambil daftar folder
          for folder in tqdm(folders):
               # mengganti nama file pdf yang sesuai
               # menggabungkan file image didalam folder dan membuat pdf
               filename = folder.replace(self.input_dir+'/', '').replace(' ', '_masuk')+'.pdf'
               validate_directory(self.output_dir) # mengecek jika folder ada
               with open(self.output_dir+'/'+filename, 'wb') as file:
                    file.write(img2pdf.convert(file_sort(folder)))
          print('Pembuatan pdf dari file dalam folder telah selesai')

     # membuat pdf dari file
     def make_pdf_from_files(self):
          print('Membuat pdf dari file...')
          files = separate_files_and_folders(self.input_dir)['files'] #mengambil daftar files
          for f in tqdm(files):
               # jika menemukan webp, maka ubah ke pdf
               # Kemudian hapus file webp
               if f.endswith('.webp'):
                    image = Image.open(f).convert('RGB')
                    image.save(f.replace('.webp', '.png'), 'png') # melakukan penyimpanan file png yang baru
                    os.remove(f) # menghapus file webp
                    f = f.replace('.webp', '.png') # merubah webp ke png

               # mengganti nama file pdf yang sesuai
               # mengubah file image menjadi pdf
               filename = f.replace(self.input_dir+'/', '').replace(' ', '_masuk').replace('.png', '').replace('.jpg', '').replace('.jpeg', '')+'.pdf'
               validate_directory(self.output_dir) # mengecek jika folder ada
               with open(self.output_dir+'/'+filename, 'wb') as file:
                    file.write(img2pdf.convert([f]))
          print('Pembuatan pdf dari file telah selesai')
     
     # membuat langsung dari file dan folder
     def make_pdf(self):
          self.make_pdf_from_folder()
          self.make_pdf_from_files()