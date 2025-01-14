import os
import json
import random
import argparse
from colorama import init, Fore, Style

class QuizPreparation:
    def __init__(self, questions_file):
        init()  # Initialize colorama
        self.questions = self.load_questions(questions_file)

    def clear_screen(self):
        """Clear the terminal screen based on the operating system."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def load_questions(self, file_path):
        """Load questions from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Fore.RED}Error: Questions file not found: {file_path}{Style.RESET_ALL}")
            exit(1)
        except json.JSONDecodeError:
            print(f"{Fore.RED}Error: Invalid JSON format in file: {file_path}{Style.RESET_ALL}")
            exit(1)

    def display_question_and_answers(self, question):
        """Display question and answers."""
        print(f"\n{question['number']}. {question['text']}")

        print("\nAnswers:")
        for i, answer in enumerate(question['answers'], start=0):
            answer_letter = chr(97 + i)  # Convert 0,1,2,3 to a,b,c,d
            print(f"{answer_letter}) {answer['text']}")

    def get_correct_answers(self, question):
        """Get set of correct answer letters for a question."""
        return {chr(97 + i) for i, answer in enumerate(question['answers'])
                if answer['correctness'] == 'correct'}

    def show_answer_feedback(self, question, user_answers_set):
        """Display color-coded feedback for each answer."""
        correct_answers_set = self.get_correct_answers(question)

        print("\nFeedback:")
        for i, answer in enumerate(question['answers']):
            answer_letter = chr(97 + i)

            if answer_letter in user_answers_set and answer['correctness'] == 'correct':
                # Correct selection
                print(f"{Fore.GREEN}{answer_letter}) {answer['text']}{Style.RESET_ALL}")
            elif answer_letter in user_answers_set and answer['correctness'] != 'correct':
                # Wrong selection
                print(f"{Fore.RED}{answer_letter}) {answer['text']}{Style.RESET_ALL}")
            elif answer_letter not in user_answers_set and answer['correctness'] == 'correct':
                # Missed correct answer
                print(f"{Fore.YELLOW}{answer_letter}) {answer['text']}{Style.RESET_ALL}")
            else:
                # Unselected incorrect answer
                print(f"{answer_letter}) {answer['text']}")

    def run(self, num_questions=None, min_question_number=None):
        """Run the quiz with specified parameters."""
        self.clear_screen()

        # Filter questions based on minimum question number if specified
        available_questions = self.questions
        if min_question_number is not None:
            available_questions = [q for q in available_questions if q['number'] > min_question_number]
            if not available_questions:
                print(f"{Fore.RED}No questions available with number greater than {min_question_number}{Style.RESET_ALL}")
                return

        # If num_questions not specified, ask user
        if num_questions is None:
            num_questions = input("How many questions would you like to prepare? (press Enter for all): ").strip()
            if not num_questions:
                num_questions = len(available_questions)
            else:
                try:
                    num_questions = int(num_questions)
                except ValueError:
                    print(f"{Fore.RED}Please enter a valid number{Style.RESET_ALL}")
                    return
                num_questions = min(num_questions, len(available_questions))

        # Ensure we don't try to select more questions than available
        num_questions = min(num_questions, len(available_questions))
        selected_questions = random.sample(available_questions, num_questions)
        correct_count = 0

        for i, question in enumerate(selected_questions, start=1):
            self.clear_screen()
            print(f"Question {i} of {num_questions}")

            self.display_question_and_answers(question)

            user_answers = input("\nEnter your answers (e.g., a,b,c): ").strip().lower().replace(" ", "")
            user_answers_set = set(user_answers.split(","))
            correct_answers_set = self.get_correct_answers(question)

            self.show_answer_feedback(question, user_answers_set)

            if user_answers_set == correct_answers_set:
                correct_count += 1
                print(f"\n{Fore.GREEN}Correct!{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}Incorrect. The correct answer(s): {', '.join(sorted(correct_answers_set))}{Style.RESET_ALL}")

            print(f"\nCurrent score: {correct_count}/{i}")
            input("\nPress Enter to continue...")

        self.clear_screen()
        print(f"\n{Fore.BLUE}Quiz completed!{Style.RESET_ALL}")
        print(f"Final score: {correct_count}/{num_questions}")

def get_default_questions_path():
    """Get the path to the default questions file included with the package."""
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'questions_en.json')

def main():
    parser = argparse.ArgumentParser(description='Run a quiz with specified parameters.')
    parser.add_argument('questions', type=int, nargs='?', help='Number of questions to ask')
    parser.add_argument('--from', dest='min_question', type=int, help='Minimum question number to include')
    parser.add_argument('--file', default=get_default_questions_path(), help='Path to questions JSON file')
    args = parser.parse_args()

    quiz = QuizPreparation(args.file)
    quiz.run(num_questions=args.questions, min_question_number=args.min_question)

if __name__ == "__main__":
    main()
