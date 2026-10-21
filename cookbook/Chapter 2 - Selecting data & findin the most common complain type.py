# %%
import pandas as pd
import matplotlib.pyplot as plt
import polars as pl

# %%
# We're going to use a new dataset here, to demonstrate how to deal with larger datasets. This is a subset of the of 311 service requests from [NYC Open Data](https://nycopendata.socrata.com/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9).
# because of mixed types we specify dtype to prevent any errors
complaints = pd.read_csv("../data/311-service-requests.csv", dtype="unicode")
complaints.head()

# %%
# TODO: rewrite the above using the polars library and call the data frame pl_complaints
# Hint: we need the dtype argument reading all columns in as strings above in Pandas due to the zip code column containing NaNs as "NA" and some zip codes containing a dash like 1234-456
# you cannot exactly do the same in Polars but you can read about some other solutions here:
# see a discussion about dtype argument here: https://github.com/pola-rs/polars/issues/8230

# Polars equivalent of dtype="unicode": infer_schema=False reads every column as a string (pl.String).
# try_parse_dates=False keeps dates as text (the calmcode course writes this as parse_dates=False,
# which was the older name of the argument).
pl_complaints = pl.read_csv(
    "../data/311-service-requests.csv",
    infer_schema=False,
    try_parse_dates=False,
)
pl_complaints.head()

# %%
# Selecting columns:
complaints["Complaint Type"]

# %%
# TODO: rewrite the above using the polars library
# Indexing with a column name returns a Series, like in pandas:
pl_complaints["Complaint Type"]

# The more idiomatic Polars way is select() with an expression, which returns a DataFrame:
pl_complaints.select(pl.col("Complaint Type"))

# %%
# Get the first 5 rows of a dataframe
complaints[:5]

# %%
# TODO: rewrite the above using the polars library
# Polars has no index, so we just ask for the first 5 rows:
pl_complaints.head(5)

# %%
# Combine these to get the first 5 rows of a column:
complaints["Complaint Type"][:5]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.select(pl.col("Complaint Type")).head(5)


# %%
# Selecting multiple columns
complaints[["Complaint Type", "Borough"]]

# %%
# TODO: rewrite the above using the polars library
pl_complaints.select(["Complaint Type", "Borough"])

# %%
# What's the most common complaint type?
complaint_counts = complaints["Complaint Type"].value_counts()
complaint_counts[:10]

# %%
# TODO: rewrite the above using the polars library
# value_counts() returns a DataFrame with the complaint type and a "count" column
pl_complaint_counts = pl_complaints["Complaint Type"].value_counts(sort=True)
pl_complaint_counts.head(10)

# The same result written with expressions, closer to the calmcode style:
# pl_complaints.group_by("Complaint Type").agg(pl.len().alias("count")).sort("count", descending=True).head(10)

# %%
# Plot the top 10 most common complaints
complaint_counts[:10].plot(kind="bar")
plt.title("Top 10 Complaint Types")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

# %%
# TODO: please do the same with Polars
# Polars' own .plot needs the altair package, so we pass the columns straight to matplotlib instead.
pl_top10 = pl_complaint_counts.head(10)
plt.bar(pl_top10["Complaint Type"], pl_top10["count"])
plt.title("Top 10 Complaint Types (Polars)")
plt.xlabel("Complaint Type")
plt.ylabel("Count")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.show()

