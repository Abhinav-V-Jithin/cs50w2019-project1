import csv
import requests
def main():
    f = open("books.csv")
    reader = csv.reader(f)
    line = 0
    work_ratings_count = ''
    average_rating = ''
    id = 0
    for isbn,title,author,year in reader:
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XvwqEKsB6436BG1hfKWg", "isbns": isbn})
        if res.status_code != 200:
            print("Error at:")
            print(f"status:{res.status_code}")
            print(f"line:{line}")
            continue
        line += 1
if __name__ == '__main__':
    main()
