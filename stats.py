import requests
import time
import json
from typing import List, Dict

# Define the questions JSON
questions_file = "questions_en.json"
with open(questions_file, "r") as file:
    questions_json = json.load(file)

API_BASE_URL = "https://api.counterapi.dev/v1/putCybersecurityQuiz/"
RATE_LIMIT = 10  # requests per second
DELAY_BETWEEN_BATCHES = 1  # seconds

def fetch_count(question_number: int, count_type: str) -> int:
    """
    Fetches the count for a given question number and type (LIKE or DISLIKE).
    Returns 0 if the count doesn't exist or an error occurs.
    """
    url = f"{API_BASE_URL}Q{question_number}_{count_type}/"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            count = data.get("count", 0)
            return count
        elif response.status_code in [400, 404]:
            # Silently ignore 404 and 400 errors (count doesn't exist)
            return 0
        else:
            # For other unexpected status codes, log the error and return 0
            print(f"Unexpected error fetching {count_type} for question {question_number}: {response.status_code} {response.reason}")
            return 0
    except requests.RequestException as e:
        print(f"Error fetching {count_type} for question {question_number}: {e}")
        return 0
    except json.JSONDecodeError:
        print(f"Invalid JSON response for {count_type} of question {question_number}.")
        return 0

def main():
    results = []
    requests_made = 0

    for question in questions_json:
        number = question["number"]
        # Fetch LIKE count
        like_count = fetch_count(number, "LIKE")
        requests_made += 1

        # Fetch DISLIKE count
        dislike_count = fetch_count(number, "DISLIKE")
        requests_made += 1

        results.append({
            "number": number,
            "text": question["text"],
            "likes": like_count,
            "dislikes": dislike_count
        })

        # Handle rate limiting
        if requests_made % RATE_LIMIT == 0:
            time.sleep(DELAY_BETWEEN_BATCHES)

    # Sort the results by dislikes in descending order
    sorted_results = sorted(results, key=lambda x: x["dislikes"], reverse=True)

    # Display the ranked results
    print("\nQuiz Questions Ranked by Highest Dislikes:\n")
    for item in sorted_results[:30]:
        print(f"Question {item['number']}: {item['text']}")
        print(f"Likes: {item['likes']} | Dislikes: {item['dislikes']}\n")

    # Sort the results by likes in descending order
    sorted_results = sorted(results, key=lambda x: x["likes"], reverse=True)

    # Display the ranked results
    print("\nQuiz Questions Ranked by Highest Likes:\n")
    for item in sorted_results[:30]:
        print(f"Question {item['number']}: {item['text']}")
        print(f"Likes: {item['likes']} | Dislikes: {item['dislikes']}\n")

if __name__ == "__main__":
    main()