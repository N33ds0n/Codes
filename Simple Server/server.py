import socket
import sqlite3



host = ""
port = 7676

_conn = sqlite3.connect("data.db")
c = _conn.cursor()
s = socket.socket()
s.bind((host, port))
while True:
    s.listen()
    conn, addr = s.accept()
    request = conn.recv(1000000).decode()
    headers = request.split("\n")
    print(headers)

    method = headers[0].split()[0]
    if method  == "POST":
        ppath = headers[0].split()[1]
        pdata = headers[-1].replace('&', ",").replace("=", ",").split(",")

        if ppath in ["/account", "/account/"]:
            login = {
                 pdata[0]:pdata[1],
                 pdata[2]:pdata[3],
                 pdata[4]:pdata[5]
               }

            id = login["id"]
            user = login["username"]
            passwd = login["password"]

            sql = """ INSERT INTO users(id, username, password) VALUES(?,?,?) """
            c.execute(sql, (id, user, passwd))
            _conn.commit()
            with open("form.html", "r") as rf0:
                res0 = rf0.read()
                conn.send(b"HTTP/1.1\n\n"+res0.encode())

        elif ppath in ["/login", "/login/"]:
            c.execute(""" SELECT username, password FROM users WHERE id='007' """)
            all = c.fetchall()
            u = ""
            p = ""
            for x, y in all:
                u = x
                p = y

            login = {
                 pdata[0]:pdata[1],
                 pdata[2]:pdata[3],
               }

            user = login["username"]
            passwd = login["password"]

            if user == u:
                if passwd == p:
                    with open("home.html", "r") as f0:
                        response0 = f0.read()
                        conn.send(b"HTTP/1.1\r\n\n"+response0.encode())

                else:
                   d = b"<h1>Wrong  Password</h1>"
                   conn.send(b"HTTP/1.1\r\n\n"+d)
            else:
                g = b"<h1>Wrong  Username</h1>"
                conn.send(b"HTTP/1.1\r\n\n"+g)

        elif ppath in ["/post", "/post/"]:
            post = {
                 pdata[0]:pdata[1],
                 pdata[2]:pdata[3],
               }

            title = post["title"]
            content = post["textarea"]

            sql = """ INSERT INTO posts(title, content) VALUES(?,?) """
            c.execute(sql, (title, content))
            _conn.commit()
            with open("home.html", "r") as rf01:
                res01 = rf01.read()
                conn.send(b"HTTP/1.1\n\n"+res01.encode())

        else:
            with open("404.html", "r") as f5:
                response5 = f5.read()
                conn.send(b"HTTP/1.1\n\n"+response5.encode())
                print("4040 not found")

    elif method == "GET":
        gpath = headers[0].split()[1]
        if gpath in ["/index", "/index/"]:
            with open("index.html", "r") as f:
                response = f.read()
                conn.send(b"HTTP/1.1\n\n"+response.encode())
                print("index")

        elif gpath in ["/", "/home", "/home/"]:
            c.execute("SELECT * FROM posts")
            datas = c.fetchall()
            at = ""
            ac = ""
            for t, fh in datas:
                at = t
                ac = fh
            fl =  open("home.html")
            h = fl.readlines()
            h[25] = f"<h1>{at}</h1></br></br><p>{ac}</p>"
            fl = open("home.html", "w")
            ho = "".join(h)
            fl.write(ho)
            fl.close()
            rf = open("home.html")
            bh = rf.read()
            conn.send(b"HTTP/1.1\n\n"+bh.encode())

        elif gpath in ["/about", "/about/"]:
            with open("about.html", "r") as f3:
                response3 = f3.read()
                conn.send(b"HTTP/1.1\n\n"+response3.encode())
                print("about")

        elif gpath in ["/contact",  "/contact/"]:
            with open("contact.html", "r") as f4:
                response4 = f4.read()
                conn.send(b"HTTP/1.1\n\n"+response4.encode())
                print("contact")

        elif gpath in ["/login", "/login/"]:
            with open("form.html", "r") as f4:
                response4 = f4.read()
                conn.send(b"HTTP/1.1\n\n"+response4.encode())
                print("Form")

        elif gpath in ["/account", "/account"]:
            with open("account.html", "r") as f6:
                response6 = f6.read()
                conn.send(b"HTTP/1.1\n\n"+response6.encode())
                print("Account Created")

        elif gpath in ["/post", "/post/"]:
            with open("post.html", "r") as rf11:
                resp11 = rf11.read()
                conn.send(b"HTTP/1.1\n\n"+resp11.encode())
                print("post form")

        else:
            with open("404.html", "r") as f5:
                response5 = f5.read()
                conn.send(b"HTTP/1.1\n\n"+response5.encode())
                print("4040 not found")

    else:
        conn.send(b"HTTP/1.1\n\n<h1>Method Not Supported</h1>")

s.close()
_conn.close()
print("socket close")



