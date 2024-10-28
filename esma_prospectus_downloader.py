import os 
import pandas as pd

from utils import download_pdf
from config import CONFIG_DICT


def main():
    # create downloads folder if it does not exist 
    os.makedirs(os.path.dirname(CONFIG_DICT['DOC_DOWNLOADS_FOLDER']), exist_ok=True)

    # load metadata csv 
    assert os.path.exists(
        CONFIG_DICT['DATA_FOLDER'] + CONFIG_DICT['METADATA_RESULT_CSV']
    ), 'There is no metadata file yet.'

    metadata_df = pd.read_csv(
        CONFIG_DICT['DATA_FOLDER'] + CONFIG_DICT['METADATA_RESULT_CSV'], 
        encoding="utf-8", sep=";"
    )

    for _, row in metadata_df.iterrows():
        download_url = row['physical_doc_downl_url']
        write_file = CONFIG_DICT['DOC_DOWNLOADS_FOLDER'] + row['file_name']
        # check if file exists 
        if not os.path.exists(write_file):
            download_pdf(download_url, write_file)
        else: 
            print(f'{write_file} already exists, skip.')


if __name__ == '__main__':
    main()