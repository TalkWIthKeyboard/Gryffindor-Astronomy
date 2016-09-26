import hashlib

def get_md5(str1=None):
    md5 = hashlib.md5()
    md5.update(str1)
    return md5.hexdigest()
