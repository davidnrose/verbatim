# install libraries
from pdf2image import convert_from_path
import os
import pandas as pd
from tqdm import tqdm
import csv
import datetime as dt

def pdf_to_img():
    ## IDENTIFY FILES TO PROCESS
    # set location of PDF files - read from
    input_dir = "./data/0_pdf"
    # set location of image write location
    output_dir = "./data/1_img"

    # get list of PDF documents in this folder
    pdf_filenames = os.listdir(input_dir)

    # get list of processed files and compare with processed
    processed = list(pd.read_csv("./database/file_processing.csv")["filename"])
    to_process = [file for file in pdf_filenames if file not in processed]

    print(f"Converting the following PDF ({len(to_process)}) files to image:")
    for f in to_process:
        print(f"Converting: {f}")


    # get length of files in db for assigning id
    db_len = len(processed)

    processed_new = list()

    ## EXTRACT IMAGES AND RENAME FILE
    for count, pdf in enumerate(tqdm(to_process)):

        # get pages from the document
        pages = convert_from_path(f"{input_dir}/{pdf}", 350)

        # rename the original file
        id_num = db_len + count
        id_num = str(id_num).zfill(4)
        prev_path = f"{input_dir}/{pdf}"
        new_name = f"{id_num}_{pdf}"
        new_path = f"{input_dir}/{new_name}"
        os.rename(prev_path, new_path)

        # extract images from document pages
        for i, page in enumerate(pages):
            no_ext = new_name.replace(".pdf", "")
            img_filepath = f"{output_dir}/{no_ext}_{i}.jpg"
            page.save(img_filepath, "JPEG")

        # update database
        row_data = [new_name, "to_image", dt.datetime.now()]
        with open("./database/file_processing.csv", "a") as f:
            writer = csv.writer(f)
            writer.writerow(row_data)




