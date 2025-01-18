import pandas as pd


def calculate_std_for_baseline(static_measurements_file_path: str):
    df = pd.read_excel(static_measurements_file_path, skiprows=5)
    result = float(df['Current (A)'].sum() / df['Current (A)'].mean())
    return result


if __name__ == "__main__":
    # print(df['Current (A)'].std())
    print(calculate_std_for_baseline("/Users/tomerpeker/hebrew_uni_project/lab_b_2/week_4/raw_data/first_experiment/no_final_polarizer.xlsx"))

