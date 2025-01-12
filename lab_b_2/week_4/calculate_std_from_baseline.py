import pandas as pd


def calculate_std_for_baseline(static_measurements_file_path: str):
    df = pd.read_excel(static_measurements_file_path, skiprows=5)
    result = float(df['Current (A)'].std() / df['Current (A)'].mean())
    return result


if __name__ == "__main__":
    print(calculate_std_for_baseline())

