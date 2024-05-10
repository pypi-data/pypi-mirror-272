from objict import objict
from datetime import datetime
import re
from .. import models as am
from location.models import GeoIP

IGNORE_RULES = [
    "100020"
]

LEVEL_REMAP_BY_RULE = {
    5402: 7,
    5710: 5
}


def removeNonAscii(input_str):
    """Remove all non-ASCII characters and escaped byte sequences from the input string."""
    # Remove escaped byte sequences
    cleaned_str = re.sub(r'\\x[0-9a-fA-F]{2}', '', input_str)
    # Remove non-ASCII characters
    return ''.join(char for char in cleaned_str if 32 <= ord(char) < 128)


def extractURL(text):
    match = re.search(r"GET\s+(https?://[^\s]+)\s+HTTP/\d\.\d", text)
    if match:
        return match.group(1)
    return None


def extractDomain(text):
    match = re.search(r"https?://([^/:]+)", text)
    if match:
        return match.group(1)
    return None


def extractUrlPath(text):
    match = re.search(r"https?://[^/]+(/[^?]*)", text)
    if match:
        return match.group(1)
    return None


def parseAlert(request, data):
    # helpers.log_print(data)
    try:
        data = objict.fromJSON(data.replace('\n', '\\n'))
    except Exception:
        data = objict.fromJSON(removeNonAscii(data))
    for key in data:
        data[key] = data[key].strip()

    if data.rule_id in IGNORE_RULES:
        return None
    if "test" in data.hostname and data.rule_id == "533":
        # bug on test ossec falsely report 533 events
        return None
    if data.rule_id == "510" and "/dev/.mount/utab" in data.text:
        return None
    # we care not for this field for now
    data.pop("logfile", None)
    if not data.text:
        raise Exception("invalid or missing json")
    alert = am.ServerOssecAlert(**data)
    alert.when = datetime.utcfromtimestamp(int(data.alert_id[:data.alert_id.find(".")]))
    # now lets parse the title
    title = alert.text[alert.text.find("Rule:") + 5:]
    # level to int
    level = title[title.find('(level') + 7:]
    alert.level = int(level[:level.find(')')].strip())
    title = title[:title.find('\n')].strip()
    pos = title.find("->")
    if pos > 0:
        title = title[pos + 2:]
    alert.title = title
    if alert.title.startswith("'"):
        alert.title = alert.title[1:-1]

    if data.hostname == "test":
        if data.rule_id == "31120" or "Web server" in title:
            return None

    # helpers.log_print(title, alert.title)
    # source ip (normally public ip of host)
    pos = alert.text.find("Src IP:")
    if pos > 1:
        src_ip = alert.text[alert.text.find("Src IP:") + 7:]
        alert.src_ip = src_ip[:src_ip.find('\n')].strip()

    irule = int(alert.rule_id)
    if irule == 5710:
        m = re.search(r"Invalid user (\S+) from (\S+)", data.text)
        if m and m.groups():
            alert.username = m.group(1)
            alert.src_ip = m.group(2).strip()
            alert.title = f"Attempt to login with invalid user: {alert.username}"
        else:
            m = re.search(r"Invalid user  from (\S+)", data.text)
            if m and m.groups():
                alert.username = "(empty string)"
                alert.src_ip = m.group(1).strip()
    elif irule == 2932:
        m = re.search(r"Installed: (\S+)", data.text)
        if m and m.groups():
            package = m.group(1)
            alert.title = "Yum Package Installed: {}".format(package)
    elif irule == 551:
        # Integrity checksum changed for: '/etc/ld.so.cache'
        m = re.search(r"Integrity checksum changed for: '(\S+)'", data.text)
        if m and m.groups():
            action = m.group(1)
            alert.title = "File Changed: {}".format(action)
    elif irule == 5715:
        m = re.search(r"Accepted publickey for (\S+).*ssh2: ([^\n\r]*)", data.text)
        if m and m.groups():
            ssh_sig = m.group(2)
            if " " in ssh_sig:
                kind, ssh_sig = ssh_sig.split(' ')
            alert.level = 8
            alert.username = m.group(1)
            alert.ssh_sig = ssh_sig
            alert.ssh_king = kind
            alert.title = f"SSH LOGIN:{alert.username}@{alert.hostname} from {alert.src_ip}"
            # member = findUserBySshSig(ssh_sig)
            # if member:
            #     alert.title = "SSH LOGIN user: {}".format(member.username)
    elif irule == 5501 or irule == 5502:
        # pam_unix(sshd:session): session opened for user git by (uid=0)
        m = re.search(r"session (\S+) for user (\S+)*", data.text)
        if m and m.groups():
            alert.action = m.group(1)
            alert.username = m.group(2)
            alert.title = f"session {alert.action} for user {alert.username}"
    elif irule == 5402:
        # TTY=pts/0 ; PWD=/opt/mm_protector ; USER=root ; COMMAND=/sbin/iptables -F
        m = re.search(r"sudo(?:\[\d+\])?:\s*(\S+).*?COMMAND=([^\n\r]*)", data.text)
        # m = re.search(r"sudo:\s*(\S+).*COMMAND=([^\n\r]*)", data.text)
        if m and m.groups():
            alert.username = m.group(1)
            alert.title = "sudo {}".format(m.group(2)).replace("#040", " ")
        alert.level = 7
    elif irule == 5706:
        m = re.search(r"identification string from (\S+) port (\S+)", data.text)
        if m and m.groups():
            alert.src_ip = m.group(1)
    elif irule == 5702:
        m = re.search(r"getaddrinfo for (\S+)", data.text)
        if m and m.groups():
            remote_host = m.group(1)
            alert.title = f"Reverse lookup failed for '{remote_host}'"
    elif irule == 554:
        m = re.search(r"New file '(\S+)' added", data.text)
        if m and m.groups():
            remote_file = m.group(1)
            alert.title = f"New file detected: '{remote_file}'"
    elif irule == 31101:
        m = re.search(r"GET\s+(http://[^\s]+)\s+HTTP/\d\.\d\s+(\d+)", data.text)
        if m and m.groups():
            code = m.groups(2)
            request_path = m.group(1)
            alert.title = f"HTTP {code}: {request_path}"
    elif irule == 100020:
        m = re.search(r"\[(\S+)\]", data.text)
        if m and m.groups():
            alert.src_ip = m.group(1)
    elif "web,accesslog," in data.text and "https:" in data.text:
        alert.ssh_sig = extractURL(data.text)
        if alert.ssh_sig:
            alert.hostname = extractDomain(alert.ssh_sig)

    if alert.ext_ip is None:
        alert.ext_ip = alert.src_ip
    if alert.src_ip is not None and len(alert.src_ip) > 6:
        # lets do a lookup for the src
        alert.geoip = GeoIP.lookup(alert.src_ip)

    if irule == 31111:
        url = alert.ssh_sig
        hostname = alert.hostname
        if url:
            hostname = extractDomain(url)
        if alert.geoip and alert.geoip.isp:
            alert.title = f"Suspicious fetch of .js, {hostname} ISP: {alert.geoip.isp}"
        else:
            alert.title = f"Suspicious fetch of .js, {hostname}"
    # finally here we change the alert level
    if irule in LEVEL_REMAP_BY_RULE:
        alert.level = LEVEL_REMAP_BY_RULE[irule]
    if alert.title[0] in ["'", '"']:
        alert.title = alert.title[1:-1]
    if len(alert.title) > 80:
        alert.title = alert.title[:80] + "..."
    alert.save()
    return alert

