import json

from ollama import chat
from prompts import SYSTEM_PROMPT
from validator import validate_evaluation, check_grounding


MODEL_NAME = "llama3.2"
MAX_RETRIES = 3


def evaluate_cv(cv_data, job_description):

    user_prompt = f"""
CV JSON:
{json.dumps(cv_data, indent=2)}

JOB DESCRIPTION:
{job_description}
"""

    previous_error = None

    for attempt in range(MAX_RETRIES):

        if previous_error:

            user_prompt = f"""
CV JSON:
{json.dumps(cv_data, indent=2)}

JOB DESCRIPTION:
{job_description}

The previous response failed validation because:

{previous_error}

Correct the response.

Remember:
- Return ONLY valid JSON.
- Score must be an integer from 1 to 10.
- Summary must contain exactly 2 sentences.
- Use only information explicitly present in the CV.
- Never claim the candidate has or lacks a skill unless the CV explicitly supports that claim.
- If a skill is not mentioned, say it is "not evidenced in the CV".
- If all important requirements are explicitly evidenced in the CV, do not invent a missing requirement.
- For a strong candidate, the second sentence should describe why their experience and background support the role.
- Do not use phrases such as "the most important missing requirement" when no requirement is actually missing.
"""

        response = chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            format="json",
            options={
                "temperature": 0,
                "num_predict": 150
            }
        )

        try:

            evaluation = json.loads(
                response.message.content
            )

            print("LLM response:")
            print(json.dumps(evaluation, indent=4))

            validate_evaluation(evaluation)

            check_grounding(
                evaluation,
                cv_data
            )

            print(
                f"Evaluation passed on attempt "
                f"{attempt + 1}."
            )

            return evaluation

        except (
            json.JSONDecodeError,
            ValueError
        ) as error:

            previous_error = str(error)

            print(
                f"Validation failed on attempt "
                f"{attempt + 1}/{MAX_RETRIES}: "
                f"{previous_error}"
            )

    raise ValueError(
        f"Evaluation failed after {MAX_RETRIES} attempts."
    )