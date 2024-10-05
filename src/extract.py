import lib
from lib import json_cursor, json_file

existing, inserted, duplicates = 0, 0, 0

def insert(r):
    global inserted
    pk = r['pk']
    check = r['check']
    content = r['content']
    title = r['title']

    lib.db.insert_one({'title': title,"content": content,
                       "checksum": check,
                       "pk": pk})
    inserted = inserted + 1

def update_pk(r):
    lib.db.update_one(
        {
            "checksum": r["check"]
        },
        {
            "$set": {"index": r["index"]}
        }
    )

def rec_exists(r):
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

def create_page(r):
    pk = r['pk']
    name = r['title']
    markdown = r['content']
    check = r['check']

    request = lib.api.post_pages_create({
        'book_id': 3,
        'page_id': pk,
        'name': name,
        'markdown': markdown,
    })

    # if 'message' in request:
    print(request)

def parse():
    f = json_file()
    print("Parsing manifest json...")
    r = {}
    # for every document in the export
    for doc in json_cursor(f):
        fields = doc['fields']
        if 'title' in fields and 'content' in fields:
            r['pk'] = doc['pk']
            r['title'] = fields['title']
            r['content'] = fields['content']
            r['check'] = fields['checksum']

            create_page(r)

            if rec_exists(r):
                continue
            else:
                insert(r)
    f.close()