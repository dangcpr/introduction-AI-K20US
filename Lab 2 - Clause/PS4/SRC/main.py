from typing import List, Tuple
from pathlib import Path

from knowledgebase import Knowledge_Base

INPUT_FOLDER = './INPUT'
OUTPUT_FOLDER = './OUTPUT'


def read_input_file(file_path: Path) -> Tuple[str, List[str]]:
    with file_path.open() as file:
        alpha = file.readline()
        clauses = file.readlines()
    return alpha, clauses


def write_output_file(file_path: Path, entail: bool, new_clauses: List[List[str]]):
    with file_path.open(mode='w') as file:
        for clauses in new_clauses:
            file.write('{}\n'.format(len(clauses)))
            for clause in clauses:
                file.write('{}\n'.format(clause))
        if entail == True:
            file.write('YES')
        else:
            file.write('NO')


def main(input_folder: Path, output_folder: Path):
    if not output_folder.exists():
        output_folder.mkdir()

    for input_file in input_folder.glob('*.txt'):
        src = input_file.name
        des = output_folder.joinpath(src.replace('input', 'output'))

        alpha, clauses = read_input_file(input_file)

        KB = Knowledge_Base()
        KB.build_Knowledge_Base(alpha, clauses)

        entail, new_clauses = KB.PL_Resolution()

        write_output_file(des, entail, new_clauses)

        # Copy the input file to the output folder
        # shutil.copy(input_file, output_folder.joinpath(src))


if __name__ == '__main__':
    input_folder = Path(INPUT_FOLDER)
    output_folder = Path(OUTPUT_FOLDER)
    main(input_folder, output_folder)