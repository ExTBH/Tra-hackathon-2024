import unicodedata, idna, requests


VALID_TLDS_LIST = requests.get('http://data.iana.org/TLD/tlds-alpha-by-domain.txt').text.split()[11::]

def encode_email(email: str) -> str|None:
    """
    Encode the given email to IDNA stuff, if its wrong it will return None.
    """
    if email.count('@') != 1 or email.count('.') < 1:
        return None

    lowercased = email.lower()  # Convert to lowercase
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
    
    # check if tld in valid tlds list
    tld = domain_encoded.split('.')[-1]
    if tld.upper() not in VALID_TLDS_LIST:
        print(f'Invalid TLD: {tld}')
        return None

    return f'{local_encoded}@{domain_encoded}'


def encode_url(url: str) -> str|None:
    """
    Encode the given url to IDNA stuff.
    """

