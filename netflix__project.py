import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("netflix_titles.csv")
print("====================================================")
# DATA UNDERSTANDING
print(df.head())
print(df.shape)
print(df.columns)
print(df.info())
print(df.describe())
print(df.isnull().sum())
print("Duplicate Rows:", df.duplicated().sum())
print("=====================================================")
# DATA CLEANING
df["director"] = df["director"].fillna("Unknown")
df["cast"] = df["cast"].fillna("Unknown")
df["country"] = df["country"].fillna("Unknown")
df["rating"] = df["rating"].fillna("Unknown")
df["duration"] = df["duration"].fillna("Unknown")
df["date_added"] = pd.to_datetime(df["date_added"],errors="coerce")
print(df.isnull().sum())
df["date_added"] = df["date_added"].fillna(pd.Timestamp("1900-01-01"))
print(df["date_added"].isnull().sum())
print(df["date_added"].dtype)
print("=====================================================")
# DATA TRANSFORMATION
df["added_year"] = df["date_added"].dt.year
df["added_month"] = df["date_added"].dt.month
df["added_month_name"] = df["date_added"].dt.month_name()

print(df[["title","date_added","added_year","added_month","added_month_name"]].head())
print("=====================================================")
# Basic Pandas Analysis
type_report = df["type"].value_counts()
print(type_report)
print(df["type"].unique())
print(df["type"].nunique())
rating_report = df["rating"].value_counts()
print(rating_report)
top_ratings = df["rating"].value_counts().head(10)
print(top_ratings)
release_year_report = df["release_year"].value_counts().sort_index()
print(release_year_report)
latest_year = df["release_year"].max()
print("Latest Release Year:",latest_year)
oldest_year = df["release_year"].min()
print("Oldest Release Year:",oldest_year)
print("=====================================================")
# GROUPBY ANALYSIS
country_report = df["country"].value_counts()
print(country_report.head(10))
director_report = df["director"].value_counts()
print(director_report.head(10))
genre_report = df["listed_in"].value_counts()
print(genre_report.head(10))
year_report = df.groupby("release_year")["show_id"].count()
print(year_report)
type_year_report = df.groupby(["release_year","type"])["show_id"].count()
print(type_year_report)
print("=====================================================")
# Multiple Values split karna
country_data = df["country"].str.split(", ").explode()
country_data = country_data[country_data != "Unknown"]
country_report = country_data.value_counts()
print(country_report.head(10))
top_countries = country_report.head(10)
print(top_countries)
print("=====================================================")
# Genres Properly Split karna
genre_data = df["listed_in"].str.split(", ").explode()
genre_report = genre_data.value_counts()
print(genre_report.head(10))
print("=====================================================")
# Movie Duration
print(df["duration"].value_counts().head(20))
movie_data = df[df["type"] == "Movie"]
tv_data = df[df["type"] == "TV Show"]
print("Movies:",movie_data.shape[0])
print("TV Shows:",tv_data.shape[0])
print("=====================================================")
# apply() + lambda
df["duration_value"] = df["duration"].apply(lambda x: int(x.split(" ")[0]) if x != "Unknown" else 0)
print(df[["title","type","duration","duration_value"]].head(20))
print("=====================================================")
# map()
type_map = {"Movie": "Film","TV Show": "Series"}
df["content_type"] = df["type"].map(type_map)
print(df[["type","content_type"]].head())
print("=====================================================")
# astype()
df["duration_value"] = df["duration_value"].astype(int)
print(df["duration_value"].dtype)
print("=====================================================")
# Movie Average Duration
movie_duration = df[df["type"] == "Movie"]
average_movie_duration = movie_duration["duration_value"].mean()
print("Average Movie Duration:",average_movie_duration)

tv_duration = df[df["type"] == "TV Show"]
average_tv_seasons = tv_duration["duration_value"].mean()
print("Average TV Show Seasons:",average_tv_seasons)
print("=====================================================")
# pivot_table()
year_type_pivot = pd.pivot_table(df,index="release_year",columns="type",values="show_id",aggfunc="count",fill_value=0)
print(year_type_pivot)
print("=====================================================")
# Top 10 Release Years
top_release_years = (df["release_year"].value_counts().sort_values(ascending=False).head(10))
print(top_release_years)
print("=====================================================")
# Top Directors
top_directors = (df[df["director"] != "Unknown"]["director"].value_counts().head(10))
print(top_directors)
print("=====================================================")
# Top Countries
top_countries = country_report.sort_values(ascending=False).head(10)
print(top_countries)
print("=====================================================")
# Top Genres
top_genres = genre_report.sort_values(ascending=False).head(10)
print(top_genres)
print("=====================================================")
# Final Pandas Analysis
movies = df[df["type"] == "Movie"].copy()
tv_shows = df[df["type"] == "TV Show"].copy()
print("Movies:", movies.shape)
print("TV Shows:", tv_shows.shape)
# concat
final_data = pd.concat([movies, tv_shows],ignore_index=True)
print(final_data.shape)
print("=====================================================")
# Final Cleaned CSV
final_data.to_csv("Netflix_Final_Cleaned.csv",index=False)
print("Final Cleaned File Saved Successfully!")
print("=====================================================")
# Final Verification
print(final_data.head())
print(final_data.shape)
print(final_data.isnull().sum())
print(final_data.dtypes)
print("=====================================================")
# Matplotlib Setup
import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("Netflix_Final_Cleaned.csv")
print(df.head())
print(df.shape)
print("=====================================================")
# Movies vs TV Shows
type_report = df["type"].value_counts()
print(type_report)
plt.figure(figsize=(8,6))
plt.pie(type_report.values,labels=type_report.index,autopct="%1.1f%%",startangle=90)
plt.title("Netflix Movies vs TV Shows",fontsize=16,fontweight="bold")
plt.tight_layout()
plt.show()
print("=====================================================")
# Top 10 Countries barh()
plt.figure(figsize=(10, 6))
bars = plt.barh(top_countries.index,top_countries.values,edgecolor="black")
plt.title("Top 10 Countries by Netflix Content",fontsize=16,fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("Country")
# Show values on bars
plt.bar_label(bars,padding=3)
# Grid
plt.grid(axis="x",linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Top 10 Genres barh()
# Split genres
genre_data = df["listed_in"].str.split(", ").explode()

# Top 10 genres
top_genres = genre_data.value_counts().head(10)

print(top_genres)

# Horizontal Bar Chart
plt.figure(figsize=(10, 6))
bars = plt.barh(top_genres.index,top_genres.values,edgecolor="black")
plt.title("Top 10 Netflix Genres",fontsize=16,fontweight="bold")
plt.xlabel("Number of Titles")
plt.ylabel("Genre")
# Values on bars
plt.bar_label(bars,padding=3)
# Grid
plt.grid(axis="x",linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Count titles by release year
year_data = df["release_year"].value_counts().sort_index()
print(year_data)
# Line Chart
plt.figure(figsize=(12, 6))
plt.plot(year_data.index,year_data.values,marker="o",linewidth=2)
plt.title("Netflix Content by Release Year",fontsize=16,fontweight="bold")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.grid(linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Rating Distribution
# Count ratings
rating_data = df["rating"].value_counts()
print(rating_data)
# Bar Chart
plt.figure(figsize=(10, 6))
bars = plt.bar(rating_data.index,rating_data.values,edgecolor="black")
plt.title("Netflix Rating Distribution",fontsize=16,fontweight="bold")
plt.xlabel("Rating")
plt.ylabel("Number of Titles")
# Values on bars
plt.bar_label(bars,padding=3)
plt.xticks(rotation=45)
plt.grid(axis="y",linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Movie Duration Histogram
# Sirf Movies select karo
movie_data = df[df["type"] == "Movie"]
# Movie duration
movie_duration = movie_data["duration_value"]
print(movie_duration.describe())
# Histogram
plt.figure(figsize=(10, 6))
plt.hist(movie_duration,bins=20,edgecolor="black")
plt.title("Netflix Movie Duration Distribution",fontsize=16,fontweight="bold")
plt.xlabel("Duration (Minutes)")
plt.ylabel("Number of Movies")
plt.grid(axis="y",linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Movie vs TV Show by Year
# Movie vs TV Show by Release Year
year_type_data = (df.groupby(["release_year", "type"]).size().unstack(fill_value=0))
print(year_type_data)
plt.figure(figsize=(12, 6))
plt.plot(year_type_data.index,year_type_data["Movie"],marker="o",label="Movies")
plt.plot(year_type_data.index,year_type_data["TV Show"],marker="o",label="TV Shows")
plt.title("Netflix Movies vs TV Shows by Release Year",fontsize=16,fontweight="bold")
plt.xlabel("Release Year")
plt.ylabel("Number of Titles")
plt.legend()
plt.grid(linestyle="--",alpha=0.5)
plt.tight_layout()
plt.show()
print("=====================================================")
# Final Netflix Analytics Dashboard
# ==========================================
# FINAL NETFLIX ANALYTICS DASHBOARD
# ==========================================

fig = plt.figure(figsize=(18, 12))

fig.suptitle("Netflix Analytics Dashboard",fontsize=22,fontweight="bold")

ax1 = plt.subplot(2, 3, 1)

ax1.pie(type_report.values,labels=type_report.index,autopct="%1.1f%%",startangle=90)
ax1.set_title("Movies vs TV Shows")

ax2 = plt.subplot(2, 3, 2)

bars = ax2.barh(top_countries.index,top_countries.values,edgecolor="black")

ax2.set_title("Top 10 Countries")

ax2.set_xlabel("Number of Titles")

ax2.bar_label(bars,padding=3)

ax3 = plt.subplot(2, 3, 3)

bars = ax3.barh(top_genres.index,top_genres.values,edgecolor="black")

ax3.set_title("Top 10 Genres")

ax3.set_xlabel("Number of Titles")
ax3.bar_label(bars,padding=3)

ax4 = plt.subplot(2, 3, 4)

ax4.plot(year_data.index,year_data.values, marker="o")

ax4.set_title("Netflix Content by Release Year")
ax4.set_xlabel("Release Year")
ax4.set_ylabel("Number of Titles")
ax4.grid(linestyle="--",alpha=0.5)

ax5 = plt.subplot(2, 3, 5)
bars = ax5.bar(rating_data.index,rating_data.values,edgecolor="black")

ax5.set_title("Rating Distribution")
ax5.set_xlabel("Rating")
ax5.set_ylabel("Number of Titles")
ax5.tick_params(axis="x",rotation=45)

ax6 = plt.subplot(2, 3, 6)
ax6.hist(movie_duration,bins=20,edgecolor="black")
ax6.set_title("Movie Duration Distribution")
ax6.set_xlabel("Duration (Minutes)")
ax6.set_ylabel("Number of Movies")

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.show()
print("=====================================================")
print("=====================================================")

