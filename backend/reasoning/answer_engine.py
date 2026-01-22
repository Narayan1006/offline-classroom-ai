from .topic_gates import is_question_allowed, load_concepts
import subprocess

# Local offline LLM via Ollama
# Model already installed on system
OLLAMA_MODEL = "phi3"


def ask_llm(prompt: str) -> str:
    """
    Sends prompt to local Ollama LLM (Phi-3).
    Always returns safe text. Never crashes.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",   # Windows-safe
            errors="ignore",    # Prevent Unicode crash
            timeout=120
        )

        output = result.stdout.strip()

        if output:
            return output
        else:
            return (
                "I understand this topic, but I cannot explain it clearly right now."
            )

    except FileNotFoundError:
        return (
            "The AI teacher is not available on this computer right now."
        )

    except subprocess.TimeoutExpired:
        return (
            "I am thinking a bit slowly. Please try again."
        )

    except Exception:
        return (
            "Something went wrong, but you are doing great. Try again!"
        )


def answer_question(question: str) -> str:
    """
    Main entry point for answering student questions.
    Applies safety, clarity checks, and topic gating
    before calling the LLM.
    """

    question = question.strip()

    # 🔒 CHILD SAFETY: very short / unclear questions
    if len(question.split()) < 2:
        return (
            "Can you please ask your question in a little more detail? 😊"
        )

    concepts = load_concepts(
        "backend/data/lessons/lecture_structured.json"
    )

    allowed, concept = is_question_allowed(question, concepts)

    if not allowed:
        return (
            "This question is not from today’s lesson. "
            "Please ask something related to the topic we studied."
        )

    # 🎓 CHILD-FRIENDLY, GROUNDED PROMPT
    prompt = f"""
You are a kind school teacher helping a child understand today's lesson.

This topic was explained in class.

Topic name:
{concept["name"]}

Important rules:
- Explain ONLY what was taught in class
- Use very simple words
- Use short sentences
- Do NOT guess meanings
- Do NOT introduce new ideas
- Do NOT use advanced or technical terms
- No emojis

If the question is unclear, say:
"Can you please ask the question in a little more detail?"

Student question:
{question}
"""

    return ask_llm(prompt)
