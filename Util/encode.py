def getStrCode(string: str) -> str:
    encoded_chars = [[]]
    for index in range(len(string)):
        if index % 2 == 0:
            encoded_chars[0].append(format(ord(string[index]), 'x'))
        else:
            encoded_chars[1].append(format(ord(string[index]), 'x'))
    return encoded_chars[0] + encoded_chars[1]

def getIpv4Code(ip: str) -> int:
    res: int = 0
    if '/' in ip:
        ip, ln = ip.split('/')
        res += int(ln) * 4294967296
    for part in ip.split('.'):
        res = res * 256 + int(part)
    return res

def decodeIpv4(ip: int) -> str:
    ip = ip & 0xffffffff
    ipv4 = []
    for i in range(4):
        ipv4.append(str(ip & 0xff))
        ip >>= 8
    return '.'.join(ipv4[::-1])

def bash(args: list[str]) -> None:
    print("Bash mode is not yet implemented.")
    if '-ip' in args:
        if '-x' in args:
            ip = args[args.index('-ip') + 1]
            print("Decode IPv4: ", decodeIpv4(int(ip)))
        else:
            ip_num = args[args.index('-ip') + 1]
            print("Encode IPv4: ", getIpv4Code(str(ip_num)))