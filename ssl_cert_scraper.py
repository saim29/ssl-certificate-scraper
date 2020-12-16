import ssl, sys, csv, socket
import pandas as pd
from OpenSSL import crypto, SSL

def get_certificate(host, port, path):

    print ("Connect to:", host)

    try:
        conn = ssl.create_connection((host, port), timeout=3)

        if not conn:
            return False
        
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)

        if not context:
            return False

        sock = context.wrap_socket(conn, server_hostname=host)

        if not sock:
            return False
    except:

        print("EXCEPTION - Cannot make SSL connection")
        return False

    cert = ssl.DER_cert_to_PEM_cert(sock.getpeercert(True))
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)    

    with open(path, 'wb') as output_file:
        output_file.write((crypto.dump_certificate(crypto.FILETYPE_PEM, x509)))

    return True


################################################################

print('Number of Files:', len(sys.argv)-1)
print('File List:', str(sys.argv[1:]))

fileList = sys.argv[1:]

for f in fileList:

    urls = pd.read_csv(f, index_col='URL')
    subset = urls.index
    numUrls = len(subset)

    for num, url in enumerate(subset):
        name = url.replace('.', '_')
        get_certificate(url, 443, 'certs/' + name + '.pem')
        print ("Progress: ", num/float(numUrls))

    
#####################################################################