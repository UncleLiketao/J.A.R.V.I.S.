import pandas as pd

troop_config_path = 'D:\\designer_config\\troop.xlsx'
buff_510_path = ''
buff_511_path = ''
buff_500_path = ''
buff

troop_base_data = pd.DataFrame(pd.read_excel(troop_config_path))
base_attribute = int(troop_base_data.loc[troop_base_data['兵种ID']==0]['攻击'].values)
print(base_attribute)


class DamageModel(object):
    def __init__(self, base_attribute, all_troops_buff, special_troop_buff, all_troop_bonus, special_troop_bonus,
                 territory_bonus, commander_bonus):
        self.base_attribute = base_attribute
        self.all_troops_buff = all_troops_buff
        self.special_troop_buff = special_troop_buff
        self.all_troop_bonus = all_troop_bonus
        self.special_troop_bonus = special_troop_bonus
        self.territory_bonus = territory_bonus
        self.commander_bonus = commander_bonus

    def calc_troop_attribute(self):
        return (self.base_attribute + self.all_troops_buff + self.special_troop_buff) * (1 + (self.all_troop_bonus +
                                                                                              self.special_troop_bonus +
                                                                                              self.commander_bonus) / 1000)


if __name__ == '__main__':
    pass
