import os
from yaml_tool import get_yaml_data

current_path = os.path.abspath(".")
yaml_path = os.path.join(current_path, "answer.yaml")


class YiYi(object):
    def __init__(self):
        self.name = "yiyi"
        self.sex = "male"
        self.birth = "2021年2月21日"

    @staticmethod
    def _prologue():
        print("******你好，我是一一******")
        question = input('请输入想要提问的内容：')
        return question

    def _use_skill(self, skill_type, skill_content):
        pass

    def _find_anwser(self, question):
        anwser_data = get_yaml_data(yaml_path)
        for k in anwser_data:
            print(k)

    def main(self):
        question = self._prologue()
        print(question)


if __name__=='__main__':
    YiYi().main()
