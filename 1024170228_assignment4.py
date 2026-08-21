"""
UCS420: Cognitive Computing
Assignment 4 - A Cognitive FAQ System Using Pandas
Roll Number: 1024170228
"""

import pandas as pd

# ---------------------------------------------------------------------------
# Q1: Build Your Personalized Knowledge Base
# ---------------------------------------------------------------------------

roll_number = "1024170228"

# Last two digits of roll number -> 2, 8
last_two_digits = [int(d) for d in roll_number[-2:]]

categories = ["billing", "account", "general"]

# digit 2 -> categories[2 % 3] = categories[2] = "general"
# digit 8 -> categories[8 % 3] = categories[2] = "general"
digit_categories = [categories[d % 3] for d in last_two_digits]
print(f"Roll number last two digits: {last_two_digits}")
print(f"Assigned categories: {digit_categories}\n")

fixed_entries = [
    {"question": "what is the annual fee", "answer": "The annual fee is Rs 500.",
     "keywords": "fee cost price charge", "category": "billing"},
    {"question": "how to reset password", "answer": "Go to Settings > Reset Password.",
     "keywords": "password reset login", "category": "account"},
    {"question": "what are your working hours", "answer": "We are open 9 AM to 5 PM.",
     "keywords": "hours timing open time", "category": "general"},
    {"question": "how can i pay the fee", "answer": "You can pay via UPI, card, or net banking.",
     "keywords": "pay payment upi fee", "category": "billing"},
]

# Personalized entries (both fall in "general" for this roll number)
personalized_entries = [
    {"question": "how can i contact customer support",
     "answer": "You can reach customer support via email at support@college.edu or call the helpdesk.",
     "keywords": "contact support help", "category": digit_categories[0]},
    {"question": "where is your office located",
     "answer": "Our office is located at the main campus building, Block A, Room 101.",
     "keywords": "location address office", "category": digit_categories[1]},
]

all_entries = fixed_entries + personalized_entries
df = pd.DataFrame(all_entries)

print("Q1: Final 6-row FAQ DataFrame")
print(df.to_string(index=False))
print()

# ---------------------------------------------------------------------------
# Q2: Generate and Score a Hypothesis
# ---------------------------------------------------------------------------

def score_query(query, dataframe):
    """
    Scores every FAQ entry against the query string based on keyword overlap.
    Returns a DataFrame of matches ranked by confidence (highest first).
    """
    query_words = set(query.lower().split())
    scores = []

    for idx, row in dataframe.iterrows():
        entry_keywords = set(row["keywords"].lower().split())
        overlap = query_words & entry_keywords
        score = len(overlap)
        if score > 0:
            scores.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score
            })

    result_df = pd.DataFrame(scores)
    if not result_df.empty:
        result_df = result_df.sort_values(by="score", ascending=False).reset_index(drop=True)
    return result_df


print("Q2: Scoring a sample query -> 'how do i pay fee'")
print(score_query("how do i pay fee", df).to_string(index=False))
print()

# ---------------------------------------------------------------------------
# Q3: same_category function
# ---------------------------------------------------------------------------

def same_category(category_name, dataframe):
    """Returns all questions belonging to a given category."""
    return dataframe[dataframe["category"] == category_name][["question", "category"]]


# Using the category of one of the personalized entries from Q1 ("general")
sample_category = personalized_entries[0]["category"]
print(f"Q3: All questions in category '{sample_category}'")
print(same_category(sample_category, df).to_string(index=False))
print()

# ---------------------------------------------------------------------------
# Q4: Update an entry's keywords via user input and save to CSV
# ---------------------------------------------------------------------------

# Pick one entry to update (index 0: "what is the annual fee")
entry_index = 0
print(f"Q4: Updating keywords for entry -> '{df.loc[entry_index, 'question']}'")

new_keyword = input("Enter a new keyword to add to this entry's keywords: ").strip()

if new_keyword:
    df.at[entry_index, "keywords"] = df.at[entry_index, "keywords"] + " " + new_keyword

csv_filename = f"{roll_number}_faq_data.csv"
df.to_csv(csv_filename, index=False)
print(f"Updated DataFrame saved to '{csv_filename}'\n")

# ---------------------------------------------------------------------------
# Q5: Count FAQ entries per category using groupby
# ---------------------------------------------------------------------------

print("Q5: Number of FAQ entries per category")
category_counts = df.groupby("category").size()
print(category_counts.to_string())
print()

# ---------------------------------------------------------------------------
# Q6: Modified scoring function that reports ties instead of picking one
# ---------------------------------------------------------------------------

def score_query_with_ties(query, dataframe):
    """
    Scores every FAQ entry against the query string based on keyword overlap.
    If multiple entries tie for the top score, ALL of them are printed
    instead of silently picking one.
    """
    query_words = set(query.lower().split())
    scores = []

    for idx, row in dataframe.iterrows():
        entry_keywords = set(row["keywords"].lower().split())
        overlap = query_words & entry_keywords
        score = len(overlap)
        if score > 0:
            scores.append({
                "question": row["question"],
                "answer": row["answer"],
                "category": row["category"],
                "score": score
            })

    result_df = pd.DataFrame(scores)
    if result_df.empty:
        print("No matching entries found.")
        return result_df

    result_df = result_df.sort_values(by="score", ascending=False).reset_index(drop=True)
    top_score = result_df.iloc[0]["score"]
    top_matches = result_df[result_df["score"] == top_score]

    if len(top_matches) > 1:
        print(f"Tie detected! {len(top_matches)} entries share the top score of {top_score}:")
        print(top_matches.to_string(index=False))
    else:
        print("Best match:")
        print(top_matches.to_string(index=False))

    return result_df


print("Q6a: Query that produces a TIE -> 'fee'")
score_query_with_ties("fee", df)
print()

print("Q6b: Query that does NOT produce a tie -> 'password reset'")
score_query_with_ties("password reset", df)
