from fsplit.filesplit import Filesplit
import encryption
import glob
def merged():
    fs = Filesplit()
    fs.merge(input_dir="sample_sharded/", output_file='file')
    path = '*'
    dir_path = glob.glob(path)
    for file in dir_path:
        if file == 'file':
            encryption.encryption(file, decryption=True)