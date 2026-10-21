
# %%
from pathlib import Path
import polars as pl
import matplotlib.pyplot as plt
import io


# %%
# Locate the data file relative to this Python script.
# Script: cookbook/Chapter 1 - Reading from a CSV.py
# Data:   data/bikes.csv

project_root = Path(__file__).resolve().parent.parent
data_path = project_root / "data" / "bikes.csv"

print("Data file:", data_path)
print("File exists:", data_path.exists())

# Read the CSV text using the correct encoding.
with open(data_path, "r", encoding="ISO-8859-1") as f:
    bikes_csv = f.read()


# %%
# Reading data from a CSV file
# First, use the default comma separator to demonstrate
# why the original data appears broken.

pl_broken_df = pl.read_csv(io.StringIO(bikes_csv))

print("\n--- Original data read with the default separator ---")
print(pl_broken_df.head(3))


# %%
# Read the CSV with the correct separator.
# The original file uses semicolons.
fixed_df = pl.read_csv(
    io.StringIO(bikes_csv),
    separator=";"
)

# Parse the Date column, with day before month.
fixed_df = fixed_df.with_columns(
    pl.col("Date").str.strptime(
        pl.Date,
        format="%d/%m/%Y",
        strict=False
    )
)

print("\n--- Correctly parsed data: first 3 rows ---")
print(fixed_df.head(3))

print("\n--- Data schema ---")
print(fixed_df.schema)

print("\n--- Null counts ---")
print(fixed_df.null_count())


# %%
# Selecting a column
print("\n--- Berri 1 column ---")
print(fixed_df["Berri 1"])


# %%
# Plotting one bike path
plt.figure(figsize=(15, 5))

plt.plot(
    fixed_df["Date"].to_list(),
    fixed_df["Berri 1"].to_list()
)

plt.xlabel("Date")
plt.ylabel("Number of cyclists")
plt.title("Daily cyclist counts on Berri 1")
plt.tight_layout()
plt.show()


# %%
# Plot all bike paths
plt.figure(figsize=(15, 10))

for column in fixed_df.columns:
    if column != "Date":
        plt.plot(
            fixed_df["Date"].to_list(),
            fixed_df[column].to_list(),
            label=column
        )

plt.xlabel("Date")
plt.ylabel("Number of cyclists")
plt.title("Daily cyclist counts on Montreal bike paths")
plt.legend()
plt.tight_layout()
plt.show()

