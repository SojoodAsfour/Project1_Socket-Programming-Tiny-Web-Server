# 🌐 ENCS3320 – Project #1  
## Socket Programming & Tiny Web Server

🎓 Birzeit University  

---

## 📌 Project Overview

This project demonstrates fundamental networking concepts through:

- 🔧 Networking tools (Ping, Tracert, NSLookup, Telnet)
- 📡 TCP & UDP socket programming
- 🌍 Building a complete Tiny Web Server using low-level socket programming
- 🔐 Secure registration & login using SHA256 hashing
- 🍪 Session management using cookies
- 🔁 HTTP redirection & error handling

No frameworks (Flask/Django) were used — only raw socket programming.

---

# 🧩 Part 1 – Networking Tools

## ✍️ Definitions (In Our Own Words)

- **Ping** 🏓: A tool used to test connectivity between two devices and measure response time.
- **Tracert** 🛣️: Shows the path (hops) that packets take to reach a destination.
- **NSLookup** 🔍: Retrieves DNS information and maps domain names to IP addresses.
- **Telnet** 💻: Connects to remote devices using TCP to test ports and services.

---

## 🧪 Commands Executed

1. Ping device in same network  
2. `ping 1.1.1.1`  
3. `tracert 1.1.1.1`  
4. `nslookup 1.1.1.1`  
5. DNS capture using Wireshark  

📊 From ping results:
- RTT values indicate internet distance.
- Number of hops in tracert indicates routing path.

Screenshots (with date & time) are included in the report.

---

# 🧩 Part 2 – TCP & UDP Socket Programming

## ⚙️ Requirements

- Server listens on port **8090**
- Client:
  - Sends `"START"` via TCP
  - Sends numbers 0 → 1,000,000 via UDP (each in separate packet)
  - Sends `"END"` via TCP

## 🖥️ Server Responsibilities

- Count received numbers
- Count how many packets arrived out of order
- Display statistics on terminal

Technologies used:
- Python sockets (no frameworks)
- TCP (reliable communication)
- UDP (connectionless transmission)

---

# 🧩 Part 3 – Tiny Web Server (Port 8099)

## 🌍 Server Features

- Listens on port **8099**
- Uses HTTP/1.1 protocol
- Serves:
  - HTML files
  - CSS files
  - PNG images
  - JPG images

---

## 📄 Main Pages

### / or /en
Returns `main_en.html`

Includes:
- Title: **ENCS3320-My Tiny Webserver 25/26**
- Styled using external CSS 🎨
- Group members information 👥
- Images (.png & .jpg)
- Register & Login links
- Summary of cache terms
- External link to W3Schools

---

### /ar
Returns `main_ar.html` (Arabic version)

---

## 🔁 Redirection (307 Temporary Redirect)

- `/chat` → ChatGPT
- `/cf` → Cloudflare
- `/rt` → Ritaj website

---

## ❌ Error Handling (404)

If file not found:

- Status: `HTTP/1.1 404 Not Found`
- Title: Error 404
- Red message: “The file is not found”
- Names & IDs in bold
- Client IP and port shown

---

# 🔐 User Authentication

## 📝 Registration

- User enters username & password
- Password hashed using **SHA256**
- Stored in `data.txt`

---

## 🔑 Login

- Password hashed again
- Compared with stored hash
- If valid:
  - Sends `protected.html`
  - Generates random session ID
  - Sends session ID in cookie 🍪

---

## 🍪 Session Management

- Session stored in server memory
- Cookie sent automatically by browser
- Access to protected pages allowed only if session exists
- Logout removes session

---

# 🖨️ HTTP Request Logging

All HTTP requests are printed on the server terminal window.

---

# 🛠️ Technologies Used

- Python socket programming
- TCP & UDP protocols
- SHA256 (hashlib)
- HTTP/1.1
- Cookies & Session Management
- Wireshark

---


---

# 🧪 Testing

✔ Tested from same computer  
✔ Tested from another device  
✔ Verified session persistence  
✔ Verified logout functionality  
✔ Verified redirection & 404  
✔ Verified HTTP request printing  

Screenshots with date & time included in report.

---

# 👥 Team Members

- [Sojood Asfour]
- [Shahd Manasra]

---

# 🚀 Learning Outcomes

This project strengthened skills in:

- Socket programming
- HTTP protocol
- DNS analysis
- Network troubleshooting
- Secure authentication
- Session management
- Low-level web server design

---

✨ ENCS3320 – Computer Networks  
Birzeit University  
