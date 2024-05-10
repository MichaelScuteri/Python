import hashlib
import sys

hashfile = sys.argv[1]
wordfile = sys.argv[2]
hash_type = sys.argv[3]
hashlist = open(hashfile, "r")
wordlist = open(wordfile, "r")
hash_list = []
crack_check = 0

def init(crack_check):
    for hash in hashlist:
        hash_list.append(hash)

    for word in wordlist:
        word = word.strip()
        select_hash(word, crack_check)

def select_hash(crack_check, word):
        if hash_type == "md5":
            guess = hashlib.md5(word.encode('utf-8')).hexdigest()   
            main(crack_check, guess, word)
                  
        if hash_type == "sha256":
            guess = hashlib.sha256(word.encode('utf-8')).hexdigest()
            main(crack_check, guess, word)

def main(crack_check, guess, word):
    for hash in hash_list:
            hash = hash.strip()
            if guess == hash:
                    crack_check = crack_check + 1
                    print(f'Password found: {word} | {hash} {hash_type}') 
    if crack_check == 0:
            print("No password found")

init(crack_check)