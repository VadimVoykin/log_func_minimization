class DifferentLengthException(Exception):
    """Indicates reduction or comparison of
       implicants of different length."""
    pass


class ShortImplicantException(Exception):
    """Indicates creation of Implicant object
       with from short implicant."""
    pass
