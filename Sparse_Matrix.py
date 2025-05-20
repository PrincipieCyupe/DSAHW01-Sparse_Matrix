import os

def list_matrix_files():
    """List all .txt files in the current directory and return the list."""

    files = [f for f in os.listdir() if f.endswith('.txt')]
    print("Available sample input files (sparse matrix files):")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    return files

def load_sparse_matrix(filename):
    """Load a sparse matrix from a text file with error handling."""

    try:
        with open(filename, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            rows = int(lines[0].split('=')[1])
            cols = int(lines[1].split('=')[1])
            matrix = {}
            for line in lines[2:]:
                if not (line.startswith('(') and line.endswith(')')):
                    raise ValueError("Input file has wrong format")

                try:
                    row, col, val = line.strip('()').split(',')
                    row = int(row)
                    col = int(col)
                    val = int(val)
                except:
                    raise ValueError("Input file has wrong format")
                matrix[(row, col)] = val
            return rows, cols, matrix
    except Exception as e:
        raise ValueError(f"Error reading '{filename}': {e}")

def add_sparse_matrices(A, B):
    result = A.copy()
    for key, val in B.items():
        result[key] = result.get(key, 0) + val
    return result

def subtract_sparse_matrices(A, B):
    result = A.copy()
    for key, val in B.items():
        result[key] = result.get(key, 0) - val
    return result

def multiply_sparse_matrices(rowsA, colsA, A, rowsB, colsB, B):
    if colsA != rowsB:
        raise ValueError("Matrix dimensions do not allow multiplication.")

    B_by_row = {}
    for (k, j), valB in B.items():
        if k not in B_by_row:
            B_by_row[k] = []
        B_by_row[k].append((j, valB))

    result = {}
    for (i, k), valA in A.items():
        if k in B_by_row:
            for j, valB in B_by_row[k]:
                result[(i, j)] = result.get((i, j), 0) + valA * valB

    return rowsA, colsB, result

def print_sparse_matrix(matrix):
    for (r, c), v in sorted(matrix.items()):
        print(f"({r},{c},{v})")

def save_sparse_matrix_to_file(matrix, rows, cols, filename):
    with open(filename, 'w') as file:
        file.write(f"rows={rows}\n")
        file.write(f"cols={cols}\n")
        for (r, c), v in sorted(matrix.items()):
            file.write(f"({r},{c},{v})\n")
    print(f"Result saved to {filename}")

# Main Program

try:
    files = list_matrix_files()
    if len(files) < 2:
        raise FileNotFoundError("Need at least two matrix files in the folder.")

    # Select first matrix

    idx1 = int(input("\nSelect the first matrix by number (e.g., 1): ")) - 1
    idx2 = int(input("Select the second matrix by number (e.g., 2): ")) - 1
    fileA = files[idx1]
    fileB = files[idx2]

    rowsA, colsA, A = load_sparse_matrix(fileA)
    rowsB, colsB, B = load_sparse_matrix(fileB)

    print("\nChoose operation:\n1 - Addition\n2 - Subtraction\n3 - Multiplication")
    choice = input("Enter choice (1/2/3): ").strip()

    if choice == '1':
        if rowsA != rowsB or colsA != colsB:
            raise ValueError("Matrix sizes do not match for addition.")
        result = add_sparse_matrices(A, B)
        result_rows, result_cols = rowsA, colsA
        print("\nResult of M1 + M2 (Sparse Format):")
        print_sparse_matrix(result)

    elif choice == '2':
        if rowsA != rowsB or colsA != colsB:
            raise ValueError("Matrix sizes do not match for subtraction.")
        result = subtract_sparse_matrices(A, B)
        result_rows, result_cols = rowsA, colsA
        print("\nResult of M1 - M2 (Sparse Format):")
        print_sparse_matrix(result)

    elif choice == '3':
        result_rows, result_cols, result = multiply_sparse_matrices(rowsA, colsA, A, rowsB, colsB, B)
        print("\nResult of M1 × M2 (Sparse Format):")
        print_sparse_matrix(result)

    else:
        raise ValueError("Invalid operation choice.")

    # Ask user if they want to save result

    save = input("\nDo you want to save the result to a file? (yes/no): ").strip().lower()
    if save == 'yes':
        output_name = input("Enter the name of the output file (e.g., result.txt): ").strip()
        save_sparse_matrix_to_file(result, result_rows, result_cols, output_name)

except Exception as e:
    print(f"\n{e}")
