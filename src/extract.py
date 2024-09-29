import lib

# import paperless database export
raw_manifest = open("/mnt/user/media/paperless/media/backup/manifest.json")
manifest = lib.json.load(raw_manifest)

# export directory for created md files
directory = '/mnt/user/repos/docs/paperless_export'

index_num = 1

existing, inserted, big, duplicates = 0, 0, 0, 0

def insert(r):
    lib.db.insert_one({"title": r["title"],
                               "content": r["content"],
                               "checksum": r["check"],
                               "index": r["index"]})

def exists(r):
    global existing, duplicates
    record = lib.db.find_one({"checksum": r["check"]})
    dupe = lib.db.find_one({"content": r["content"], "title": r["title"]})

    if dupe:
        if record:
            existing = existing + 1
            return True
        duplicates = duplicates + 1
        return True
    else: return False

def parse():
    global inserted, big, index_num
    print("entering parse()")
    # for every document in the export
    for document in manifest:
        #if the title and content tags aren't blank
        try:
            record = {"title": document["fields"]["title"],
                      "content": document["fields"]["content"],
                      "check": document["fields"]["checksum"],
                      "index": index_num}

            if lib.sys.getsizeof(record["content"]) < 16777216:
                if record["content"] != "" and record["title"] != "":
                    if not exists(record):
                        insert(record)
                        inserted = inserted + 1
                        index_num = index_num + 1
            else: big = big + 1
        except KeyError:
            continue


