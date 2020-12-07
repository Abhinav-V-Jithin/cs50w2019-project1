import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
import speech
import urllib.request
engine = create_engine('postgres://ezglyvvlicbgbv:ead7588140b7272354da497c1165d09ab6929a8f2077595625dfb46f30e27ecb@ec2-34-224-229-81.compute-1.amazonaws.com:5432/dcsdjfos3rgbsj')
db = scoped_session(sessionmaker(bind=engine))
def connect(host='https://www.google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False
res = ''
def main():
    line=0
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        while 1:
            try:
                res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XvwqEKsB6436BG1hfKWg", "isbns": isbn})
            except:
                speech.say("Boss, please check your internet connection")
                print("No internet. Retrying...")
                continue
            break
        if res.status_code != 200:
            speech.say("Boss detected an error")
            print("Found errors at:")
            print(f"status:{res.status_code}")
            print(f"line:{line+1}")
            continue
        data= res.json()
        data = data["books"]
        work_ratings_count = ''
        average_rating = ''
        id = 0
        for list in data:
            work_ratings_count = list["work_ratings_count"]
            average_rating     = list["average_rating"]
            id =  list["id"]
        db.execute("INSERT INTO books (isbn,title,author,year) VALUES (:isbn,:title,:author,:year)",{"isbn":isbn,"title":title,"author":author,"year":year})
        print(f"Added book with isbn={isbn} title={title} author={author} year={year}")
        if line % 500==0:
            speech.say(f"Boss, I have reached line number {line}")
        print(f"{line}")
        line = line+1
    db.commit()
if __name__ == '__main__':
    main()
