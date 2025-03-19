# install libraries
from pdf2image import convert_from_path
import os
import pandas as pd
from tqdm import tqdm
import datetime as dt
import pymupdf as pmu
import json
import sys
from csv import writer


# function takes pdf files and converts them to image
def pdf_to_img():
    ## IDENTIFY FILES TO PROCESS
    # set location of PDF files - read from
    input_dir = "./data/0_pdf"
    # set location of image write location
    output_dir = "./data/1_img"

    # get list of PDF documents in this folder
    pdf_filenames = os.listdir(input_dir)

    # get list of processed files and compare with processed
    db = pd.read_csv(r".\database\file_processing.csv", low_memory=False)
    processed = db.query("process_step == 'to_image'")["filename"].unique()
    print(processed)
    to_process = [file for file in pdf_filenames if file not in processed]

    print(f"Found the following PDF ({len(to_process)}) files to image:")
    for f in to_process:
        print(f)

    if len(to_process) == 0:
        print("No new PDF files to convert")
        sys.exit("verbatim ended")

    # get user input to proceed with file processing
    proceed = input("Proceed with converting these pdf files to img? (y/n)")
    if proceed == "n":
        sys.exit("verbatim ended")

    ## EXTRACT IMAGES AND RENAME FILE
    for count, pdf in enumerate(tqdm(to_process)):

        # get pages from the document
        pages = convert_from_path(f"{input_dir}/{pdf}", 350)

        # extract images from document pages
        for i, page in enumerate(pages):
            no_ext = pdf.replace(".pdf", "")
            img_filepath = f"{output_dir}/{no_ext}_{i}.jpg"
            page.save(img_filepath, "JPEG")

        # update database
        row_data = [pdf, "to_image", dt.datetime.now()]
        with open(r".\database\file_processing.csv", "a") as db:
            write_csv = writer(db)
            write_csv.writerow(row_data)

# function to create bounding box points
def make_rect(points):
    x0 = points[0][0]
    y0 = points[0][1]
    x1 = points[1][0]
    y1 = points[1][1]

    rect = [points[0][0], points[0][1], points[1][0], points[1][1]]
    # convert dpi to units for pymupdf
    rect = [(r/350) * 72 for r in rect]

    return rect

def img_to_txt():
    # pdf input location
    pdf_input = "./data/0_pdf"
    # annotation input location
    ann_input = "./data/2_annotate"

    # TODO change this to read from the database
    # TODO add check that annotations are available for images
    # IDENTIFY UN-EXTRACTED
    log = pd.read_csv("./database/file_processing.csv")
    img = list(log.query("process_step == 'to_image'")["filename"])
    txt = list(log.query("process_step == 'get_text'")["filename"])
    to_process = [f for f in img if f not in txt]

    if len(to_process) == 0:
        print("No new PDF files to extract")
        sys.exit("verbatim ended")

    # display files for extraction
    print("Found the following files, and corresponding annotations, for text extraction:")
    for f in to_process:
        print(f)

    # user confirms to proceed with text extraction
    proceed = input("Proceed with extracting text from these pdf files? (y/n)")
    if proceed == 'n':
        sys.exit("verbatim ended")
    if proceed ==  'y':
        pass
    else:
        sys.exit("Commend not recognised. verbatim ended")


    # identify all annotations
    ann_filenames = os.listdir(ann_input)

    # initialise dataframe to store result
    df_text = pd.DataFrame(columns=["filename", "page_no", "label", "text", "bounding_box"])

    # iterate through unprocessed files
    for file in tqdm(to_process):
        # get the filename of file to process
        pdf_filename = file

        # return list of all json annotation files
        fn_no_ext = pdf_filename.replace(".pdf", "")
        ann_json = [a for a in ann_filenames if a.startswith(fn_no_ext)]

        # get the index corresponding to the document page number
        indices = [int(a.replace(".json", "").rsplit("_", 1)[1]) for a in ann_json]

        # load the pdf
        pdf_to_load = f"{pdf_input}/{pdf_filename}"
        doc = pmu.open(pdf_to_load)

        # iterate through the json files and applying extraction to each page
        for idx in indices:
            # get json data
            with open(f"{ann_input}/{fn_no_ext}_{str(idx)}.json", "r") as file:
                ann = json.load(file)

            # get bounding boxes from the json file
            boxes = ann["shapes"]

            # iterate through the shapes and get the text from each
            for bb in boxes:
                # get points and make rectangle
                points = bb["points"]
                rect = make_rect(points)

                # get the corresponding page and extract text
                page = doc[idx]
                text = page.get_textbox(rect)

                # append data to dataframe
                row_data = [pdf_filename, int(idx) + 1, bb["label"], text, rect]
                df_text.loc[len(df_text)] = row_data

    # TODO: write result to a table within the database
    # TODO: give options for writing .csv output as well
    # write output for inspecting
    df_text.to_csv("output.csv", index=False)

def txt_to_pod():
    pass