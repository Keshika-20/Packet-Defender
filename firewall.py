import time
import json
import os
from datetime import datetime
from collections import defaultdict

DATA_FILE = "firewall_data.json"


def load_data():
    global whitelist, blacklist, protocol_rules

    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            whitelist.update(data.get("whitelist", []))
            blacklist.update(data.get("blacklist", []))
            protocol_rules.update(data.get("protocol_rules", {}))
    else:
        save_data()


def save_data():
    data = {
        "whitelist": list(whitelist),
        "blacklist": list(blacklist),
        "protocol_rules": protocol_rules
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


whitelist = set()
blacklist = set()

protocol_rules = {
    "HTTP": True,
    "FTP": True,
}

request_log = []
request_timestamps = defaultdict(list)

THROTTLE_LIMIT = 5
THROTTLE_WINDOW = 60
ALLOWED_START_HOUR = 9
ALLOWED_END_HOUR = 17


def admin_login(username: str, password: str) -> bool:
    return username == "admin" and password == "1234"


def add_to_whitelist(ip: str) -> str:
    ip = ip.strip()
    if not ip:
        return "ERROR: IP cannot be empty."
    if ip in blacklist:
        return f"ERROR: {ip} is in blacklist."

    whitelist.add(ip)
    save_data()
    _log_event("ADMIN", ip, "N/A", "WHITELISTED", "Added to whitelist")
    return f"SUCCESS: {ip} added to whitelist."


def remove_from_whitelist(ip: str) -> str:
    ip = ip.strip()
    if ip in whitelist:
        whitelist.remove(ip)
        save_data()
        return f"SUCCESS: {ip} removed from whitelist."
    return f"INFO: {ip} not found in whitelist."


def add_to_blacklist(ip: str) -> str:
    ip = ip.strip()
    if not ip:
        return "ERROR: IP cannot be empty."
    if ip in whitelist:
        return f"ERROR: {ip} is in whitelist."

    blacklist.add(ip)
    save_data()
    _log_event("ADMIN", ip, "N/A", "BLACKLISTED", "Added to blacklist")
    return f"SUCCESS: {ip} added to blacklist."


def remove_from_blacklist(ip: str) -> str:
    ip = ip.strip()
    if ip in blacklist:
        blacklist.remove(ip)
        save_data()
        return f"SUCCESS: {ip} removed from blacklist."
    return f"INFO: {ip} not found in blacklist."


def set_protocol(protocol: str, enabled: bool) -> str:
    protocol = protocol.upper()
    if protocol not in protocol_rules:
        return "ERROR: Invalid protocol."

    protocol_rules[protocol] = enabled
    save_data()
    status = "ENABLED" if enabled else "DISABLED"

    _log_event("ADMIN", "N/A", protocol, status, "Protocol changed")
    return f"SUCCESS: {protocol} {status}"


def check_request(ip: str, protocol: str) -> dict:
    ip = ip.strip()
    protocol = protocol.upper()

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Rule 1: Blacklist
    if ip in blacklist:
        return _build_result(ip, protocol, timestamp, "BLOCKED", "Blacklisted")

    # Rule 2: Time restriction
    if not (ALLOWED_START_HOUR <= now.hour < ALLOWED_END_HOUR):
        return _build_result(ip, protocol, timestamp, "BLOCKED", "Outside allowed time")

    # Rule 3: Throttling
    _clean_old_timestamps(ip)
    if len(request_timestamps[ip]) >= THROTTLE_LIMIT:
        return _build_result(ip, protocol, timestamp, "BLOCKED", "Too many requests")

    # Rule 4: Protocol
    if protocol not in protocol_rules or not protocol_rules[protocol]:
        return _build_result(ip, protocol, timestamp, "BLOCKED", "Protocol blocked")

    # Rule 5: Whitelist
    if whitelist and ip not in whitelist:
        return _build_result(ip, protocol, timestamp, "BLOCKED", "Not in whitelist")

    request_timestamps[ip].append(time.time())
    return _build_result(ip, protocol, timestamp, "ALLOWED", "Passed all checks")




def get_summary():
    return f"""
WHITELIST: {list(whitelist)}
BLACKLIST: {list(blacklist)}
PROTOCOLS: {protocol_rules}
LOG COUNT: {len(request_log)}
"""


def get_log_entries():
    return request_log


def _build_result(ip, protocol, timestamp, result, reason):
    entry = {
        "timestamp": timestamp,
        "actor": "USER",
        "ip": ip,
        "protocol": protocol,
        "result": result,
        "reason": reason,
    }
    request_log.append(entry)
    return entry


def _log_event(actor, ip, protocol, result, reason):
    request_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actor": actor,
        "ip": ip,
        "protocol": protocol,
        "result": result,
        "reason": reason,
    })


def _clean_old_timestamps(ip):
    cutoff = time.time() - THROTTLE_WINDOW
    request_timestamps[ip] = [t for t in request_timestamps[ip] if t > cutoff]
    
def get_user_session_summary():
    user_entries = [e for e in request_log if e["actor"] == "USER"]

    if not user_entries:
        return "\n(No user activity in this session)\n"

    lines = ["\n--- USER SESSION SUMMARY ---"]

    for e in user_entries:
        lines.append(
            f"{e['timestamp']} | {e['ip']} | {e['protocol']} | "
            f"{e['result']} | {e['reason']}"
        )

    return "\n".join(lines)