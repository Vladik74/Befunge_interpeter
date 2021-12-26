from argparse import ArgumentParser
from interpreter import Interpreter

argparser = ArgumentParser()
argparser.add_argument('program_file',
                       help="path to Befunge executable code file")
argparser.add_argument('-i', '--input_file', required=False,
                       help="path to file with additional args that are "
                            "separated by space")

if __name__ == "__main__":
    args = argparser.parse_args()
    program_file = args.program_file
    input_file = args.input_file

    bi = Interpreter()
    try:
        bi.load_file(program_file, input_file)
    except FileNotFoundError as e:
        print(f"{e} not found")
        exit()
    bi.run()
