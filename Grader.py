class Grader():
    def __init__(self):
        self.ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    #takes in the image of a single answer as a numpy array
    def grade_test(self, ans_np, answers_sheet, model):
        num_correct = 0
        current_answer_index = 0
        user_answers = []
        for ans in ans_np:
            prediction = model.predict(ans)
            letter_index = prediction.argmax()
            user_answer = self.ALPHABET[letter_index]

            if(user_answer.upper() == answers_sheet[current_answer_index].upper()):
                num_correct += 1

            user_answers.append(user_answer)
            current_answer_index += 1

        return user_answers, num_correct

    def get_answers(self, ans_np, model):
        answers = []
        for ans in ans_np:
            prediction = model.predict(ans)
            letter_index = prediction.argmax()
            answer = self.ALPHABET[letter_index]
            answers.append(answer)
        return answers
