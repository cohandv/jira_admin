from program import Program

if __name__ == "__main__":
    # program_ticket = input("Please enter the program TPM")
    program_ticket = "TPM-1756"  # test
    # program_ticket = "TPM-931"  # OpEx
    p = Program(program_ticket)
    p.review_projects()
