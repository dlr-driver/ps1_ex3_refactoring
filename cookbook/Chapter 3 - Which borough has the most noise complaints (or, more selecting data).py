# %%
import polars as pl
import matplotlib.pyplot as plt


# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)

# Show more columns when displaying data frames.
pl.Config.set_tbl_width_chars(5000)
pl.Config.set_tbl_cols(60)

# %%
# Let's continue with our NYC 311 service requests example.
# Read all columns as strings to avoid errors from mixed types.
pl_complaints = pl.read_csv("../data/311-service-requests.csv", infer_schema=False)


# %%
# 3.1 Selecting only noise complaints
# I'd like to know which borough has the most noise complaints. First, we'll take a look at the data to see what it looks like:
pl_complaints.head(5)


# %%
# To get the noise complaints, we need to find the rows where the "Complaint Type" column is "Noise - Street/Sidewalk".
noise_complaints = pl_complaints.filter(pl.col("Complaint Type") == "Noise - Street/Sidewalk")
noise_complaints.head(3)


# %%
# Combining more than one condition
is_noise = pl.col("Complaint Type") == "Noise - Street/Sidewalk"
in_brooklyn = pl.col("Borough") == "BROOKLYN"
pl_complaints.filter(is_noise & in_brooklyn).head(5)


# %%
# If we just wanted a few columns:
pl_complaints.filter(is_noise & in_brooklyn).select(
    ["Complaint Type", "Borough", "Created Date", "Descriptor"]
).head(10)


# %%
# 3.3 So, which borough has the most noise complaints?
is_noise = pl.col("Complaint Type") == "Noise - Street/Sidewalk"
noise_complaints = pl_complaints.filter(is_noise)
noise_complaints["Borough"].drop_nulls().value_counts(sort=True)


# %%
# What if we wanted to divide by the total number of complaints?
noise_complaint_counts = noise_complaints["Borough"].drop_nulls().value_counts(sort=True)
complaint_counts = pl_complaints["Borough"].drop_nulls().value_counts(sort=True)

# Align counts by borough before dividing.
noise_complaint_ratios = (
    complaint_counts.join(
        noise_complaint_counts.rename({"count": "noise_count"}),
        on="Borough",
        how="left",
    )
    .select("Borough", (pl.col("noise_count") / pl.col("count")).alias("ratio"))
    .sort("Borough")
)
noise_complaint_ratios


# %%
# Plot the results
plt.bar(noise_complaint_ratios["Borough"].to_list(), noise_complaint_ratios["ratio"].to_numpy())
plt.title("Noise Complaints by Borough (Normalized)")
plt.xlabel("Borough")
plt.ylabel("Ratio of Noise Complaints to Total Complaints")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
