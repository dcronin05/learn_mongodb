from pprint import pprint

import lib

def query(s):

    q = lib.db.find(
        {
            "$or":
            [
                {"content": {"$regex": s}},
                {"title": {"$regex": s}},
                {"index": s if not s.isdigit() else int(s)}
            ]
        }
    )

    results = [document for document in q]
    for item in results:
        if item["index"] == s if not s.isdigit() else int(s):
            return lib.db.find_one({"index": int(s)})
    return results