import os 
import pandas as pd

from config import CONFIG_DICT


def main():
    # create downloads folder if it does not exist 
    os.makedirs(os.path.dirname(CONFIG_DICT['DOC_DOWNLOADS_FOLDER']), exist_ok=True)

    # load metadata csv 
    assert os.path.exists(
        CONFIG_DICT['DATA_FOLDER'] + CONFIG_DICT['METADATA_RESULT_CSV']), 'There is no metadata file yet.'

    metadata_df = pd.read_csv(
        CONFIG_DICT['DATA_FOLDER'] + CONFIG_DICT['METADATA_RESULT_CSV'], 
        encoding="utf-8", sep=";"
    )

    print(metadata_df)


if __name__ == '__main__':
    main()