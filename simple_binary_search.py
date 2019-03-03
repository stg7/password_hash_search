#!/usr/bin/env python3
import sys
import argparse
import mmap


def find_hash_nearby(hfmap, position):
    k = position
    while hfmap[k] != ord("\r") and k < len(hfmap):
        k += 1
    i = position
    while hfmap[i] != ord("\r") and i > 0:
        i -= 1
    hashline = str(hfmap[i+2:k], encoding="utf-8")
    if len(hashline) == 0:
        return "", 0
    hashstr, hashcount = hashline.split(":")
    return hashstr, int(hashcount)


def search(databasefile, hash_to_search):
    with open(databasefile, "r+") as hfp:
        hfmap = mmap.mmap(hfp.fileno(), 0)
        left = 0
        right = len(hfmap) - 1
        c = 0
        while right - left > 40:
            mid = left + (right - left) // 2 + 1
            hstr, hctn = find_hash_nearby(hfmap, mid)
            if hstr == hash_to_search:
                return hstr, hctn, c
                break
            if hstr < hash_to_search:
                left = mid
            else:
                right = mid
            c += 1
        hfmap.close()


def main(_):
    # argument parsing
    parser = argparse.ArgumentParser(description='binary search of password hashes',
                                     epilog="stg7 2019",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--hashdatabase", type=str, default="./download/pwned-passwords-sha1-ordered-by-hash-v4.txt", help="text file for password hashes")
    parser.add_argument("searchhash", type=str, help="hash that should be checked")
    a = vars(parser.parse_args())

    if not os.path.isfile(a["hashdatabase"]):
        print(f"password database does not exists: {a['hashdatabase']}")
        return -1

    print(f"open password database: {a['hashdatabase']}")
    print(f"check hash: {a['searchhash']}")
    hstr, hctn, steps = search(a["hashdatabase"], a["searchhash"])
    print(f"found hash with {steps} checks")
    print(hstr, hctn)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
