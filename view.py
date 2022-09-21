from controller import execute_minimization

if __name__ == "__main__":
    print("Welcome to logical functions minimization program.\n"
          "Application asks for implicant separated by space\n"
          "two times. First one for obligatory implicant, that\n"
          "are defined and must be covered in future and\n"
          "second time for supplementary implicants, that\n"
          "represents undefined sets.\n")

    obl_imps_str = input("Enter obligatory implicants:\n   ")
    sup_imps_str = input("Enter supplementary implicants:\n   ")
    obl_imps = obl_imps_str.split()
    sup_imps = sup_imps_str.split()
    print(obl_imps, sup_imps)
    execute_minimization(obl_imps, sup_imps)
