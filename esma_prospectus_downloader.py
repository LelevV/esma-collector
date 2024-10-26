import os 

from config import CONFIG_DICT


def main():
    os.makedirs(os.path.dirname(CONFIG_DICT['DOC_DOWNLOADS_FOLDER']), exist_ok=True)


if __name__ == '__main__':
    main()