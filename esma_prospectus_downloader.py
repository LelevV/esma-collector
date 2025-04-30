import os 
import pandas as pd
import re

from utils import download_pdf
from config import CONFIG_DICT


def clean_filename(filename: str, replacement: str = '_') -> str:
    """
    Remove invalid characters from filename and replace them with `replacement`.
    Keeps letters, numbers, dots, dashes, and underscores.
    """
    # Define invalid characters pattern (anything except allowed chars)
    # Allowed: letters, numbers, dot, dash, underscore
    pattern = r'[^A-Za-z0-9._-]+'
    
    # Replace invalid chars with replacement (default '_')
    cleaned = re.sub(pattern, replacement, filename)
    
    # Optionally, strip leading/trailing dots or spaces (can cause issues)
    cleaned = cleaned.strip(' .')
    
    # Limit length if needed (e.g., max 255 chars)
    max_length = 255
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]
    
    return cleaned



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

    # drop nans 
    metadata_df.dropna(subset=['physical_doc_downl_url'], inplace=True)

    for _, row in metadata_df.iterrows():
        download_url = row['physical_doc_downl_url']
        clean_file_name = clean_filename(row['file_name'])
        print(clean_file_name)
        write_file = CONFIG_DICT['DOC_DOWNLOADS_FOLDER'] + clean_file_name
        # check if file exists 
        if not os.path.exists(write_file):
            download_pdf(download_url, write_file)
        else: 
            print(f'{write_file} already exists, skip.')


if __name__ == '__main__':
    main()