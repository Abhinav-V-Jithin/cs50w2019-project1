from flask import Flask, session, render_template, request, redirect, url_for, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from datetime import datetime

app = Flask(__name__)
def get_avg(num1,num2,list):
    isbn_string = ''
    for i in range(num1,num2):
        isbn_string += list[i]
        if i==(num2-1):
            break
        isbn_string += ','
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XvwqEKsB6436BG1hfKWg", "isbns": isbn_string})
    data = res.json()
    data = data["books"]
    rating_list = []
    for list in data:
        rating_list.append(list["average_rating"])
    return rating_list
def mix_avg(list1,list2):
    for i in list2:
        list1.append(i)
    return list1

def isEmpty(list):
    if len(list) ==0:
        return "empty"
    return "notEmpty"
def getUser():
    return session["username"]
def getavg(isbn):
    rating = db.execute("SELECT rating FROM rating WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    avg = 0.0
    sum = 0
    num = 0
    if rating is None:
        return avg
    ratings = db.execute("SELECT rating from rating WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
    for rating in ratings:
        sum += rating.rating
        num += 1
    if num == 0:
        return avg
    avg =  float(sum)/num
    return avg
# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
username = ''
# Set up database
engine = create_engine('postgresql://postgres:1029384756Vithayathil@localhost:5432/book_review',pool_size=10, max_overflow=50)
db = scoped_session(sessionmaker(bind=engine))
@app.route("/", methods=["POST","GET"])
def index():
    if 'username' in session:
        return redirect(url_for('book_store'))
    return render_template("index.html")
@app.route("/register_page", methods=["POST","GET"])
def register_page():
    #redirecting to the register page
    return render_template("register.html")


@app.route("/register", methods=["GET","POST"])
def register():
    username = str(request.form.get("username"))
    password = str(request.form.get("password"))
    if password.isdigit():
        return render_template("error.html", message="Your password must contain at least 1 character.")
    if username == '':
        return render_template("error.html", message="You have to specify your username.")
    if password == '':
        return render_template("error.html", message="You have to specify your password.")
    existing_users = db.execute("SELECT username FROM users").fetchall()
    for user in existing_users:
        if username == user.username:
            return render_template("error.html", message="This username already exists.")
    session["username"] = username
    db.execute("INSERT INTO users (username,password) VALUES(:username,:password)",{"username":username,"password":password})
    db.commit()
    return redirect(url_for('book_store'))
@app.route("/verify", methods=["POST"])
def verify():
    username = request.form.get("name")
    password = request.form.get("password")
    if username == '' or password == '':
        return render_template("error.html", message="Do not keep the boxes empty.", file="login")
    users = db.execute("SELECT username, password FROM users WHERE username=:username", {"username":username}).fetchone()
    if users is None:
        return render_template("error.html", message="Invalid username or password.", file="login")
    if users.password != password:
        return render_template("error.html", message="Invalid username or password.", file="login")
    session["username"] = username
    return redirect(url_for('book_store'))
@app.route("/book_store", methods=["GET","POST"])
def book_store():
    return render_template("loader.html")
@app.route("/top_books/", methods=["POST","GET"])
def top_books():
    all_list = []
    title_list  = []
    author_list = []
    year_list = []
    rating_list= []
    isbn_list  = []
    book_list = db.execute("SELECT isbn, author, title, year FROM books")
    for single_book in book_list:
        isbn_list.append(single_book.isbn)
    print("Starting to make average list...")
    rating_list1 = get_avg(0,500,isbn_list)
    print("list1 completed.")
    rating_list2 = get_avg(500,1000,isbn_list)
    print("list2 completed.")
    rating_list3 = get_avg(1000,1500,isbn_list)
    print("list3 completed.")
    rating_list4 = get_avg(1500,2000,isbn_list)
    print("list4 completed.")
    rating_list5 = get_avg(2000,2500,isbn_list)
    print("list5 completed.")
    rating_list6 = get_avg(2500,3000,isbn_list)
    print("list6 completed.")
    rating_list7 = get_avg(3000,3500,isbn_list)
    print("list7 completed.")
    rating_list8 = get_avg(3500,4000,isbn_list)
    print("list8 completed.")
    rating_list9 = get_avg(4000,4500,isbn_list)
    print("list9 completed.")
    rating_list10 = get_avg(4500,len(isbn_list),isbn_list)
    print("list10 completed.")
    rating_list = []
    rating_list = mix_avg(mix_avg(mix_avg(mix_avg(mix_avg(mix_avg(mix_avg(mix_avg(mix_avg(rating_list1,rating_list2),rating_list3),rating_list4),rating_list5),rating_list6),rating_list7),rating_list8),rating_list9),rating_list10)
    print("rating list is ready...")
    all_list = []
    for i in range(0,len(isbn_list)):
        book = db.execute("SELECT isbn,author,title,year FROM books WHERE isbn=:isbn",{"isbn":isbn_list[i]}).fetchone()
        all_list.append([f"{book.isbn}",f"{book.title}",f"{book.author}",f"{book.year}",f"{rating_list[i]}"])
    print("Sorting...")
    sorted_books = sorted(all_list, key=lambda x:x[4])
    print("Sorted")
    all_books = []
    new_rating_list = []
    new_isbn_list = []
    for i in reversed(sorted_books):
        all_books.append(i)
    for i in all_books:
        print(i)
        new_isbn_list.append(i[0])
        title_list.append(i[1])
        author_list.append(i[2])
        year_list.append(i[3])
        new_rating_list.append(i[4])
    if 'username' in session:
        return render_template("book_store.html",username=session["username"],stat='logged in',authors=author_list,titles=title_list,years=year_list,ratings=new_rating_list,isbns=new_isbn_list,num=50)
    return render_template("book_store.html",authors=author_list,stat='logged out',titles=title_list,years=year_list,ratings=new_rating_list,isbns=new_isbn_list,num=50)
#completed upto here
@app.route("/search/results", methods=["POST","GET"])
def search():
    is_isbn = True
    is_year = True
    is_title= True
    is_author= True
    authors = []
    titles  = []
    isbns   = []
    years   = []
    query = str(request.form.get("search2"))
    books = db.execute("SELECT isbn,title,author,year FROM books").fetchall()
    for book in books:
        if query in book.author or query.capitalize() in book.author:
            authors.append([f"{book.isbn}",f"{book.title}",f"{book.author}",f"{book.year}"])
    for book in books:
        if query in book.title or query.capitalize() in book.title:
            titles.append([f"{book.isbn}",f"{book.title}",f"{book.author}",f"{book.year}"])
        if str(query) in str(book.isbn) or str(query)==str(book.isbn):
            isbns.append([f"{book.isbn}",f"{book.title}",f"{book.author}",f"{book.year}"])
        if query in str(book.year):
            years.append([f"{book.isbn}",f"{book.title}",f"{book.author}",f"{book.year}"])
    if isEmpty(authors) == "empty":
        is_author = False
    if isEmpty(titles) == "empty":
        is_title = False
    if isEmpty(isbns) == "empty":
        is_isbn = False
    if isEmpty(years) == "empty":
        is_year = False
    stat = 'logged out'
    if 'username' in session:
        stat = 'logged in'
    return render_template("search_results.html", stat=stat,query=query,authors=authors,titles=titles,years=years,isbns=isbns,is_isbn=is_isbn,is_year=is_year,is_title=is_title,is_author=is_author)
@app.route("/book_details/<string:isbn>", methods=["GET","POST"])
def books_details(isbn):
    book = db.execute("SELECT isbn,title,author,year FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "XvwqEKsB6436BG1hfKWg", "isbns": isbn})
    data = res.json()
    data = data["books"]
    goodreadsrating = ''
    n = False
    rating_list = []
    sum = 0
    num = 0
    average = 0
    myrating = db.execute("SELECT rating FROM rating WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if myrating == None:
        n = True
    else:
        myrating = db.execute("SELECT rating FROM rating WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
        for rating in myrating:
            rating_list.append(rating.rating)
        for rating in rating_list:
            sum += rating
            num += 1
        average = float(sum)/num
    for list in data:
        goodreadsrating = list["average_rating"]
    stat=''
    if 'username' in session:
        stat='logged in'
    else:
        stat='logged out'
    return render_template("book_details.html",stat=stat,book=book,goodreadsrating=goodreadsrating,avg=average,n=n)
@app.route("/book/rate/<string:isbn>", methods=["POST","GET"])
def rate(isbn):
    num = request.form.get("star")
    print("star:",num)
    if 'username' in session:
        book = db.execute("SELECT * FROM rating WHERE isbn=:isbn AND username=:username",{"isbn":isbn,"username":session["username"]}).fetchone()
        if book != None:
            return render_template("error.html", message="You have already rated this book!", file="already", isbn=isbn)
        db.execute("INSERT INTO rating (isbn,rating,username) VALUES(:isbn,:rating,:username)",{"isbn":isbn,"rating":num,"username":session["username"]})
        db.commit()
        return redirect(url_for('books_details', isbn=isbn))
    return render_template("error.html",isbn=isbn, message="You can't rate any books unless you sign in!", file="rate")
@app.route("/book/<string:isbn>/getcomments", methods=["POST","GET"])
def getcomments(isbn):
    comments = db.execute("SELECT comment,username,comment_time FROM comments WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if comments is None:
        return render_template("comments.html",isbn=isbn, no_comments=True)
    comments = db.execute("SELECT comment,username,comment_time FROM comments WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
    comment_list = []
    for comment in comments:
        comment_list.append([f"{comment.comment}",f"{comment.username}",f"{comment.comment_time}"])
    sorted_comments = sorted(comment_list, key=lambda x:x[2])
    ordered_comments = []
    i=len(sorted_comments)-1
    while i>=0:
        ordered_comments.append(sorted_comments[i])
        i -= 1
    comment_list = []
    username_list = []
    time_list = []
    date_list = []
    for i in ordered_comments:
        comment_list.append(i[0])
        username_list.append(i[1])
        m = i[2]
        l = m.split(' ')
        date = l[0]
        m_list = date.split('-')
        year = m_list[0]
        if m_list[1] == '01':
            month = "January"
        elif m_list[1] == '02':
            month = "February"
        elif m_list[1] == '03':
            month = "March"
        elif m_list[1] == '04':
            month = "April"
        elif m_list[1] == '05':
            month = "May"
        elif m_list[1] == '06':
            month = "June"
        elif m_list[1] == '07':
            month = "July"
        elif m_list[1] == '08':
            month = "August"
        elif m_list[1] == '09':
            month = "September"
        elif m_list[1] == '10':
            month = "October"
        elif m_list[1] == '11':
            month = "November"
        else:
            month = "December"
        day = m_list[2]
        date_list.append(f"{day}th {month}, {year}")
        time = l[1]
        t_list = time.split(':')
        meridian = "AM"
        hour = t_list[0]
        if hour>'12':
            hour = str(int(hour)-12)
            meridian = "PM"
        minute = t_list[1]
        time_list.append(f"{hour}:{minute} {meridian}")
    limit = len(ordered_comments)
    return render_template("comments.html",isbn=isbn, users=username_list,comments=comment_list,time=time_list,date_list=date_list,num=limit)
@app.route("/book/<string:isbn>/comment", methods=["POST", "GET"])
def commenton(isbn):
    comment = request.form.get("comment")
    if comment == '':
        return render_template("error.html", isbn=isbn, message="Do not keep the boxes empty!", file="comments")
    if 'username' not in session:
        return render_template("error.html", isbn=isbn, message="Please sign in to comment on this book", file="register")
    co = db.execute("SELECT (username,comment) FROM comments WHERE username=:username AND isbn=:isbn", {"isbn":isbn,"username":session["username"]}).fetchone()
    if co != None:
        return render_template("error.html",isbn=isbn, message="You have already commented on this book!", file="comments")
    db.execute("INSERT INTO comments (isbn,comment,username,comment_time) VALUES(:isbn,:comment,:username,:comment_time)",{"isbn":isbn,"comment":comment,"username":session["username"],"comment_time":str(datetime.now())})
    db.commit()
    return redirect(url_for('getcomments', isbn=isbn))
@app.route("/logout", methods=["POST"])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
@app.route("/book/api/<string:isbn>")
def book_api(isbn):
    book = db.execute("SELECT isbn,title,author,year FROM books WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if book is None:
        return jsonify({"error":"Invalid isbn number"}), 422
    comment = db.execute("SELECT comment FROM comments WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    count = 0
    sum = 0
    num = 0
    if comment is not None:
        comments = db.execute("SELECT comment FROM  comments WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
        for comment in comments:
            count += 1
    rating = db.execute("SELECT rating FROM rating WHERE isbn=:isbn",{"isbn":isbn}).fetchone()
    if rating is not None:
        ratings = db.execute("SELECT rating FROM rating WHERE isbn=:isbn",{"isbn":isbn}).fetchall()
        for rating in ratings:
            num += 1
            sum += rating.rating
    if num == 0:
        avg = 0.0
    else:
        avg = float(sum)/num
    return jsonify({
    "title":book.title,
    "author":book.author,
    "year":book.year,
    "isbn":isbn,
    "review_count":count,
    "average_score":avg
    })
@app.route("/WebsiteX/About", methods=["POST", "GET"])
def About():
    return render_template("About.html")
@app.route("/WebsiteX/Documentation", methods=["POST","GET"])
def documentation():
    return render_template("Documentation.html")
if __name__ == '__main__':
    app.run()
