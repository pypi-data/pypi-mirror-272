class zipfiles():
  def crack_using_wordlist(zip_file, wordlist_path): #type:ignore
    from tqdm import tqdm
    import zipfile
    from .colorcodes import colorcodes
    import os
    #type:ignore
    if not os.path.exists(wordlist_path):
        raise FileNotFoundError(colorcodes.red('Invalid Wordlist Path.'))#type:ignore
    zip_file = zipfile.ZipFile(zip_file) #type:ignore
    n_words = len(list(open(wordlist_path, "rb")))
    print("Total passwords to test:", n_words)
    with open(wordlist_path, "rb") as wordlist:
        for word in tqdm(wordlist, total=n_words, unit="word"):
            try:
                zip_file.extractall(pwd=word.strip())
            except Exception:
                continue
            else:
                print("[+] Password found:", word.decode().strip())
                exit(0)
        print("[!] Password not found, try other wordlist.")


  