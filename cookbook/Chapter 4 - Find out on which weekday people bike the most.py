# %%
import polars as pl
import matplotlib.pyplot as plt

# Make the graphs a bit prettier, and bigger
plt.style.use("ggplot")
plt.rcParams["figure.figsize"] = (15, 5)
plt.rcParams["font.family"] = "sans-serif"

# Show more columns when displaying data frames.
pl.Config.set_tbl_width_chars(5000)
pl.Config.set_tbl_cols(60)

# %% Load the data
bikes = pl.read_csv(
    "../data/bikes.csv",
    separator=";",
    encoding="latin1",
).with_columns(pl.col("Date").str.to_date("%d/%m/%Y"))
plt.plot(bikes["Date"].to_list(), bikes["Berri 1"].to_list())
plt.xlabel("Date")
plt.show()

# %% Plot Berri 1 data
# Next up, we're just going to look at the Berri bike path. Berri is a street in Montreal, with a pretty important bike path. I use it mostly on my way to the library now, but I used to take it to work sometimes when I worked in Old Montreal.

# Keep the dates alongside the Berri bikepath counts, since Polars has no index.
pl_berri_bikes = bikes.select("Date", "Berri 1")
pl_berri_bikes.head(5)


# %% Add weekday column
# Next, we need to add a 'weekday' column. In Polars, dates stay in a regular column.

pl_berri_bikes["Date"]

# You can see that actually some of the days are missing -- only 310 days of the year are actually there. Who knows why.

# Polars has time series functionality for getting the day of the month:
pl_berri_bikes["Date"].dt.day()

# We actually want the weekday, though:
pl_berri_bikes["Date"].dt.weekday() - 1

# Polars numbers Monday as 1, so subtract 1 to keep Monday as 0.

# Now that we know how to *get* the weekday, we can add it as a column in our dataframe like this:
pl_berri_bikes = pl_berri_bikes.with_columns(
    (pl.col("Date").dt.weekday() - 1).alias("weekday")
)
pl_berri_bikes.head(5)


# %%
# Let's add up the cyclists by weekday
# This turns out to be really easy!

# Dataframes have a `.group_by()` method that is similar to SQL GROUP BY.
# Group the rows by weekday, add up the bike counts, and sort Monday to Sunday.
weekday_counts = pl_berri_bikes.group_by("weekday").agg(pl.col("Berri 1").sum()).sort("weekday")
weekday_counts


# %% Rename weekdays
weekday_names = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
weekday_counts = weekday_counts.with_columns(
    pl.col("weekday").replace_strict(dict(enumerate(weekday_names)))
)


# %% Plot results
plt.figure()
plt.bar(weekday_counts["weekday"].to_list(), weekday_counts["Berri 1"].to_list(), label="Berri 1")
plt.xticks(rotation=90)
plt.legend()
plt.show()

# %% Final message
print("Analysis complete!")
