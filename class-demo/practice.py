# Install a pip package in the current Jupyter kernel
import sys
#!{sys.executable} -m pip install python-jose

import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'matthsworld.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Image'

'''
AuthError Exception
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Im44cVBZTWtoMmlfcGIzUTR4OE43aSJ9.eyJpc3MiOiJodHRwczovL21hdHRoc3dvcmxkLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2MmIxYmFiOTRkZmM0ZjFiOTVlMWJhODEiLCJhdWQiOiJpbWFnZSIsImlhdCI6MTY1NTgxNDg2MywiZXhwIjoxNjU1ODIyMDYzLCJhenAiOiI5VnE0YWRLOFNNZkpobVhBbUVWcnZyMWhXTFpEM2RpTiIsInNjb3BlIjoiIn0.gDEPIjYuedCU6kVJbhMd3KSGvwhtfOAQAsgs5lScNOIRTc8-NFtOdmQMf5IL7i_fBTbiH1n9522gxUOwnEpIfbS9_r93bRzfVWlQ_hLBF5lNxN7YXUmgrWat1srD7V8l3-gIlxUoxZRYOy_eUOlG8N_0eX5bnZLayxDlumjeoNk4gNe_BMaQmf3MSj_htRbHx5-mNanY6KavRqY09ardx5RODRY-Hr-QZFxvZcL0BbkSyN7wpeYKyP5FPyJqK5JERwSSsLeb-cNxcFAcOveIsqFb5V_1Z6FRmFJmMa7MHOZ9gMCmaV0M0PdgYUU4NAvL8FJlZ3CY7sEUu9qD30PDKg"

## Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)