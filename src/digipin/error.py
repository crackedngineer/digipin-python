class DigipinBaseError(Exception):
    """Base exception for all DIGIPIN related errors."""

    pass


class LatitudeOutOfRangeError(DigipinBaseError):
    """Exception raised when latitude is outside the defined bounds."""

    def __init__(self, message="Latitude is out of the defined range."):
        self.message = message
        super().__init__(self.message)


class LongitudeOutOfRangeError(DigipinBaseError):
    """Exception raised when longitude is outside the defined bounds."""

    def __init__(self, message="Longitude is out of the defined range."):
        self.message = message
        super().__init__(self.message)


class InvalidDigipinError(DigipinBaseError):
    """Exception raised when a DIGIPIN string has an invalid length."""

    def __init__(self, message="Invalid DIGIPIN length."):
        self.message = message
        super().__init__(self.message)


class InvalidDigipinCharError(DigipinBaseError):
    """Exception raised when a DIGIPIN string contains an invalid character."""

    def __init__(self, message="Invalid character found in DIGIPIN."):
        self.message = message
        super().__init__(self.message)
