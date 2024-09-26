import extract
import search
import pprint

def prompt():
    return input("Search Value: ")

def menu():
    value = prompt()
    while value != "quit":
        results = search.query(value)
        if type(results) == dict:
            print(results["content"])
        else:
            for doc in results:
                print(doc["index"], " : ", doc["title"])
        value = prompt()


def main():

    extract.parse()
    print("Existing:", extract.existing)
    print("Inserted:", extract.inserted)
    print("To big:", extract.big)
    print("Dupes:", extract.duplicates)

    menu()

if __name__ == '__main__':
    main()