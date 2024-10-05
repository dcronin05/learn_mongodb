import lib
from lib import json_cursor, json_file

existing, inserted, duplicates = 0, 0, 0

def insert_tag(r):
    type = "tag"
    pk = r['pk']
    name = r['name']

    lib.db.insert_one({
        'type': type,
        'pk': pk,
        'name': name
    })

def insert(r):
    global inserted
    type = "document"
    pk = r['pk']
    check = r['check']
    content = r['content']
    title = r['title']

    lib.db.insert_one({'type': type, 
                       'title': title,
                       "content": content,
                       "checksum": check,
                       "pk": pk})
    inserted = inserted + 1

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
    tags = r['tags']
    pk = r['pk']
    name = r['title']
    markdown = r['content']
    check = r['check']

    t_list = []
    for tag in tags:
        t_list.append(
            {"name": "pk", "value": str(tag)}
        )
    
    mongo_tag = lib.db.find_one({"type": "tag", "pk": pk})
    if mongo_tag:
        chapter_id = lib.api.post_chapters_create({
            'book_id': 3,
            'name': mongo_tag['name'],
            'tags': [{"name": "pk", "value": pk}]
        })

    try: chapter_id
    except NameError: chapter_id = None

    request = lib.api.post_pages_create({
        'chapter_id': chapter_id['id'] if chapter_id else "",
        'tags': t_list if len(tags) > 0 else "[]",
        'book_id': 3,
        'page_id': pk,
        'name': name,
        'markdown': markdown,
    })

    if 'error' in request:
        print("\n\ndidn't work: ")
        print(request['error']['message'])
        print(t_list)
    else: print("\n\nWorked: \n", t_list, "\n", request['name'])

def tag_exists(t):
    tag = lib.db.find_one({"pk": t['pk']})
    return True if tag else False

def parse():
    f = json_file()
    print("Parsing manifest json...")
    r = {}
    # for every document in the export
    for doc in json_cursor(f):
        fields = doc['fields']
        if doc['model'] == 'documents.tag':
            tag = {'name': fields['name'], 'pk': doc['pk']}
            if tag_exists(tag):
                pass
            else:
                insert_tag(tag)
            
        if 'title' in fields and 'content' in fields \
                and doc['model'] == 'documents.document' \
                and lib.sys.getsizeof(fields['content']) < 16777216:
            
            r['tags'] = doc['fields']['tags']
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