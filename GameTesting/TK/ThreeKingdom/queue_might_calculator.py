import pandas as pd
from collections import Counter
from hero_might_calculator import HeroMightModel

"""
使用的配置表路径
"""
game_param_path = 'D:\\designer_config\\game_param.xlsx'
hero_path = 'D:\\designer_config\\hero.xlsx'
troop_path = 'D:\\designer_config\\troop.xlsx'
skills_group_path = 'D:\\designer_config\\skills_group.xlsx'
buff_type_path = 'D:\\designer_config\\buff_type.xlsx'
buff_path = 'D:\\designer_config\\buff.xlsx'

hero_data = pd.DataFrame(pd.read_excel(hero_path))
game_param_data = pd.DataFrame(pd.read_excel(game_param_path))
troop_data = pd.DataFrame(pd.read_excel(troop_path))
skills_group_data = pd.DataFrame(pd.read_excel(skills_group_path))
buff_type_data = pd.DataFrame(pd.read_excel(buff_type_path))
buff_data = pd.DataFrame(pd.read_excel(buff_path))


class QueueMightModel(HeroMightModel):
    def __init__(self, hero_id, hero_lv, hero_troop_capacity, hero_anger_skill_lv, lvg_id=None, lvg_anger_skill_lv=None,
                 rvg_id=None,
                 rvg_anger_skill_lv=None, ldg_id=None, rdg_id=None):
        super(QueueMightModel, self).__init__(hero_id, hero_lv, hero_troop_capacity, hero_anger_skill_lv)
        self.lvg_id = lvg_id
        self.lvg_anger_skill_lv = lvg_anger_skill_lv
        self.rvg_id = rvg_id
        self.rvg_anger_skill_lv = rvg_anger_skill_lv
        self.ldg_id = ldg_id
        self.rdg_id = rdg_id

    """
    1.计算公式：（表订属性+技能战力+BUFF战力）*（队伍当前配兵量）^参数
    """

    def cal_queue_might(self):
        queue_might = (self.cal_queue_skill_might() + self.cal_hero_and_troop_three_dimensional()) * pow(
            self.hero_troop_capacity, self.might_param)
        return queue_might

    """
    2.技能类型：主动技能、被动技能。
    1)主动技能：主将、副将的主动技能增加队伍战力。
    2)被动技能：主将、副将、偏将的被动技能增加队伍战力。
    """

    def cal_queue_skill_might(self):
        queue_skill_might = self.queue_anger_skill_might() + self.queue_passive_skill_might()
        return queue_skill_might

    def cal_single_hero_skill_might(self, general_id, general_anger_skill_lv):
        if general_id is not None:
            anger_skill_id = int(hero_data.loc[hero_data['英雄id'] == general_id]['怒气技能'].values[0])
            anger_skill_might = int(
                skills_group_data.loc[
                    (skills_group_data['id'] == anger_skill_id) & (skills_group_data['等级'] == general_anger_skill_lv)][
                    '战力'].values[0])
            return anger_skill_might
        else:
            return 0

    def queue_anger_skill_might(self):
        queue_anger_skill_might = self.cal_single_hero_skill_might(self.hero_id, self.hero_anger_skill_lv) + \
                                  self.cal_single_hero_skill_might(self.lvg_id, self.lvg_anger_skill_lv) + \
                                  self.cal_single_hero_skill_might(self.rvg_id, self.rvg_anger_skill_lv)
        return queue_anger_skill_might

    def passive_skill_list(self, general_id):
        if general_id is not None:
            passive_skill_list = hero_data.loc[hero_data['英雄id'] == general_id]['被动技能'].values[0].split('|')
            return passive_skill_list
        else:
            return []

    def queue_passive_skill_might(self):
        queue_passive_skill_list = self.passive_skill_list(self.hero_id) + self.passive_skill_list(
            self.lvg_id) + self.passive_skill_list(self.rvg_id) + self.passive_skill_list(
            self.ldg_id) + self.passive_skill_list(self.rdg_id)
        queue_passive_skill_dict = dict(Counter(queue_passive_skill_list))
        queue_passive_skill_might = 0
        for k in queue_passive_skill_dict:
            queue_passive_skill_might += skills_group_data.loc[
                (skills_group_data['id'] == int(k)) & (skills_group_data['等级'] == queue_passive_skill_dict[k])][
                '战力'].values[0]
        return queue_passive_skill_might

    def cal_queue_passive_skill_dict(self):
        queue_passive_skill_list = self.passive_skill_list(self.hero_id) + self.passive_skill_list(
            self.lvg_id) + self.passive_skill_list(self.rvg_id) + self.passive_skill_list(
            self.ldg_id) + self.passive_skill_list(self.rdg_id)
        queue_passive_skill_dict = dict(Counter(queue_passive_skill_list))
        return queue_passive_skill_dict

    """
    1.基础规则：需判断BUFF来源，只有规划内的来源才增加战力。
    2.Buff来源：武将养成（升阶、升星）、器械养成、科技系统、军团科技。
    3.计算规则：（A buff增加值*战力系数）+（B BUFF增加值*战力系数）=全部BUFF增加战
    """


if __name__ == '__main__':
    queue_test_data = QueueMightModel(1016, 6, 988, 1, None, None, None, None, None, None)
    print("主将ID：%s" % queue_test_data.hero_id)
    print("主将等级：%s" % queue_test_data.hero_lv)
    print("表订属性：%s" % queue_test_data.cal_hero_and_troop_three_dimensional())
    print("主将怒气技等级：%s" % queue_test_data.hero_anger_skill_lv)
    print("队伍带兵数量：%s" % queue_test_data.hero_troop_capacity)
    print("战力参数：%s" % queue_test_data.might_param)
    print("左副将ID：%s" % queue_test_data.lvg_id)
    print("左副将怒气技等级：%s" % queue_test_data.lvg_anger_skill_lv)
    print("右副将ID：%s" % queue_test_data.rvg_id)
    print("右副将怒气技等级：%s" % queue_test_data.rvg_anger_skill_lv)
    print("左偏将ID：%s" % queue_test_data.ldg_id)
    print("右偏将ID：%s" % queue_test_data.rdg_id)
    print("队伍技能战力：%s" % queue_test_data.cal_queue_skill_might())
    print("部队战力：%s" % queue_test_data.cal_queue_might())
