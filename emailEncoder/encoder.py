import unicodedata, idna, re, requests


VALID_TLDS_LIST = requests.get('http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split()[11::]

def encode_email(email: str):
    if email.count('@') != 1 or email.count('.') < 1:
        return None

    lowercased = email.lower() 
    normalized = unicodedata.normalize('NFC', lowercased)

    local, domain = normalized.split('@')

    if len(local) > 64 or len(domain) > 255:
        return None

    local_encoded, domain_encoded = '', ''
    try:
        local_encoded = idna.encode(local).decode('ascii')
        domain_encoded = idna.encode(domain).decode('ascii')
    except Exception as e:
        print(f'Error encoding email: {e}')
        return None
    
   
    tld = domain_encoded.split('.')[-1]
    if tld.upper() not in VALID_TLDS_LIST:
        print(f'Invalid TLD: {tld}')
        return None

    return f'{local_encoded}@{domain_encoded}'


def encode_domain_from_url(url: str):
    domain_match = re.match(r'(https?://)([^/]+)(/.*)?', url)
    if not domain_match:
        return None
    
    protocol = domain_match.group(1)
    domain = domain_match.group(2)
    path = domain_match.group(3)

    normalized_domain = unicodedata.normalize('NFC', domain)

    try:
        encoded_domain = idna.encode(normalized_domain).decode('ascii')
    except Exception as e:
        print(f'Error encoding domain: {e}')
        return None

    encoded_url = f"{protocol}{encoded_domain}{path}" if path else f"{protocol}{encoded_domain}"
    return encoded_url


print(encode_domain_from_url('https://مثال.موقع/مسار'))