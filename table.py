from errors import DifferentLengthException
from errors import ImplicantCoverageException
from implicant import Implicant

import re
import itertools as it


# Current version of class Table uses set to store implicants.
# It increases time required to perform reduction of implicants.

class Table:

    __debug_mode__ = False
    __reduction_symbol__: str = "*"

    def __init__(self, obl_imp_list: list[str],
                 sup_imp_list: list[str] = None,
                 debug_mode: bool = False):

        Implicant.set_reduction_symbol(self.__reduction_symbol__)
        __debug_mode__ = debug_mode

        if sup_imp_list is None:
            sup_imp_list = []
        self.imp_table = [{}]
        self.original_imps = {Implicant(imp) for imp in obl_imp_list}
        self.reduced_imps = set()
        self.core_imps = set()
        self.coverage_imps = set()

        imp_length = -1
        for imp in it.chain(obl_imp_list, sup_imp_list):
            if imp_length == -1:
                imp_length = len(imp)
            if imp_length != len(imp):
                raise DifferentLengthException(
                    "Input implicants are different length.")
            self.add_implicant(Implicant(imp))
        self.imp_padding = imp_length  # padding for implicants

    def set_imp_table(self, imp_table):
        """Method created for testing process."""
        self.imp_table = imp_table

    def add_implicant(self, imp: Implicant):
        """Add new implicant to table of implicant."""
        imp_str = imp.get_implicant()
        degree = imp.get_degree()
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
            for index in range(last_index):
                curr_key = key_val[index]
                next_key = key_val[index + 1]
                for imp1 in self.imp_table[column][curr_key]:
                    for imp2 in self.imp_table[column][next_key]:
                        if self.__debug_mode__:
                            print(f"Compare: {imp1.get_implicant()} "
                                  f"{imp2.get_implicant()}")
                        new_imp = None
                        if imp1.get_implicant() != imp2.get_implicant():
                            new_imp = imp1.reduce(imp2)
                        if new_imp is not None:
                            self.add_implicant(new_imp)
                            reduction_flag = True
        else:
            for key, imps in self.imp_table[column].items():
                for imp1 in imps:
                    for imp2 in imps:
                        if self.__debug_mode__:
                            print(f"Compare: {imp1.get_implicant()} "
                                  f"{imp2.get_implicant()}")
                        new_imp = imp1.reduce(imp2)
                        if new_imp is not None:
                            self.add_implicant(new_imp)
                            reduction_flag = True
        return reduction_flag

    def reduce(self) -> None:
        """Form table of implicants. Sort implicants
           by degree."""
        if self.__debug_mode__:
            print(">>Executing reduction")
        column = 0
        flag = True
        while flag:
            flag = self.process_column(column)
            column += 1

    def consume_for_implicant(self, imp: Implicant) -> None:
        """Mark all implicants, that can be consumed by
            given implicant 'imp', in table 'imp_table'."""

        degree = imp.get_degree()
        for index in range(degree):
            for val in self.imp_table[index].values():
                for curr_imp in val:
                    if self.__debug_mode__:
                        print(f"Compare if {imp} consumes"
                              f" {curr_imp}")
                    if imp.consumes(curr_imp) and \
                            not curr_imp.is_consumed():
                        curr_imp.consume()

    def consume(self) -> None:
        """Marks all implicants that can be consumed by implicant
           of higher degree as consumed."""
        if self.__debug_mode__:
            print(">>Executing consumption")
        table_length = len(self.imp_table)
        for index in range(table_length):
            column = self.imp_table[table_length - index - 1]
            for val in column.values():
                for imp in val:
                    if self.__debug_mode__:
                        print()
                    if not imp.is_consumed():
                        self.consume_for_implicant(imp)
                        self.reduced_imps.add(imp)

    def cover(self) -> None:
        """Finds minimal cover of original implicants by
           prime implicants, that were not consumed."""
        if self.__debug_mode__:
            print(">>Find Coverage")
        # Object attributes and local variables are
        # the same object, they will be modified.
        original_imps = self.original_imps
        reduced_imps = self.reduced_imps
        core_imps = set()
        # Find core implicants. Raise exception if
        # detected implicant, that can not be covered
        # by any implicant in 'reduced_imps'.
        for original_imp in original_imps:
            temp_core_imps = {imp for imp in reduced_imps
                              if imp.consumes(original_imp)}
            if self.__debug_mode__:
                print(f"{original_imp} covered by "
                      f"{len(temp_core_imps)} implicants")
            if len(temp_core_imps) == 1:
                core_imps = core_imps.union(temp_core_imps)
            elif len(temp_core_imps) == 0:
                raise ImplicantCoverageException(
                    "No reduced implicant to cover original.")
        # Delete core implicants from 'reduced_implicant'.
        # Delete implicants, that can be covered by core,
        # from 'original_implicants'.
        for core_imp in core_imps:
            consumed_imps = {imp for imp in original_imps
                             if core_imp.consumes(imp)}
            original_imps.difference_update(consumed_imps)
        reduced_imps.difference_update(core_imps)
        # Contains the best combination of implicant to cover
        # uncovered by 'core_imps' implicants.
        best_coverage = self.full_handle(
            original_imps, reduced_imps)
        self.core_imps = core_imps
        self.coverage_imps = best_coverage

    @staticmethod
    def full_handle(original_imps, reduced_imps):
        """Find minimal coverage using griddy algorith."""

        imps_num = 1
        comb_coefficient = float("inf")
        best_comb = set()
        for length in range(1, len(reduced_imps) + 1):
            for comb in it.combinations(reduced_imps, length):
                params = Table.coverage_coefficients(
                    original_imps, comb)
                temp_comb_coefficient = params[0] / params[1]
                if params[0] > imps_num or \
                   (params[0] == imps_num and
                   temp_comb_coefficient < comb_coefficient):
                    best_comb = comb
                    imps_num = params[0]
                    comb_coefficient = params[1]
        return best_comb

    @staticmethod
    def coverage_coefficients(
            original_imps, reduced_imps):
        """Calculate number of covered implicants and combination
           coefficient and return in same order enclosed in tuple."""

        comb_coefficient = 0
        covered_imps = set()
        for curr_imp in reduced_imps:
            imp_coefficient = curr_imp.get_length() - \
                              curr_imp.get_degree()
            temp_covered_imps = {imp for imp in original_imps
                                 if curr_imp.consumes(imp)}
            covered_imps = covered_imps.union(temp_covered_imps)
            comb_coefficient += imp_coefficient
        return len(covered_imps), comb_coefficient

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
            result[row].append(" " * self.imp_padding)
        # Add given implicant or str to table.
        if isinstance(element, Implicant):
            sequence = element.get_implicant()
        elif isinstance(element, str):
            sequence = element
            sequence = sequence.center(self.imp_padding, "-")
        else:
            raise TypeError(
                "Expected object of type str of Implicant.")
        result[row].append(sequence)

    def visualize_reduction(self) -> str:
        """Return str representation of current class
           member imp_table in 'sql' format."""
        result = []
        row_counter = 0
        column_counter = 0
        for column in self.imp_table:
            for header, imp_set in column.items():
                # Add header to table.
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
        top_border = "+" + ("-" * self.imp_padding + "+") * len(result[0]) + "\n"
        content = ["|" + "|".join(row) + "|\n" for row in result]
        return top_border + "".join(content) + top_border

    @staticmethod
    def str_repr(imp_set):
        result = ' '.join({str(imp) for imp in imp_set})
        if len(result) == 0:
            result = "Empty list"
        return result

    def visualize_coverage(self):
        result = ""
        result += f"Core imps\n   " \
                  f"{Table.str_repr(self.core_imps)}\n"
        result += f"Reduced imps\n   " \
                  f"{Table.str_repr(self.reduced_imps)}\n"
        result += f"Imps to cover\n   " \
                  f"{Table.str_repr(self.original_imps)}\n"
        result += f"Best coverage\n   " \
                  f"{Table.str_repr(self.coverage_imps)}"
        return result
