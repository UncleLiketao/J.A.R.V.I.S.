import numpy as np

class DamageModel(object):
    def __init__(self, base_attack, ext_attack, critical, critical_damage):
        self.base_attack = base_attack
        self.ext_attack = ext_attack
        self.critical = critical
        self.critical_damage = critical_damage

    def calc_damage(self):
        return (self.base_attack+self.ext_attack) * self.critical *(1+self.critical_damage)\
                + (self.base_attack+self.ext_attack)*(1-self.critical)

if __name__=='__main__':
    pass