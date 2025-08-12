import pyshark
from collections import Counter

def english_packet_summary(pkt, src, dst):
    # SIP
    if hasattr(pkt, 'sip'):
        method = getattr(pkt.sip, 'Method', None)
        status = getattr(pkt.sip, 'Status-Line', None)
        if method:
            return f"A SIP {method} request was sent from {src} to {dst}."
        elif status:
            # e.g., SIP/2.0 200 OK
            status_code = status.split()[1] if len(status.split()) > 1 else status
            status_text = " ".join(status.split()[2:]) if len(status.split()) > 2 else status
            return f"A SIP {status_code} {status_text} response was sent from {src} to {dst}."
        else:
            return f"A SIP packet was sent from {src} to {dst}."
    # HTTP
    elif hasattr(pkt, 'http'):
        if hasattr(pkt.http, 'request_method'):
            return f"An HTTP {pkt.http.request_method} request was sent from {src} to {dst}."
        elif hasattr(pkt.http, 'response_code'):
            return f"An HTTP {pkt.http.response_code} response was sent from {src} to {dst}."
        else:
            return f"An HTTP packet was sent from {src} to {dst}."
    # RTP
    elif hasattr(pkt, 'rtp'):
        return f"An RTP media packet was sent from {src} to {dst}."
    # DNS
    elif hasattr(pkt, 'dns'):
        return f"A DNS packet was sent from {src} to {dst}."
    # Generic fallback
    else:
        proto = pkt.highest_layer
        return f"A {proto} packet was sent from {src} to {dst}."

def analyze_pcap(pcap_file):
    print(f"Analyzing: {pcap_file}\n")
    cap = pyshark.FileCapture(pcap_file, only_summaries=False)
    protocol_counter = Counter()
    ip_counter = Counter()
    sip_calls = []
    rtp_streams = set()
    http_requests = []
    http_responses = []
    total_packets = 0

    # RCA variables
    call_connected = False
    call_rejected = False
    call_rejected_by = None
    last_sip_status = None
    last_sip_from = None
    last_sip_to = None
    sip_invite_from = None
    sip_invite_to = None
    sip_call_id = None
    rtp_seen = False

    # --- Per-packet English summary (one line per packet) ---
    for idx, pkt in enumerate(cap, 1):
        total_packets += 1
        proto = pkt.highest_layer
        protocol_counter[proto] += 1

        # IPs
        src = getattr(pkt.ip, 'src', '-') if hasattr(pkt, 'ip') else '-'
        dst = getattr(pkt.ip, 'dst', '-') if hasattr(pkt, 'ip') else '-'
        if src != '-': ip_counter[src] += 1
        if dst != '-': ip_counter[dst] += 1

        # Info for SIP/RCA
        if hasattr(pkt, 'sip'):
            method = getattr(pkt.sip, 'Method', None)
            status = getattr(pkt.sip, 'Status-Line', None)
            call_id = getattr(pkt.sip, 'Call-ID', None)
            from_user = getattr(pkt.sip, 'from_user', None)
            to_user = getattr(pkt.sip, 'to_user', None)
            sip_calls.append({
                'time': pkt.sniff_time,
                'method': method,
                'status': status,
                'call_id': call_id,
                'from': from_user,
                'to': to_user,
                'src': src,
                'dst': dst
            })
            # RCA logic
            if method == "INVITE" and not sip_invite_from:
                sip_invite_from = from_user
                sip_invite_to = to_user
                sip_call_id = call_id
            if status:
                last_sip_status = status
                last_sip_from = from_user
                last_sip_to = to_user
                if "200 OK" in status and "INVITE" in status:
                    call_connected = True
                if status.startswith("SIP/2.0 4") or status.startswith("SIP/2.0 5") or status.startswith("SIP/2.0 6"):
                    call_rejected = True
                    call_rejected_by = src
        elif hasattr(pkt, 'http'):
            if hasattr(pkt.http, 'request_method'):
                http_requests.append(f"{pkt.http.request_method} {pkt.http.host}{pkt.http.request_uri}")
            elif hasattr(pkt.http, 'response_code'):
                http_responses.append(f"{pkt.http.response_code} {pkt.http.response_phrase}")
        elif hasattr(pkt, 'rtp'):
            ssrc = getattr(pkt.rtp, 'ssrc', None)
            if ssrc:
                rtp_streams.add(ssrc)
            rtp_seen = True

        # Print only the English summary line
        print(english_packet_summary(pkt, src, dst))

    cap.close()

    # --- Summary ---
    print("\n--- Summary ---")
    print(f"Total packets: {total_packets}")
    print(f"\nProtocol distribution:")
    for proto, count in protocol_counter.most_common():
        print(f"  {proto}: {count}")

    print(f"\nUnique IP addresses ({len(ip_counter)}):")
    for ip, count in ip_counter.most_common(5):
        print(f"  {ip}: {count} packets")

    if sip_calls:
        print(f"\nSIP Call Flow (first 10 messages):")
        for call in sip_calls:
            print(f"  [{call['time']}] {call['method'] or call['status']} | Call-ID: {call['call_id']} | From: {call['from']} | To: {call['to']}")

    if rtp_streams:
        print(f"\nRTP Streams found: {len(rtp_streams)} (SSRCs: {', '.join(rtp_streams)})")

    if http_requests or http_responses:
        print(f"\nHTTP Requests (first 5):")
        for req in http_requests[:5]:
            print(f"  {req}")
        print(f"HTTP Responses (first 5):")
        for res in http_responses[:5]:
            print(f"  {res}")

    # --- RCA Section ---
    print("\n--- Root Cause Analysis (RCA) ---")
    if sip_invite_from and sip_invite_to:
        print(f"Call initiated by: {sip_invite_from} → {sip_invite_to}")
    if sip_call_id:
        print(f"Call-ID: {sip_call_id}")

    # Find BYE and CANCEL
    bye_found = False
    bye_sender = None
    cancel_found = False
    cancel_sender = None
    ack_found = False
    invite_time = None
    ok_time = None
    last_error_status = None
    retransmissions = 0
    seen_sip_messages = set()

    for call in sip_calls:
        # BYE
        if call['method'] == "BYE":
            bye_found = True
            bye_sender = call['src']
        # CANCEL
        if call['method'] == "CANCEL":
            cancel_found = True
            cancel_sender = call['src']
        # ACK
        if call['method'] == "ACK":
            ack_found = True
        # INVITE/200 OK timing
        if call['method'] == "INVITE" and not invite_time:
            invite_time = call['time']
        if call['status'] and "200 OK" in call['status'] and "INVITE" in call['status'] and not ok_time:
            ok_time = call['time']
        # SIP errors
        if call['status'] and (call['status'].startswith("SIP/2.0 4") or call['status'].startswith("SIP/2.0 5") or call['status'].startswith("SIP/2.0 6")):
            last_error_status = call['status']
        # Retransmissions
        msg_id = (call['method'], call['status'], call['call_id'])
        if msg_id in seen_sip_messages:
            retransmissions += 1
        else:
            seen_sip_messages.add(msg_id)

    if call_connected:
        print("✅ Call was successfully connected (200 OK for INVITE seen).")
        if ack_found:
            print("✅ ACK was sent after 200 OK (call fully established).")
        else:
            print("⚠️  No ACK seen after 200 OK (call may not be fully established).")
        if rtp_seen:
            print("✅ RTP (media) data was transmitted after call setup.")
        else:
            print("⚠️  No RTP (media) data seen after call setup.")
        if bye_found:
            print(f"✅ Call was properly hung up with BYE from {bye_sender}.")
        else:
            print("⚠️  No BYE seen (call may not have been properly terminated).")
    elif call_rejected:
        print(f"❌ Call was rejected. Last SIP status: {last_sip_status}")
        print(f"   Rejected by: {call_rejected_by}")
        if last_error_status:
            print(f"   Last SIP error: {last_error_status}")
    else:
        print("❌ Call was not connected (no 200 OK for INVITE).")
        if last_sip_status:
            print(f"   Last SIP status: {last_sip_status}")
        else:
            print("   No SIP status found.")

    if cancel_found:
        print(f"⚠️  Call was cancelled before being answered. CANCEL sent by {cancel_sender}.")
    if not sip_calls:
        print("⚠️  No SIP signaling found in this capture.")
    if not rtp_seen and call_connected:
        print("⚠️  Call connected but no RTP (media) packets found.")
    if retransmissions > 0:
        print(f"⚠️  {retransmissions} possible SIP retransmissions or duplicate messages detected.")
    if invite_time and ok_time:
        try:
            delay = (ok_time - invite_time).total_seconds()
            if delay > 5:
                print(f"⚠️  Long delay ({delay:.2f} seconds) between INVITE and 200 OK.")
        except Exception:
            pass
    if call_connected and not bye_found:
        print("⚠️  Call connected but no BYE seen (call may not have been properly terminated).")
    if call_connected and not ack_found:
        print("⚠️  Call connected but no ACK seen after 200 OK (call may not have been fully established).")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python pcap_english_packet_summaries.py <file.pcap>")
        sys.exit(1)
    analyze_pcap(sys.argv[1])

