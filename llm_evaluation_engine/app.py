import json

from evaluator import evaluate_cv


JOB_DESCRIPTION = """
DevLogix is looking for a Python Developer with experience in:

- Python
- SQL
- Machine Learning
- Git
- APIs
- Streamlit

The candidate should have relevant project, internship, or development experience.
A Computer Science or related educational background is preferred.
"""


def main():

    # Open and read the CV JSON file
    with open("sample_cv.json", "r", encoding="utf-8") as file:
        cv_data = json.load(file)

    print("Evaluating CV...\n")

    try:
        # Send CV and Job Description to Llama
        evaluation = evaluate_cv(
            cv_data,
            JOB_DESCRIPTION
        )

        print("Raw LLM output:")
        print(json.dumps(evaluation, indent=4))
        print()
        
        # Check that Llama returned the correct format

        print("Evaluation successful!\n")

        # Print the final result
        print(json.dumps(evaluation, indent=4))

    except json.JSONDecodeError:
        print("Error: The model returned invalid JSON.")

    except ValueError as error:
        print(f"Validation Error: {error}")

    except Exception as error:
        print(f"Unexpected Error: {error}")


if __name__ == "__main__":
    main()