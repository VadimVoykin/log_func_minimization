from errors import DifferentLengthException
from errors import ImplicantCoverageException
from errors import ShortImplicantException
from errors import NotImplicantException

from table import Table


def execute_minimization(obl_imps: list[str], sup_imps: list[str]):
    try:
        table = Table(obl_imps, sup_imps)
        table.reduce()
        table.consume()
        table.cover()
        print(table.visualize_reduction())
        print(table.visualize_coverage())
    except DifferentLengthException:
        print("Entered implicants have different length.")
    except ShortImplicantException:
        print("Entered implicants are shorter than 3.")
    except ImplicantCoverageException:
        print("Something has gone wrong."
              "Prime implicants can not cover original implicant.")
    except NotImplicantException:
        print("Entered invalid implicant.")


