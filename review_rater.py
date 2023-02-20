import csv

import openai
import pandas as pd
import os

# Устанавливаем API-ключ для OpenAI



openai.api_key = "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"


# read input file
input_file = "reviews.csv"

with open(input_file, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    rows = list(reader)

    # analyze reviews and add ratings
    ratings = []
    for row in rows:
        text = row[1]
        response = openai.Completion.create(
          engine="text-davinci-002",
          prompt=(f"Rate this review on a scale of 1-10, where 10 is the most positive and 1 is the most negative.\n\n"
                  f"{text}\n"
                  f"Rating:"),
          max_tokens=1,
          n=1,
          stop=None,
          temperature=0.5,
        )
        rating = int(response.choices[0].text)
        ratings.append(rating)
        row.append(rating)

    # sort rows by rating
    rows_sorted = [row for _, row in sorted(zip(ratings, rows), reverse=True)]

    # write output file
    file_name = input_file.split(".")[0]
    with open(f"{file_name}_analyzed.csv", 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(header)
        csv_writer.writerows(rows_sorted)
