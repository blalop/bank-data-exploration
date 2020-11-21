# So... what's this?

Lately, I've been looking for a way to measure my income, my expending, and be more clever about how I spend my money.

BBVA is a Spanish bank (mine to be precise, repo not sponsorized). Atlhought this bank provides some APIs via www.bbvaapimarket.com, I found myself too lazy to further investigate if they could fit my needs.

But I do have the habit of downloading all my monthly reports via web (in the operations page).

So, I've come to the conclusion that I should extract my bank movements for each of my monthly reports and make some data explotation with them.

## How does this work?

This repo consists of two different parts:

* A Python script that extracts data from monthly reports to a csv or sqlite file.
* A Jupyter notebook that loads the extracted data, performs some data exploration and shows it via matplotlib.
