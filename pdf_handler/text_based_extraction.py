import pymupdf
import fitz
import pathlib
import dotenv
import os

dotenv.load_dotenv()

def text_extraction(file):

    doc=pymupdf.open(file)
    if not doc:
        doc=fitz.open(file)
    '''text=''

    for page in doc:
        text+=page.get_text('text')+'\n'
    doc.close()'''
    return doc.page_count

if __name__=='__main__':
    path=pathlib.Path(os.getenv('FILE_PATH'))
    if not path.exists():
        print(f"Still can't find it. I'm looking at: {path.resolve()}")
    else:
        print(text_extraction(path))
