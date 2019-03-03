# analyzing password hashes

It started with an article from heise/ct (see https://www.heise.de/select/ct/2019/05/1551437903574108), however I'm not able to access the full article.
The idea is to check in this dump if a given password is stored and how often it is used, heise/ct propose a python implementation with binary search.
Lets try this.

There is a dump of common used password hashes available, see https://haveibeenpwned.com/Passwords.

Download the dump, where the values are sorted by hashes, e.g. using transmission-cli
```bash
mkdir -p download
transmission-cli https://downloads.pwnedpasswords.com/passwords/pwned-passwords-sha1-ordered-by-hash-v4.7z.torrent -w download/
```

Extract the archive (if you have 7zip and atool installed), you will need a minimum of 24.3 GB free space on your hard-drive:
```bash
atool -x pwned-passwords-sha1-ordered-by-hash-v4.7z
```

Now we can start checking/inspecting the downloaded file.
```bash
head pwned-passwords-sha1-ordered-by-hash-v4.txt
000000005AD76BD555C1D6D771DE417A4B87E4B4:4
00000000A8DAE4228F821FB418F59826079BF368:2
00000000DD7F2A1C68A35673713783CA390C9E93:630
00000001E225B908BAC31C56DB04D892E47536E0:5
00000006BAB7FC3113AA73DE3589630FC08218E7:2
00000008CD1806EB7B9B46A8F87690B2AC16F617:3
0000000A0E3B9F25FF41DE4B5AC238C2D545C7A8:15
0000000A1D4B746FAA3FD526FF6D5BC8052FDB38:16
0000000CAEF405439D57847A8657218C618160B2:15
0000000FC1C08E6454BED24F463EA2129E254D43:40
```

As it can be seen the format is obviously `<HASH>:<COUNT>\NL`.

How can we check if a simple password is stored?
```python3
import hashlib; print(hashlib.sha1(bytes("password", "utf-8")).hexdigest().upper())
# output: 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
```

We use the generated hash and perform a "pure"/"basic" bash search via grep:
```bash
time cat pwned-passwords-sha1-ordered-by-hash-v4.txt | grep "5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8"
# output
# 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8:3645804
# real    0m44,654s
# user    0m15,501s
# sys 0m22,309s
```
The password was used `3645804` times in the source data of this dump, moreover the value fits perfectly with the web-interface of https://haveibeenpwned.com/Passwords.

How many hashes are in total stored?
```bash
time cat pwned-passwords-sha1-ordered-by-hash-v4.txt | wc -l
# output
# 551509767
# real    0m44,723s
# user    0m8,026s
# sys 0m23,694s
```

So there are nearly 552 million password hashes stored.
A full search needs approximately 44s real time on my system.

## Binary Search a given HASH
Lets check with a simple binary search approach, see `simple_binary_search.py`.
```bash
./simple_binary_search.py 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
# output
# open password database: ./download/pwned-passwords-sha1-ordered-by-hash-v4.txt
# check hash: 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8
# found hash with 25 checks
# 5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8 3645804
# real    0m0,044s
# user    0m0,029s
# sys 0m0,011s
```

Binary search needs approximately 11 ms, that's not bad.
However, I wanted to extend the idea to use multiprocessing or a smarter index structure, but it seems that it is already quite fast.


