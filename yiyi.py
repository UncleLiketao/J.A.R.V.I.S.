# coding=utf-8
import os
import re
import webbrowser
from Utils.yaml_tool import get_yaml_data

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
        if skill_type == 'open_browser':
            webbrowser.open(skill_content)

    def _fuzzy_finder(self, keyword, data):
        """
        模糊查找器
        :param keyword: 关键字
        :param data: 数据
        :return: list
        """
        suggestions = []
        pattern = '.*%s.' % keyword
        regex = re.compile(pattern)
        for item in data:
            match = regex.search(item({'keyword'}))
            if match:
                suggestions.append(item)
        return suggestions

    def _find_anwser(self, question):
        anwser_data = get_yaml_data(yaml_path)
        for k in anwser_data:
            if not question:
                print("没有检测到输出内容")
                break
            elif question in k:
                print("你要找的是不是：{answer_keyword}\nreply:{reply_content}".format(answer_keyword=k,
                                                                                reply_content=anwser_data[k]['reply']))
                self._use_skill(anwser_data[k]['skill_type'], anwser_data[k]['skill_content'])
                break


    def main(self):
        question = self._prologue()
        self._find_anwser(question)


if __name__=='__main__':
    YiYi().main()

