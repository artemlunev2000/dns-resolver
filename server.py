import socket
from dns import *

roots = [
    "198.41.0.4",
    "199.9.14.201",
    "192.33.4.12",
    "199.7.91.13",
    "192.203.230.10",
    "192.5.5.241",
    "192.112.36.4",
    "198.97.190.53",
    "192.36.148.17",
    "192.58.128.30",
    "193.0.14.129",
    "199.7.83.42",
    "202.12.27.33",
]

address = ("127.0.0.1", 53)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)


def resolve():
    if domain in cache:
        return cache[domain]

    mes = message.make_query(name.from_text(domain), getattr(rdatatype, req_type), getattr(rdataclass, req_cl))

    for root in roots:
        response = recurse(mes, root)

        if response is not None:
            cache[domain] = response
            return response

    return None


def recurse(q, serv_ip):
    response = query.udp(q, serv_ip)

    if response:
        if response.answer:
            return response
        elif response.additional:
            for additional in response.additional:
                if additional.rdtype != getattr(rdatatype, req_type):
                    continue
                for add in additional:
                    new_response = recurse(q, str(add))
                    if new_response:
                        return new_response

    return response


if __name__ == "__main__":
    cache = dict()
    while True:
        request, time, addr = query.receive_udp(sock)

        req = str(request.question[0]).split()

        domain = req[0]
        req_cl = req[1]
        req_type = req[2]

        res = resolve()

        response = message.make_response(request)

        if res is not None:
            response.answer = res.answer

        query.send_udp(sock, response, addr)