from rest_framework import status
from random import randrange
from rest_framework.response import Response

def generate_400_response(message):
    return Response({"detail": message}, status.HTTP_400_BAD_REQUEST)

def generate_unique_code():
    CHARSET = '0123456789'
    LENGTH = 6
    new_code = ''
    for i in range(LENGTH):
        new_code += CHARSET[randrange(0, len(CHARSET))]
        return new_code