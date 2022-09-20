from errors import DifferentLengthException
from errors import ShortImplicantException


class Implicant:

    __reduction_symbol__ = "*"

    def __init__(self, implicant):
        """If implicant length less, than 3,
           returns ShortImplicantException."""

        if len(implicant) < 3:
            raise ShortImplicantException(
                "Implicant length less than 3.")
        self.__implicant__ = implicant
        self.__degree__ = self.__implicant__.count(
            self.__reduction_symbol__)
        self.consumed = False

    @staticmethod
    def set_reduction_symbol(symbol: str) -> None:
        """Sets symbol, that will be used to depict
           reduced arguments of implicant."""
        Implicant.__reduction_symbol__ = symbol

    def get_implicant(self) -> str:
        """Returns string representation of implicant."""
        return self.__implicant__

    def get_length(self) -> int:
        """Returns length of implicant."""
        return len(self.__implicant__)

    def get_degree(self) -> int:
        """Returns degree of implicant."""
        return self.__degree__

    def is_consumed(self) -> bool:
        """Returns True if implicant marked as
           consumed else False."""
        return self.consumed

    def consume(self) -> None:
        """Marks implicant as consumed. Change attribute
           'implicant' of object to straight crossed
           form of itself."""
        self.consumed = True

    def consumes(self, imp) -> bool:
        """Returns True if current implicant objects consumes
           given else False. If implicants lengths are different
           DifferentLengthError is returned."""

        if self.get_length() != imp.get_length():
            raise DifferentLengthException(
                "Length of implicants don`t match")
        str_imp_1 = self.get_implicant()
        str_imp_2 = imp.get_implicant()
        for i in range(self.get_length()):
            if not (str_imp_1[i] == self.__reduction_symbol__ or
                    str_imp_1[i] == str_imp_2[i]):
                return False
        return True

    def reduce(self, imp):
        """Reduces two implicant itself and given.
           If reduction is possible returns reduced implicant
           of Implicant Object else None type object. If implicants
           are identical, return None."""

        if self.get_length() != imp.get_length():
            raise DifferentLengthException(
                "Length of implicants don`t match")
        index = -1
        str_imp_1 = self.get_implicant()
        str_imp_2 = imp.get_implicant()
        for i in range(self.get_length()):
            if str_imp_1[i] != str_imp_2[i]:
                if index == -1:
                    index = i
                else:
                    return None
        if index == -1:
            return None
        result = list(str_imp_1)
        result[index] = self.__reduction_symbol__
        new_imp = Implicant("".join(result))
        return new_imp

    def __eq__(self, obj):
        return self.get_implicant() == obj.get_implicant()

    def __hash__(self):
        return self.get_implicant().__hash__()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Imp({self.get_implicant()})"
