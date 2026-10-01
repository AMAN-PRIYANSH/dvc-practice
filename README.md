# DVC practice: versioning a data file

Author: Aman Priyansh (PES1UG24AM030)

This repo does the **DVC tutorial** task: create a data file, version it with DVC,
change it, version it again, and switch back to the old version.

## What was done (the tutorial's steps)

**One-time set-up**

```
git init
dvc init
git commit -m "Initialize DVC"
```

**Version 1**

```
echo "version 1" > data.txt
dvc add data.txt                      # DVC hashes the file and moves it to its cache
git add data.txt.dvc .gitignore       # Git only keeps the small .dvc receipt
git commit -m "Add version 1 of data"
git tag -a "v1.0" -m "Data version 1.0"
```

**Version 2**

```
echo "version 2" > data.txt
dvc add data.txt                      # new content -> new md5 hash in data.txt.dvc
git add data.txt.dvc
git commit -m "Update data to version 2"
git tag -a "v2.0" -m "Data version 2.0"
```

**Going back to version 1 (the "double checkout")**

```
git checkout v1.0     # Git brings back the old data.txt.dvc receipt
dvc checkout          # DVC brings back the matching data.txt
```

Result:

```
after git checkout v1.0 + dvc checkout  ->  data.txt says "version 1"
after git checkout main + dvc checkout  ->  data.txt says "version 2"
```

## The two versions

| Git tag | data.txt | md5 hash in data.txt.dvc |
|---|---|---|
| v1.0 | version 1 | 81127ad129dd2249f5ab0667ca0aeb84 |
| v2.0 | version 2 | b04d0b29d4bac0781fe844e328c5e2ac |

## Extra (beyond the tutorial)

1. **DVC remote.** Git (and GitHub) only store the `.dvc` receipt, not the data itself.
   So the data of both versions was pushed with `dvc push` to a storage folder,
   `dvc_storage/`, that is part of this repo. Anyone who clones the repo can get the data
   back with `dvc pull`. In a real project the remote would be S3 or Google Drive.
2. **`show_versions.py`** prints the content of every version straight from DVC,
   without changing any file:

   ```
   v1.0: data.txt says -> 'version 1'
   v2.0: data.txt says -> 'version 2'
   ```

## Try it yourself

```
git clone https://github.com/AMAN-PRIYANSH/dvc-practice.git
cd dvc-practice
pip install -r requirements.txt
dvc pull                      # gets data.txt from the storage folder
dvc remote modify --local storage url dvc_storage   # one-time: lets DVC find the storage folder for old tags too
dvc fetch --all-tags          # also downloads version 1 into DVC's cache
python show_versions.py
git checkout v1.0
dvc checkout                  # data.txt is now "version 1"
git checkout main
dvc checkout                  # back to "version 2"
```
