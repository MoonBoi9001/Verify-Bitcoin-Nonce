import requests
import hashlib
from datetime import datetime

# Define the block height
block_height = 778115

# Define the URL for the Blockchair API endpoint
url = 'https://api.blockchair.com/bitcoin/blocks?q=id(' + str(block_height) + ')'

# Make a GET request to the URL
response = requests.get(url)

# Extract the block header fields from the response dictionary
data = response.json()['data'][0]
version = data['version']
previous_block_hash = data['hash']
merkle_root = data['merkle_root']
timestamp = data['time']
bits = data['bits']
nonce = data['nonce']

#Convert timestamp to UNIX time
timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
unix_time = int(timestamp.timestamp())

# Print the block header fields
print('Block Header Fields for Block Height ' + str(block_height) + ':')
print('')
print('Version: ' + str(version))
print('Previous Block Hash: ' + previous_block_hash)
print('Merkle Root: ' + merkle_root)
print('Timestamp: ' + str(unix_time))
print('Bits: ' + str(bits))
print('Nonce: ' + str(nonce))

# Concatenate the block header fields into a single string
block_header = str(version) + previous_block_hash + merkle_root + str(unix_time) + str(bits) + str(nonce)

# Compute the SHA-256 hash of the block header and reverse the byte order to match the endianness used in Bitcoin
hash = hashlib.sha256(hashlib.sha256(block_header.encode('utf-8')).digest()).digest()[::-1]

# Compute the target difficulty for the block
exponent = (bits >> 24) & 0xff
coefficient = bits & 0xffffff
target = coefficient * 2 ** (8 * (exponent - 3))

# Check if the hash is valid by comparing it to the target difficulty
if int.from_bytes(hash, byteorder='big') <= target:
    print('Nonce is valid')
else:
    print('Nonce is not valid')
    print('Target is:   ' + str(target))
    print('Hash is:     ' + str(int.from_bytes(hash, byteorder='big')))
    print('The block header is: ' + str(block_header))
   
