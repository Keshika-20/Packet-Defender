# 🔐 Packet Defender — Firewall System

## 📌 Project Overview

**Blacklist & Whitelist with Protocol Filtering Firewall System**

---

## 👩‍💻 Team

* **Keshika N M** (24PW20)
* **Dhakshitha S** (24PW12)

---

## 📖 Abstract

Packet Defender is a Python-based firewall simulation system designed to implement key network security mechanisms, including **IP whitelisting, blacklisting, protocol-based filtering, throttling, and time-based access control**.

The system processes incoming requests through a **multi-layered filtering approach**, ensuring that only trusted and valid traffic is permitted while blocking unauthorized or potentially harmful access. This layered model improves security, minimizes misuse, and enhances traffic control efficiency.

A graphical user interface built using Tkinter enables both administrators and users to interact with the system effectively. Administrators can manage firewall rules, while users can simulate and observe request handling in real time.

The project is further extended using Cisco Packet Tracer to demonstrate real-world firewall implementation through **Access Control Lists (ACLs)**.

---

## 🎯 Objectives

* Simulate real-world firewall behavior using software
* Implement layered network security mechanisms
* Control access using IP-based and protocol-based rules
* Map theoretical concepts to practical networking using Cisco Packet Tracer

---

## 🚀 Features

* **IP Whitelisting**
* **IP Blacklisting**
* **Protocol Filtering** (HTTP, FTP)
* **Request Throttling (Rate Limiting)**
* **Time-Based Access Control**
* **Activity Logging and Monitoring**
* **Administrative Control Panel**
* **User Simulation Interface**
* **Persistent Data Storage (JSON)**

---

## 🧠 System Workflow

The firewall evaluates each incoming request through the following stages:

1. **Blacklist Validation** → Blocks known malicious IP addresses
2. **Time-Based Restriction** → Allows access only within defined time windows
3. **Request Throttling** → Limits excessive requests from a single IP
4. **Protocol Filtering** → Validates allowed communication protocols
5. **Whitelist Verification** → Permits only trusted IPs (if enabled)

> A request is **approved only if it successfully passes all layers**.

---

## 🛠 Technology Stack

* **Programming Language:** Python
* **GUI Framework:** Tkinter
* **Data Storage:** JSON
* **Network Simulation:** Cisco Packet Tracer

---

## 📂 Project Structure

```
Packet-Defender/
│
├── firewall.py          # Core firewall logic
├── main.py              # GUI application (Admin & User panels)
├── firewall_data.json   # Stores firewall rules and configurations
└── README.md            # Project documentation
```

---

## ⚙️ Setup & Execution

### Clone Repository

```bash
git clone <your-repo-link>
cd Packet-Defender
```

### Run Application

```bash
python main.py
```

---

## 🔐 Default Credentials

* **Username:** admin
* **Password:** 1234

---

## 🖥 Usage

### Administrator

* Manage whitelist and blacklist entries
* Enable or disable protocols
* Monitor system summary and logs

### User

* Enter IP address
* Select protocol (HTTP/FTP)
* Submit request and view firewall response

---

## 🌐 Cisco Packet Tracer Implementation

The firewall logic is replicated in a networking environment using:

* **Access Control Lists (ACLs)** → IP-based filtering
* **Port-Based Rules** → Protocol control (HTTP: 80, FTP: 21)
* **Time-Based ACLs** → Scheduled access restrictions

---

## 📊 Rule Evaluation Summary

| Condition                | Outcome |
| ------------------------ | ------- |
| IP in blacklist          | Blocked |
| Exceeds request limit    | Blocked |
| Protocol disabled        | Blocked |
| Not in whitelist         | Blocked |
| All conditions satisfied | Allowed |

---

## 🔥 Key Highlights

* Multi-layered firewall design
* Integration of software and network simulation
* Interactive GUI for better visualization
* Real-world applicability using Cisco tools

---

## 📌 Future Enhancements

* Support for additional protocols (SMTP, HTTPS)
* AI-based anomaly detection
* Real-time monitoring dashboard
* Cloud-based firewall integration

---

## 💯 Conclusion

Packet Defender demonstrates how modern firewall systems integrate multiple filtering mechanisms to provide secure and efficient network communication. The project effectively combines theoretical concepts with practical implementation, offering a strong foundation in network security principles.
