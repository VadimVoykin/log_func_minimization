from controller import execute_minimization

if __name__ == "__main__":
    print("Welcome to logical functions minimization program.\n"
          "Mode 'sep_imps'. Asks for implicant separated by space\n"
          "two times. First one for implicant, that defined and\n"
          "must be covered in future and second time for implicants\n"
          "that represents undefined sets.\n"
          "Mode 'con_imps'. Same as mode 'sep imp', but expects\n"
          "to obtain two argument each time: first - conjunct\n"
          "implicants and second - number of implicant.\n")

    mode: str = input("Enter desired mode: ")

    if mode == "sep_imps":
        obl_imps_str = input("Enter obligatory implicants:\n   ")
        sup_imps_str = input("Enter supplementary implicants:\n   ")
        obl_imps = obl_imps_str.split()
        sup_imps = sup_imps_str.split()
        execute_minimization(obl_imps, sup_imps)


