
# import module
from pdf2image import convert_from_path
import os
 
 
# Store Pdf with convert_from_path function
folder = 'pdfs'
folder_to = 'receipts'
# get all pdfs
pdfs = [f for f in os.listdir(folder) if f.endswith('.pdf')]
for pdf in pdfs:
    print('Converting ' + pdf + ' to images...')
    images = convert_from_path(folder + '/' + pdf)

    # Save pages as images in the pdf
    for i in range(len(images)):
        # Save pages as images in the pdf
        images[i].save(folder_to + '/' + pdf + str(i) + '.jpg', 'JPEG')
        print('Saved ' + pdf + str(i) + '.jpg')