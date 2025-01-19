# import dependencies
import verbatim as vb

# confirm which step the user would like to execute
print("Please select a mode for verbatim")
print("1: Convert new PDF documents to images for bounding box annotation")
print("2: Extract text from PDF documents which have been annotated")
# print("3: Convert extracted text to audio file")
mode_select = input("Select Mode (1 / 2)")

# TODO: add a master table to the database for faster lookup

if mode_select == '1':
    # convert new pdfs to images for further processing
    vb.pdf_to_img()
if mode_select == '2':
    # read in image and annotation to extract text
    vb.img_to_txt()
if mode_select == '3':
    # convert text to audio and save various metadata

