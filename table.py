from errors import DifferentLengthException
from implicant import Implicant

import re


# Current version of class Table uses set to store implicants.
# It increases time required to perform reduction of implicants.

class Table:

    __reduction_symbol__: str = "*"

    def __init__(self, imp_list: list[str]):
        Implicant.set_reduction_symbol(self.__reduction_symbol__)
        self.imp_table = [{}]
        imp_length = -1
        for imp in imp_list:
            if imp_length == -1:
                imp_length = len(imp)
            if imp_length != len(imp):
                raise DifferentLengthException(
                    "Input implicants are different length.")
            self.add_implicant(Implicant(imp))
        self.imp_length = imp_length

    def set_imp_table(self, imp_table):
        """Method created for testing process."""
        self.imp_table = imp_table

    def add_implicant(self, imp: Implicant):
        """Add new implicant to table of implicant."""
        imp_str = imp.get_implicant()
        degree = imp_str.count(self.__reduction_symbol__)
        # Depending on implicant degree chose appropriate key.
        if degree == 0:
            key = str(imp_str.count("1"))
        else:
            key = re.sub('[01]', "-", imp_str)
        # If not enough columns in 'imp_table',
        # add missing one. If element with key
        # 'key' does not exist, add one.
        if len(self.imp_table) < degree + 1:
            self.imp_table.append(dict())
        if key not in self.imp_table[degree].keys():
            self.imp_table[degree][key] = set()
        self.imp_table[degree][key].add(imp)

    def process_column(self, column: int) -> bool:
        """Reduce implicants of column with index 'column'."""
        reduction_flag = False
        if column == 0:
            key_val = list(self.imp_table[column].keys())
            key_val.sort()
            last_index = len(key_val) - 1
            print(key_val)
            for index in range(last_index):
                curr_key = key_val[index]
                next_key = key_val[index + 1]
                for imp1 in self.imp_table[column][curr_key]:
                    for imp2 in self.imp_table[column][next_key]:
                        new_imp = None
                        print(f"Compare: {imp1.get_implicant()} {imp2.get_implicant()}")
                        if imp1.get_implicant() != imp2.get_implicant():
                            new_imp = imp1.reduce(imp2)
                        if new_imp is not None:
                            self.add_implicant(new_imp)
                            reduction_flag = True
        else:
            for key, imps in self.imp_table[column].items():
                for imp1 in imps:
                    for imp2 in imps:
                        new_imp = imp1.reduce(imp2)
                        if new_imp is not None:
                            self.add_implicant(new_imp)
                            reduction_flag = True
        return reduction_flag

    def reduce(self) -> None:
        """Form table of implicants. Sort implicants
           by degree."""

        column = 0
        flag = True
        while flag:
            flag = self.process_column(column)
            column += 1
        print(self.imp_table)

    def consume_for_implicant(self, imp: Implicant) -> None:
        """Mark all implicants, that can be consumed by
            given implicant 'imp', in table 'imp_table'."""

        degree = imp.get_degree()
        for index in range(degree):
            for val in self.imp_table[index].values():
                for curr_imp in val:
                    print(f"Compare if {imp} consumes {curr_imp}")
                    if imp.consumes(curr_imp) and \
                            not curr_imp.is_consumed():
                        curr_imp.consume()

    def consume(self) -> None:
        """Marks all implicants that can be consumed by implicant
           of higher degree as consumed."""

        for column in self.imp_table:
            for val in column.values():
                for imp in val:
                    if not imp.is_consumed():
                        self.consume_for_implicant(imp)

    def cover(self) -> None:
        """Finds minimal cover of original implicants by
           prime implicants, that were not consumed."""
        pass

    def add_imp(self, result, element: Implicant | str,
                row: int, column: int) -> None:
        """Add implicant at given indices. If not enough
           rows or elements in certain row, complement tabel."""
        # check if enough rows. If not add missing one.
        if len(result) < row + 1:
            result.append([])
        # Calculate current number of elements in
        # given row. Variable "column" represent
        # simultaneously index to insert at and
        # required number of elements.
        num_of_columns = len(result[row])
        difference = column - num_of_columns
        # Complement row with number of missing elements.
        for i in range(difference):
            result[row].append(" " * self.imp_length)
        # Add given implicant or str to table.
        if isinstance(element, Implicant):
            sequence = element.get_implicant()
        elif isinstance(element, str):
            sequence = element
        else:
            raise TypeError(
                "Expected object of type str of Implicant.")
        result[row].append(sequence)

    def visualize_table_of_reduction(self) -> str:
        """Return str representation of current class
           member imp_table in 'sql' format."""
        result = []
        row_counter = 0
        column_counter = 0
        for column in self.imp_table:
            for key, imp_set in column.items():
                # Add header to table.
                if column_counter > 0:
                    header = key
                else:
                    header = f"{key:^{self.imp_length}}"
                self.add_imp(
                    result, header, row_counter, column_counter)
                row_counter += 1
                # Add implicants from set.
                for imp in imp_set:
                    self.add_imp(
                        result, imp, row_counter, column_counter)
                    row_counter += 1
            column_counter += 1
            row_counter = 0
        # Construct table.
        top_border = "+" + ("-" * self.imp_length + "+") * len(result[0]) + "\n"
        content = ["|" + "|".join(row) + "|\n" for row in result]
        return top_border + "".join(content) + top_border
