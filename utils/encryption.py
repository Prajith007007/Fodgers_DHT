import os, random, struct
import glob
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
from fsplit.filesplit import Filesplit
import decryption as de


def encryption(file, decryption = False):
    password = "justAsamplePassword"
    hash = SHA256.new(password.encode('utf-8'))
    key = hash.digest()
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    chunksize = 64 * 1024

    if decryption == False:
        
        name = SHA256.new(file.encode('utf-8'))
        name = str(name.digest())
        outputFile = name
        filesize = os.path.getsize(file)
        with open(file, 'rb') as infile:
            try:
                os.makedirs('sample_encrypted')
            except OSError:
                pass
            with open(os.path.join('sample_encrypted', outputFile), 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(IV)

                while True:
                    chunk = infile.read(chunksize)

                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - (len(chunk) % 16))

                    outfile.write(encryptor.encrypt(chunk))
        sharding(os.path.join('sample_encrypted', outputFile))
    
    else:
        with open(file, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)
            try:
                os.makedirs('decrypted_file')
            except OSError:
                pass
            with open(os.path.join('decrypted_file', file), 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))
                outfile.truncate(origsize)

def sharding(file_name):
    try:
        os.makedirs('sample_sharded')
    except:
        pass
    filesize = int(str(os.path.getsize(file_name)).zfill(16))/4
    fs = Filesplit()
    fs.split(file=file_name, split_size=int(filesize), output_dir="sample_sharded/")

def main():
    path = 'deploy/*'
    dir_path = glob.glob(path)
    print ("Enter Option")
    op = int(input("1. ENCRYPT DATA \n2. DECRYPT DATA \n3. EXIT \n"))
    while op < 3:
        if op == 1:
            for file in dir_path:
                encryption(file)
        if op == 2:
            de.merged()
        op = int(input("1. ENCRYPT DATA \n2. DECRYPT DATA \n3. EXIT \n"))

if __name__ == "__main__":
    main()
