#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2023-2024.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

from ibmfl.exceptions import FLException


class CryptoException(FLException):
    pass


class KeyManagerException(FLException):
    pass


class KeyDistributionException(FLException):
    pass


class KeyDistributionInputException(KeyDistributionException):
    pass


class KeyDistributionVerificationException(KeyDistributionException):
    pass


class KeyDistributionCommunicationException(KeyDistributionException):
    pass
