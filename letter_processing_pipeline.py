from pdf_converter import PDFConverter
from letter_processor import LetterProcessor
from gemini import model, model_classify

class LetterProcessingPipeline:
  """
  Kelas untuk menjalankan pipeline pemrosesan surat, 
  mulai dari konversi PDF hingga pembuatan dataset.
  """
  def __init__(self, input_dir, output_dir, dataset_name, category):
    """
    Inisialisasi objek LetterProcessingPipeline.

    Args:
      input_dir: Direktori input berisi file gambar surat.
      output_dir: Direktori output untuk menyimpan hasil.
      dataset_name: Nama dataset yang akan dibuat.
      category: Kategori surat.
    """
    self.input_dir = input_dir
    self.output_dir = output_dir
    self.dataset_name = dataset_name
    self.category = category
    
    self.pdf_converter = PDFConverter(input_dir=self.input_dir, output_dir=self.output_dir)
    self.letter_processor = LetterProcessor(self.output_dir)


  def run(self):
    """
    Menjalankan pipeline pemrosesan surat.
    """
    # Konversi gambar ke PDF
    self.pdf_converter.make_pdf()

    # Pemrosesan surat
    self.letter_processor.make_letter_text(ocr_model=model)
    self.letter_processor.make_datasets(model=model_classify, dataset_name=self.dataset_name, category=self.category)