from pathlib import Path



def save_img(obj, path_to_save):
    with open(path_to_save, 'wb') as f:
        f.write(obj)
