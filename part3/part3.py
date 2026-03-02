from socket import *
import hashlib
import urllib.parse
import random
import string

portNum=8099
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(("",portNum))
serverSocket.listen(1)
print ("The server is ready to receive")

def generate_session_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) 

session_table = {}

while True:
    connectionSocket, address = serverSocket.accept()
    sent=connectionSocket.recv(2048).decode()
    print(address)
    IP= address[0]
    port=address[1]
    print("IP: "+ str(IP) +",Port: "+ str(port))
    print("********************************************************")
    print(sent)
    print("********************************************************")
    
    if sent !='':
        request_File=sent.split(' ')[1].replace('/','')
        method = sent.split(' ')[0]
        print("Request File: "+request_File)
        print("Method: "+method)
    else:
        connectionSocket.close()
        continue
        
    try:        
        if method == 'POST':
            
            if request_File == 'register':
                body = sent.split('\r\n\r\n')[1]
                parsed = urllib.parse.parse_qs(body)
                username = parsed.get('username',[''])[0]
                password = parsed.get('password',[''])[0]
                username_exists = False
                
                try:   
                    with open("data.txt", "r") as f:
                        for line in f:
                            existing_user = line.split(":")[0]
                            if existing_user == username:
                                username_exists = True
                                break
                except FileNotFoundError:
                    pass
                    
                if username_exists:
                    response = """
                    <html>
                    <head>
                        <link rel="stylesheet" href="styles.css">
                        <title>Register Error</title>
                    </head>
                    <body>
                        <div class="container">
                            <div class="box">
                                <h2>Username Already Exists!</h2>
                                <p><a href="main_en.html">Go back</a></p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                    connectionSocket.send(response.encode())
                else:
                    hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                    with open("data.txt", "a") as f:
                        f.write(f"{username}:{hashed_pw}\n")
                    response = """
                        <html>
                        <head>
                            <link rel="stylesheet" href="styles.css">
                            <title>Registration Successful</title>
                        </head>
                        <body>
                            <div class="container">
                                <div class="box">
                                    <h2>Registration Successful!</h2>
                                    <p><a href="main_en.html">Go back to Home</a></p>
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                    connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                    connectionSocket.send(response.encode())
                    
            elif request_File == 'login.html' or request_File == 'login':
                body = sent.split('\r\n\r\n')[1]
                parsed = urllib.parse.parse_qs(body)
                username = parsed.get('username',[''])[0]
                password = parsed.get('password',[''])[0]
                hashed_pw = hashlib.sha256(password.encode()).hexdigest()
                
                login_success = False
                
                try:   
                    with open("data.txt", "r") as f:
                        for line in f:
                            parts = line.strip().split(":")
                            if len(parts) == 2:  
                                stored_user, stored_hash = parts
                                if username == stored_user and hashed_pw == stored_hash:
                                    login_success = True
                                    break
                except FileNotFoundError:
                    pass
                    
                if login_success:
                    session_id = generate_session_id()
                    session_table[session_id] = username
                    print(f"Session created: {session_id} for user: {username}")
                    
                    try:
                        with open("protected.html","r", encoding='utf-8') as f:
                            page = f.read()
                            connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                            connectionSocket.send(f"Set-Cookie: session_id={session_id}; Path=/\r\n".encode())
                            connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                            connectionSocket.send(page.encode())
                    except FileNotFoundError:
                        response = f"""
                            <html>
                            <head><link rel="stylesheet" href="styles.css"><title>Login Success</title></head>
                            <body>
                                <div class="container">
                                    <div class="box">
                                        <h2>Welcome {username}!</h2>
                                        <p>Login Successful!</p>
                                        <p><a href="main_en.html">Go to Home</a></p>
                                    </div>
                                </div>
                            </body>
                            </html>
                            """
                        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                        connectionSocket.send(f"Set-Cookie: session_id={session_id}; Path=/\r\n".encode())
                        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                        connectionSocket.send(response.encode())
                else:
                    response = """
                        <html>
                        <head><link rel="stylesheet" href="styles.css"><title>Login Error</title></head>
                        <body>
                            <div class="container">
                                <div class="box">
                                    <h2>Invalid Username or Password!</h2>
                                    <p><a href="login.html">Try Again</a></p>
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                    connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                    connectionSocket.send(response.encode())
                    
            elif request_File == 'logout':
                session_id = None
                headers = sent.split('\r\n')
                for header in headers:
                    if header.startswith('Cookie:'):
                        cookies = header.split('Cookie:')[1].strip()
                        for cookie in cookies.split(';'):
                            if 'session_id=' in cookie:
                                session_id = cookie.split('session_id=')[1].strip()
                                break
                
                if session_id and session_id in session_table:
                    del session_table[session_id]
                    print(f"Session deleted: {session_id}")
                
                response = """
                <html>
                <head><link rel="stylesheet" href="styles.css"></head>
                <body>
                    <div class="container">
                        <div class="box">
                            <h2>Logged Out Successfully</h2>
                            <p><a href="main_en.html">Go to Home</a></p>
                        </div>
                    </div>
                </body>
                </html>
                """
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Set-Cookie: session_id=; Max-Age=0\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                connectionSocket.send(response.encode())
            else:
                raise Exception('Not found')
                
        # ==================== GET REQUESTS ====================
        elif method == 'GET':
            
            # Protected pages - check session
            if request_File == 'protected.html':
                session_id = None
                headers = sent.split('\r\n')
                for header in headers:
                    if header.startswith('Cookie:'):
                        cookies = header.split('Cookie:')[1].strip()
                        for cookie in cookies.split(';'):
                            if 'session_id=' in cookie:
                                session_id = cookie.split('session_id=')[1].strip()
                                break
                
                if session_id and session_id in session_table:
                    with open("protected.html", "r", encoding='utf-8') as f:
                        page = f.read()
                        connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                        connectionSocket.send(page.encode())
                else:
                    response = """
                    <html>
                    <head><link rel="stylesheet" href="styles.css"></head>
                    <body>
                        <div class="container">
                            <div class="box">
                                <h2>Access Denied</h2>
                                <p>Please <a href="login.html">login</a> first.</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    connectionSocket.send("HTTP/1.1 401 Unauthorized\r\n".encode())
                    connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                    connectionSocket.send(response.encode())
                    
            elif request_File == '' or request_File=='main_en.html' or request_File== 'index.html' or request_File =='en':
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                mhtml=open('main_en.html' ,'rb')
                connectionSocket.send(mhtml.read())
                mhtml.close()
                
            elif request_File=='ar':
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                mhtml=open('main_ar.html' ,'rb')
                connectionSocket.send(mhtml.read())
                mhtml.close()
                
            elif '.html' in request_File:
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
                print('response status: 200 OK\n\n')
                f= open(str(request_File), 'rb')
                connectionSocket.send(f.read())
                f.close()
                
            elif '.css' in request_File:
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: text/css\r\n\r\n".encode())
                print('response status: 200 OK\n\n')
                f= open(str(request_File), 'rb')
                connectionSocket.send(f.read())
                f.close()
                
            elif '.png' in request_File:
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/png\r\n\r\n".encode())
                print('response status: 200 OK\n\n')
                f= open(str(request_File), 'rb')
                connectionSocket.send(f.read())
                f.close()
                
            elif '.jpg' in request_File:
                connectionSocket.send("HTTP/1.1 200 OK\r\n".encode())
                connectionSocket.send("Content-Type: image/jpeg\r\n\r\n".encode())
                print('response status: 200 OK\n\n')
                f = open(str(request_File), 'rb')
                connectionSocket.send(f.read())
                f.close()
                
            elif request_File =='chat':
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://chatgpt.com/\r\n\r\n".encode())

            elif request_File =='cf':
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://www.cloudflare.com/\r\n\r\n".encode())

            elif request_File =='rt':
                connectionSocket.send("HTTP/1.1 307 Temporary Redirect\r\n".encode())
                connectionSocket.send("Location: https://ritaj.birzeit.edu/\r\n\r\n".encode())
                
            elif 'favicon.ico' == request_File:
                print()
            else:
                raise Exception('Not found')
        else:
            raise Exception('Not found')
            
    except Exception as e:
        connectionSocket.send("HTTP/1.1 404 Not Found\r\n".encode())
        connectionSocket.send("Content-Type: text/html\r\n\r\n".encode())
        print(request_File + " - Not Found")
        print('Response status: 404 Not Found')
        error_page='<!DOCTYPE html><html>' \
        '<style>*{ text-align: center; }' \
        '#Error{ color: red;}#name{ font-weight: bold;}</style>'\
        '<head>  <title>Error 404</title></head>' \
        '<body>  <div id="Error">   <h1>The file is not found</h1> </div>' \
        '<hr> <div id="name">  <p>Sojood Asfour 1230298</p> <p>Shahd Manasra 1230308</p>' \
        '<p> Ip Adress: '+ str(IP)+ ', Port Number: ' +str(port)+\
        '</p> </div> </body></html>'
        connectionSocket.send(error_page.encode())

    connectionSocket.close()