from letter_processor import LetterProcessor
from gemini import model_classify, model

lprocessor = LetterProcessor('Hasil', 'Dataset/surat.csv')
lprocessor.make_datasets(model_classify)
# lprocessor.make_letter_text(model)