import os
from PyPDF2 import PdfReader, PdfWriter,PdfMerger

def compressPdf(fileName, path=''):
    file_path = f'{path}{fileName}'

    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()
        writer.add_page(page)

    with open(f"{file_path[:-4]}_compressed.pdf", "wb") as f:
        writer.write(f)

def encryptPdf(fileName, path=''):
    file_path = f'{path}{fileName}'

    reader = PdfReader(file_path)
    writer = PdfWriter()

    # make sure file is not encrypted
    if not(reader.is_encrypted):
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(input("Password: "))

        with open(f'{file_path[:-4]}_encrypted.pdf', 'wb') as f:
            writer.write(f)
    else:
        print('File already encrypted')

def decryptPdf(fileName, path=''):
    file_path = f'{path}{fileName}'

    reader = PdfReader(file_path)
    writer = PdfWriter()

    # make sure file is encrypted
    if reader.is_encrypted:
        reader.decrypt(input("Password: "))

        for page in reader.pages:
            writer.add_page(page)

        with open(f'{file_path[:-4]}_decrypted.pdf', 'wb') as f:
            writer.write(f)
    else:
        print('File not encrypted')

DEFAULT_EXTRACTED_IMAGES_DIR_NAME = 'extracted_images'

def extractImagesFromPdf(fileName, path=''):
    reader = PdfReader(f'{path}{fileName}')

    # create folder if not exists
    if not(os.path.exists(f'./{path}{DEFAULT_EXTRACTED_IMAGES_DIR_NAME}')):
        os.mkdir(F'{path}{DEFAULT_EXTRACTED_IMAGES_DIR_NAME}')

    for page in reader.pages:
        count = 0
        for image_file_object in page.images:
            with open(f'{path}{DEFAULT_EXTRACTED_IMAGES_DIR_NAME}/{count}{image_file_object.name}', "wb") as fp:
                fp.write(image_file_object.data)
                count += 1

def mergePdf(fileArray, outputFileName='Combined_PyPDF2.pdf', path=''):
    merger = PdfMerger()

    # add file to merger object
    for file in fileArray:
        if file.endswith('.pdf'):
            merger.append(f'{path}{file}')

    # make sure output file name is valid
    INVALID_CHARACTER = "#%&{}\<>*?/$'\":@`|="
    if outputFileName == '':
        outputFileName = 'Combined_PyPDF2.pdf'
    else:
        if not(outputFileName.endswith('.pdf')):
            outputFileName += '.pdf'
        for character in INVALID_CHARACTER:
            outputFileName = outputFileName.replace(character, '')

    # merge to new file
    merger.write(f'{path}{outputFileName}')
    merger.close()

def readMetadataPdf(fileName, path=''):
    file_path = f'{path}{fileName}'

    reader = PdfReader(file_path)
    meta = dict()
    meta['author'] = reader.metadata.author
    meta['creator'] = reader.metadata.creator
    meta['producer'] = reader.metadata.producer
    meta['subject'] = reader.metadata.subject
    meta['title'] = reader.metadata.title
    meta['page_count'] = len(reader.pages)

    return meta

def writeMetadataPdf(fileName, newMetadata, path=''):
    file_path = f'{path}{fileName}'

    reader = PdfReader(file_path)
    writer = PdfWriter()

    for page in reader.pages:
        writer.add_page(page)

    # Add the metadata
    writer.add_metadata(
        {
            "/Author": "Martin",
            "/Producer": "Libre Writer",
        }
    )

    # Save the new PDF to a file
    with open("meta-pdf.pdf", "wb") as f:
        writer.write(f)

# def extractTextFromPdf():
#     from PyPDF2 import PdfReader

#     reader = PdfReader("example.pdf")
#     page = reader.pages[0]
#     print(page.extract_text())