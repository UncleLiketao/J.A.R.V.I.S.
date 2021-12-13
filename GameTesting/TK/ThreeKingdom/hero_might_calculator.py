import pandas as pd

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


class HeroMightModel(object):
    def __init__(self, hero_id, hero_lv, hero_troop_capacity, hero_anger_skill_lv):
        self.hero_id = hero_id
        self.hero_lv = hero_lv
        self.hero_troop_capacity = hero_troop_capacity
        self.hero_anger_skill_lv = hero_anger_skill_lv
        self.might_param = \
            game_param_data.loc[(game_param_data['类型'] == 12) & (game_param_data['类型定义'] == 19)]['参数'].values[0] / 1000

    """
    战力计算公式：（表订属性战力之和+各BUFF属性战力累加之和+各技能战力之和）*（武将带兵量）^参数
    """

    def cal_hero_might(self):
        hero_might = (self.cal_hero_skill_might() + self.cal_hero_and_troop_three_dimensional()) * pow(
            self.hero_troop_capacity, self.might_param)
        return hero_might

    """
    技能战力：读取skill_group表中power字段读取
    总技能战力=主动技能战力+被动技能战力
    """

    def cal_hero_anger_skill_might(self):
        anger_skill_id = int(hero_data.loc[hero_data['英雄id'] == self.hero_id]['怒气技能'].values[0])
        anger_skill_might = int(
            skills_group_data.loc[
                (skills_group_data['id'] == anger_skill_id) & (skills_group_data['等级'] == self.hero_anger_skill_lv)][
                '战力'].values[0])
        return anger_skill_might

    def cal_hero_passive_skill_might(self):
        passive_skill_list = hero_data.loc[hero_data['英雄id'] == self.hero_id]['被动技能'].values[0].split('|')
        total_passsive_skills_might = 0
        for i in passive_skill_list:
            total_passsive_skills_might += skills_group_data.loc[skills_group_data['id'] == int(i)]['战力'].values[0]
        return total_passsive_skills_might

    def cal_hero_skill_might(self):
        anger_skill_might = self.cal_hero_anger_skill_might()
        total_passsive_skills_might = self.cal_hero_passive_skill_might()
        total_hero_skill_might = anger_skill_might + total_passsive_skills_might
        return total_hero_skill_might

    """
    表订属性战力：
    (1)hero表中配置武将基础的属性三围（power、defense、life），与提升武将等级所增加属性。（表订属性武力*武将武力系数+表订属性智力*武将智力系数+表订属性统率*武将统率系数）等于单武将表订战力。
    (2)troop表中配置士兵基础的三围属性（attack、defense、hp）字段表示士兵攻击、防御、血量。（表订士兵攻击*士兵攻击系数+表订士兵防御*士兵防御系数+表订血量*士兵血量系数）
    game_param表中类型12，值为18，配置格式为（武将战力系数 | 武将智力系数 |武将统率系数 | 士兵攻击系数 |士兵防御系数 |士兵血量系数）
    """

    def cal_hero_one_dimensional(self, hero_attr_type, hero_attr_param_index):
        hero_one_dimensional_init_might = int(
            hero_data.loc[hero_data['英雄id'] == self.hero_id][hero_attr_type].values[0].split('|')[0]) / 1000 + \
                                          int(hero_data.loc[hero_data['英雄id'] == self.hero_id][hero_attr_type].values[
                                                  0].split('|')[1]) / 1000 * (self.hero_lv - 1)
        hero_one_dimensional_param = int(
            game_param_data.loc[(game_param_data['类型'] == 12) & (game_param_data['类型定义'] == 18)]['参数'].values[0].split(
                '|')[
                hero_attr_param_index]) / 1000
        hero_one_dimensional_fixed_might = hero_one_dimensional_init_might * hero_one_dimensional_param
        return hero_one_dimensional_fixed_might

    def cal_troop_one_dimensional(self, troop_attr_type, troop_attr_param_index):
        troop_id = int(hero_data.loc[hero_data['英雄id'] == self.hero_id]['士兵ID'].values[0])
        troop_one_dimensional_init_might = int(
            troop_data.loc[troop_data['兵种ID'] == troop_id][troop_attr_type].values[0])
        troop_one_dimensional_param = int(
            game_param_data.loc[(game_param_data['类型'] == 12) & (game_param_data['类型定义'] == 18)]['参数'].values[0].split(
                '|')[
                troop_attr_param_index]) / 1000
        troop_one_dimensional_fixed_might = troop_one_dimensional_init_might * troop_one_dimensional_param
        return troop_one_dimensional_fixed_might

    def cal_hero_and_troop_three_dimensional(self):
        total_hero_and_troop_fixed_might = self.cal_hero_one_dimensional("力量", 0) + self.cal_hero_one_dimensional("防护",
                                                                                                                  1) + self.cal_hero_one_dimensional(
            "体质", 2) + self.cal_troop_one_dimensional("攻击", 3) + self.cal_troop_one_dimensional("防御",
                                                                                                4) + self.cal_troop_one_dimensional(
            "血量", 5)
        return total_hero_and_troop_fixed_might

    """
    （A buff增加值*战力系数）+（B BUFF增加值*战力系数）=全部BUFF增加战力
    """

    def cal_buff_might(self, buff_id):
        pass


if __name__ == '__main__':
    # input_hero_id = int(input("请输入武将id："))
    # input_hero_lv = int(input("请输入武将等级："))
    # input_hero_troop_capacity = int(input("请输入武将部队容量："))
    # input_hero_anger_skill_lv = int(input("请输入武将怒气技能等级："))

    hero_data_test = HeroMightModel(1016, 2, 923, 1)
    print("武将ID：%s" % hero_data_test.hero_id)
    print("武将等级：%s" % hero_data_test.hero_lv)
    print("武将部队容量：%s" % hero_data_test.hero_troop_capacity)
    print("武将怒气技等级：%s" % hero_data_test.hero_anger_skill_lv)
    print("战力计算参数：%s" % hero_data_test.might_param)
    print("表订属性战力：%s" % hero_data_test.cal_hero_and_troop_three_dimensional())
    print("各技能战力之和：%s" % hero_data_test.cal_hero_skill_might())
    print("英雄总战力：%s" % hero_data_test.cal_hero_might())
