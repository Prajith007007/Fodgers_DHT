import os
import glob
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from fsplit.filesplit import FileSplit


def encryption(file):
    password = "justAsamplePassword"
    hash = SHA256.new(password.encode('utf-8'))
    key = hash.digest()
    chunksize = 64 * 1024
    name = SHA256.new(file.encode('utf-8'))
    name = str(name.digest())
    outputFile = name
    filesize = str(os.path.getsize(file)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    with open(file, 'rb') as infile:
        try:
            os.makedirs('sample_encrypted')
        except OSError:
            pass
        with open(os.path.join('sample_encrypted', outputFile), 'wb') as outfile:
            outfile.write(filesize.encode('utf-8'))
            outfile.write(IV)

            while True:
                chunk = infile.read(chunksize)

                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))

                outfile.write(encryptor.encrypt(chunk))
    sharding(os.path.join('sample_encrypted', outputFile))


def sharding(file_name):
    try:
        os.makedirs('sample_sharded')
    except:
        pass
    filesize = str(os.path.getsize(file_name)).zfill(16)
    fs = FileSplit(file=file_name, splitsize=int(
        filesize)/4, output_dir="sample_sharded/")
    fs.split()


def main():
    path = 'deploy/*'
    dir_path = glob.glob(path)
    for file in dir_path:
        encryption(file)


if __name__ == "__main__":
    main()
