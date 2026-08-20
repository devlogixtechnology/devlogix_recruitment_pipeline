def count_sentences(text):
    sentences = [
        sentence.strip()
        for sentence in text.replace("!", ".").replace("?", ".").split(".")
        if sentence.strip()
    ]

    return len(sentences)


def validate_evaluation(evaluation):

    if not isinstance(evaluation, dict):
        raise ValueError("Output must be a JSON object.")

    required_keys = {"score", "summary"}

    if set(evaluation.keys()) != required_keys:
        raise ValueError(
            "Output must contain exactly: score and summary."
        )

    score = evaluation["score"]

    if isinstance(score, bool) or not isinstance(score, int):
        raise ValueError("Score must be an integer.")

    if not 1 <= score <= 10:
        raise ValueError("Score must be between 1 and 10.")

    summary = evaluation["summary"]

    if not isinstance(summary, str):
        raise ValueError("Summary must be a string.")

    if count_sentences(summary) != 2:
        raise ValueError("Summary must contain exactly 2 sentences.")

    return True




import re


def check_grounding(evaluation, cv_data):
    """
    Checks whether the LLM claims that information explicitly
    present in the CV is missing or unsupported.
    """

    summary = evaluation["summary"].lower()

    # -------------------------------------------------
    # 1. Check explicitly listed skills
    # -------------------------------------------------

    cv_skills = [
        skill.lower().strip()
        for skill in cv_data.get("skills", [])
    ]

    for skill in cv_skills:

        # Patterns where the skill itself is being described
        # as missing or unsupported.
        patterns = [
            rf"missing(?: [a-z]+){{0,6}} {re.escape(skill)}",
            rf"lacks(?: [a-z]+){{0,6}} {re.escape(skill)}",
            rf"does not have(?: [a-z]+){{0,6}} {re.escape(skill)}",
            rf"no experience(?: [a-z]+){{0,6}} {re.escape(skill)}",
            rf"{re.escape(skill)}(?: [a-z]+){{0,6}} is not evidenced",
            rf"{re.escape(skill)}(?: [a-z]+){{0,6}} is not mentioned",
            rf"{re.escape(skill)}(?: [a-z]+){{0,6}} is unsupported",
        ]

        for pattern in patterns:

            if re.search(pattern, summary):

                raise ValueError(
                    f"Grounding error: '{skill}' is explicitly "
                    f"present in the CV, but the summary claims "
                    f"it is missing or unsupported."
                )

    # -------------------------------------------------
    # 2. Check Computer Science education
    # -------------------------------------------------

    education = cv_data.get("education", "").lower()

    if "computer science" in education:

        education_patterns = [
            r"computer science(?: [a-z]+){0,6} is not evidenced",
            r"computer science(?: [a-z]+){0,6} is not mentioned",
            r"computer science(?: [a-z]+){0,6} is unsupported",
            r"missing(?: [a-z]+){0,6} computer science",
            r"does not have(?: [a-z]+){0,6} computer science",
            r"lacks(?: [a-z]+){0,6} computer science"
        ]

        for pattern in education_patterns:

            if re.search(pattern, summary):

                raise ValueError(
                    "Grounding error: Computer Science education "
                    "is explicitly present in the CV, but the "
                    "summary claims it is missing or unsupported."
                )

    return True