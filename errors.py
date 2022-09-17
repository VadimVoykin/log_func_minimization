class DifferentLengthException(Exception):
    """Indicates reduction or comparison of
       implicants of different length."""
    pass


class ShortImplicantException(Exception):
    """Indicates creation of Implicant object
       with from short implicant."""
    pass


class ImplicantCoverageException(Exception):
    """Indicates detection of implicant, that
       can not be covered."""
    pass
