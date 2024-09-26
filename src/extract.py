import lib

# import paperless database export
raw_manifest = open("/mnt/user/media/paperless/export/manifest.json")
manifest = lib.json.load(raw_manifest)

mongo = lib.pymongo.MongoClient("localhost", 27017)
db = mongo.paperless

# export directory for created md files
directory = '/mnt/user/repos/docs/paperless_export'

def output(t, c):
    db.content.insert_one({"title": t, "content": c})

def parse():
    print("entering parse()")
    # for every document in the export
    for field in manifest:
        #if the title and content tags aren't blank
        if "title" in field["fields"]:
            title = field["fields"]["title"]
            if "content" in field["fields"]:
                content = field["fields"]["content"]
                if content != "" and title != "" and lib.sys.getsizeof(content) < 999999:
                    print(title)
                    output(title, content)
