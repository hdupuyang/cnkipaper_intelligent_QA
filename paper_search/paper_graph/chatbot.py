from .question_classifer import *
from .question_transfer_sql import *
from .sql_answer import *

class chatbot:
    def __init__(self):
        self.classifer=questionClassifier()
        self.sql_transfer=question_transfer_sql()
        self.answer=sql_answer()
    def chat_main(self,question):
        self.a1=self.classifer.classifer_main(question)
        self.a2=self.sql_transfer.transfer_main(self.a1)
        ans=self.answer.ans_main(self.a2)
        return ans


if __name__=='__main__':
    handler = chatbot()
    while 1:
        question = input('用户:')
        answer = handler.chat_main(question)
        for an in answer:
            print(an)
