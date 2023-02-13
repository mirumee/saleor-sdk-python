class CryptoException(Exception):
    """
    Base exception for the crypto module errors.
    """


class JWKSKeyMissing(CryptoException):
    """
    Raised when a requested kid is missing from a keyset.
    """


class KeyIDMissing(CryptoException):
    """
    Raised when a JWT without a 'kid' header is received.
    """
