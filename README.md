# 🕵️‍♂️ WiFi Watchdog – "I See What You Did There"

> Ever wondered what websites your family, flatmates, or freeloading neighbors are visiting while hogging your Wi-Fi? Well... now you *don’t have to* wonder.

## 🚨 Disclaimer

> **⚠️ WARNING:** This project is for **educational purposes only**. Spying on people without consent is **highly unethical** (and often illegal). Don’t be a creep. Be cool. 😎

---

## 📦 What Is This?

A full-stack real-time network traffic sniffer that:
- Detects devices connected to your Wi-Fi network
- Shows their **IP**, **MAC address**, and **(if possible)** device name
- Monitors and logs the **websites** they visit
- Streams all that juicy data live to a pretty frontend dashboard


---

## 🛠️ Tech Stack

| Layer       | Tech                            |
|------------|----------------------------------|
| 🧠 Backend  | Python (`scapy`, `socketio`, `plyer`) |
| 📢 Server   | Flask + Flask-SocketIO           |
| 🌍 Frontend | Next.js + Tailwind CSS           |
| 💬 Protocols| WebSockets & HTTP                |

---

## 🧪 Features

- 📡 **Real-time sniffing** of DNS/TCP traffic
- 🌐 **Domain detection** from HTTP, TLS, and DNS packets
- 💻 **Device discovery** with IP, MAC, and device names
- 🔎 **Live web dashboard** to view logs & filters
- 🔥 **Filter system** to highlight suspicious sites.

---

## 🧰 How It Works

1. Your `sniff.py` script acts like a silent ninja, lurking in your network’s shadows...
2. It captures DNS & HTTP requests made by any device connected to the same Wi-Fi.
3. When it sees someone Googling something weird at 3am, it:
   - Logs the domain
   - Notifies you (yes, like a loyal snitch)
   - Sends it to the frontend via Socket.IO
4. Your frontend displays everything like a hacker movie dashboard 🎬

---

