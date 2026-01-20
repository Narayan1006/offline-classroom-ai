from backend.reasoning.answer_engine import answer_question

while True:
    q = input("Ask a question: ")
    print(answer_question(q))
