import socket
import time
import sys

dest_port = 33434
max_hops = 30

def main(dest_name):
    dest_ip = socket.gethostbyname(dest_name)
    sys.stdout.write(f'Tracing the route to {dest_name} ({dest_ip})\n')
    TTL = 1
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    recv_socket.settimeout(5)
    curr_ip = None
    curr_name = None
    while(curr_ip != dest_ip and TTL < max_hops):
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)
        sys.stdout.write(f'{TTL}')
        finished = False
        attempts = 3
        send_socket.sendto(bytes('Hey', 'utf-8'), (dest_name, dest_port))
        time_start = time.time()
        while not finished and attempts > 0:
            try:
                _, curr_addr = recv_socket.recvfrom(1024)
                time_end = time.time()
                finished = True
                curr_ip = curr_addr[0]
                try:
                    curr_name = socket.gethostbyaddr(curr_ip)[0]
                except socket.error:
                    curr_name = curr_ip
            except socket.error:
                attempts -= 1
                sys.stdout.write(' * ')
                curr_ip = None
                curr_name = None
        if curr_ip is not None:
            curr_host = f'{curr_name} ({curr_ip})'
            t = round((time_end - time_start) * 1000, 3)
            sys.stdout.write(f' {curr_host} {t}ms\n')
        else:
            sys.stdout.write('\n')
        TTL += 1

if __name__ == '__main__':
    main(sys.argv[1])