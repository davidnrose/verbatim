import os
import pandas as pd


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

def extract():
    # pdf input location
    pdf_input = "./data/0_pdf"
    # annotation input location
    ann_input = "./data/2_annotate"

    # IDENTIFY UN-EXTRACTED
    log = pd.read_csv("./database/file_processing.csv")
    img = list(log.query("process_step == 'to_image'")["filename"])
    txt = list(log.query("process_step == 'get_text'")["filename"])
    to_process = [f for f in img if f not in txt]

    # identify all annotations
    ann_filenames = os.listdir(ann_input)

    print(to_process)

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

    # write output for inspecting
    df_text.to_csv("output.csv", index=False)








