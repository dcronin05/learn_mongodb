import extract
import search

def start():
    extract.parse()
    print("Existing:", extract.existing)
    print("Inserted:", extract.inserted)
    print("Dupes:", extract.duplicates)
    extract.existing, extract.inserted, extract.duplicates = 0, 0, 0

    menu()

def prompt():
    return input("Search Value: ")

def menu():
    value = prompt()
    if value == "reload":
        start()
    while value != "quit" and value != "reload":
        results = search.query(value)
        if type(results) == dict:
            print(results["content"])
        else:
            for doc in results:
                print(doc["index"], " : ", doc["title"])
        value = prompt()


def main():
    start()

if __name__ == '__main__':
    main()