# So... what's this?

Lately, I've been looking for a way to measure my income, my expending, and be more clever about how I spend my money.

BBVA is a Spanish bank (mine to be precise, repo not sponsorized). Atlhought this bank provides some APIs via www.bbvaapimarket.com, I found myself too lazy to further investigate if they could fit my needs.

But I do have the habit of downloading all my monthly reports via web (in the operations page).

So, I've come to the conclusion that I should extract my bank movements for each of my monthly reports and make some data explotation with them.

## How does this work?

This repo consists of three different parts:

* A Python script extractor.py, that expects the directory where the reports live as argument. It will extract the data from all the reports and write them to a CSV file.
* A small SQL script load.sql, used to load the CSV into a SQLite 3 database.
* A Jupyter notebook that loads the CSV into Pandas, performs some data exploration and shows it via matplotlib.
