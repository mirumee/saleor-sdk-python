class ConfigDoesNotExistException(Exception):
    pass


class SaleorAppInstallationProblem(Exception):
    pass


class InvalidSaleorDomain(SaleorAppInstallationProblem):
    pass


class Unauthorized(Exception):
    pass


class SaleorConfigJWKSCacheException(Exception):
    pass
