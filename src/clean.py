import os

folders = ["test","kaggle"]
subfolders = ["raw", "temp", "out"]


def clean():
    empty = True
    for folder in folders:
        for subfolder in subfolders:
            currdir = os.path.join("data", folder, subfolder)
            try:
                for filename in os.listdir(currdir):
                    empty = False
                    file_path = os.path.join(currdir, filename)
                    try:
                        os.remove(file_path)
                        print(file_path + " removed!")
                    except Exception as e:
                        print('Failed to delete %s. Reason: %s' % (file_path, e))
            except Exception as e:
                        print('Failed to find folder. Reason: %s' % (e))
    if empty:
        print("No files to delete! 'data' directory empty!")

def make_data_dir():
     for folder in folders:
        for subfolder in subfolders:
            currdir = os.path.join("data", folder, subfolder)
            if not os.path.exists(currdir):
                os.makedirs(currdir)