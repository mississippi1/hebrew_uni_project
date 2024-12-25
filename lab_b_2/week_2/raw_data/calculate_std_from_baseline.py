import pandas as pd


def calculate_std_for_baseline():
    df = pd.read_excel("/Users/tomerpeker/hebrew_uni_project/lab_b_2/week_2/raw_data/quarter_wave/static_measurments.xlsx", skiprows=5)
    result = float(df['Current (A)'].std() / df['Current (A)'].mean())
    return result


if __name__ == "__main__":
    print(calculate_std_for_baseline())

