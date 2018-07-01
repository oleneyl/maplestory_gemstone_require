import sys
import json
import random
import math

# Fixed values
with open("core_jemstone.json") as f:
    DATA = json.load(f)

CORE_EXP = 50

ENHANCE_FLAG = 0
SKILL_FLAG = 1
USELESS_FLAG = 2

ENHANCE_PROB = 0.8
SKILL_PROB = 0.16
USELESS_PROB = 0.04

ENHANCE_FRAG = 10
SKILL_FRAG = 40
USELESS_FRAG = 50

ENHANCE_NEED_FRAG = 70
SKILL_NEED_FRAG = 140

ENHANCE_NEED = []
[ENHANCE_NEED.append( (3 * n + 19) * n * 5 // 2 ) for n in range(25)]
SKILL_NEED = []
[SKILL_NEED.append( (n + 21) * n * 5 // 2 ) for n in range(25)]

AIM_MAIN = 50
AIM_SUB = 25
AIM_SKILL = 14

class User():
    def __init__(self, jobname, slot = -1):
        self.job = jobname
        self.frags = 0
        
        self.aim_main = AIM_MAIN
        self.aim_sub = AIM_SUB
        self.aim_skill = AIM_SKILL
        
        #corelist : List of collected cores
        # [0, 1, ... main-1, main, main+1, ... , main + sub -1, ..., total - 1]
        
        self.core_list = []
        self.core_amount = []
        
        self.core_attr = []
        self.core_head = []
        self.skill_list = []
        
        self.total = DATA[self.job]["core_total"]
        self.main = len(DATA[self.job]["main"])
        self.sub = len(DATA[self.job]["sub"])
        
        self.skillneed = 0  #Modify if program applies skill usages
        
        if slot == -1:
            self.slot = self.total
        else:
            self.slot = slot
        
        [self.core_list.append([]) for i in range(self.total)]
        [self.core_amount.append(0) for i in range(self.total)]
        [self.core_head.append([i,-1,-1]) for i in range(self.total)]
        [self.skill_list.append(0) for i in range(self.skillneed)]
        [self.core_attr.append(0) for i in range(self.total)]
        
    def get_core_amount_exp(self, amount):
        return amount * CORE_EXP

    def get_level(self, exp, _type = ENHANCE_FLAG):
        i = 0
        if _type == ENHANCE_FLAG:
            while ENHANCE_NEED[i] < exp:
                i += 1
        elif _type == SKILL_FLAG:
            while SKILL_NEED[i] < exp:
                i += 1
        return i
        
    def get_level_at_core_list(self, index):
        return self.get_level(self.get_core_amount_exp(self.core_amount[index]))
    
    def get_core(self):
        prob = random.random()
        if prob < ENHANCE_PROB:
            core = random.sample(range(self.total),3)
            self.core_list[core[0]].append(core)
            self.core_amount[core[0]] += 1
            
        elif prob < ENHANCE_PROB + SKILL_PROB:
            core = random.randint(0, self.skillneed)
            if self.skillneed == 0:
                self.frags += SKILL_FRAG
            else:
                self.skill_list[core] += CORE_EXP
        else:
            self.frags += USELESS_FRAG
            
    def update_core_head(self):
        attrs = []
        
        #Initialize attraction point
        for i in range(self.main):
            attrs.append(self.aim_main)
        for i in range(self.sub):
            attrs.append(self.aim_sub)
        while len(attrs) != self.total:
            attrs.append(0)
        
        def get_attr(_core):
            retval = 0
            for i in range(3):
                retval += attrs[_core[i]]
            return retval
        
        for i in range(self.total):
            if self.core_amount[i] > 0:
                test_core = self.core_list[i][-1]
                    
                if get_attr(test_core) > get_attr(self.core_head[i]):
                    self.core_head[i] = test_core
            #update attrs
            for k in range(3):
                attrs[self.core_head[i][k]] -= self.get_level_at_core_list(i)
                if attrs[self.core_head[i][k]] < 0:
                    attrs[self.core_head[i][k]] = 0
    
    def get_important_indices(self, _print = False):
        retlist = []
        [retlist.append(i) for i in range(self.total)]

        #Iterate 10 times : be cleverer! But it makes us stupid..
        for repeat in range(10):
            attrs = []
            #Initialize attraction point
            for i in range(self.main):
                attrs.append(self.aim_main)
            for i in range(self.sub):
                attrs.append(self.aim_sub)
            while len(attrs) != self.total:
                attrs.append(0)
            
            def get_attr_from_index(_index):
                retval = 0
                for k in range(3):
                    if _index in retlist:
                        retval += max(attrs[self.core_head[_index][k]] + self.get_level_at_core_list(_index), 0)
                    else:
                        retval += max(attrs[self.core_head[_index][k]], 0)
                return retval
            
            for i in retlist:
                #update attrs
                for k in range(3):
                    attrs[self.core_head[i][k]] -= self.get_level_at_core_list(i)
                        
            index_attrs = {}
            for i in range(self.total):
                index_attrs[i] = get_attr_from_index(i)
            
            retlist = []
            #find picks
            while len(retlist) < self.slot:
                pick = list(index_attrs.keys())[0]
                for i in index_attrs:
                    if index_attrs[pick] < index_attrs[i]:
                        pick = i
                index_attrs.pop(pick)
                retlist.append(pick)
        
        if _print:
            print("---importancy calculation---")
            print("attrs: " + str(attrs))
            print("retlist: " + str(retlist))
            print("----------------------------")
        return retlist
    
    #Calculate lack exp for target index core upgrade                
    def calculate_lack_exp(self, index, lack, flag = ENHANCE_FLAG):
        def exp_from_lvup_at(_lv, _flag):
            if _flag == ENHANCE_FLAG:
                return (40 + 15 * _lv)
            elif _flag == SKILL_FLAG:
                return (50 + 5 * _lv)
                
        lvlist = []        
        for i in range(self.total):
            if index in self.core_head[i]:
                lvlist.append(self.get_level_at_core_list(i))
                
        count = lack
        retexp = 0
        
        while count > 0:
            lvlist.sort()
            retexp += exp_from_lvup_at(lvlist[0], flag)
            lvlist[0] += 1
            count -= 1
            
        return retexp
        
    def judge(self, _print = None):
        lv_list = []
        enhance_list = []
        [enhance_list.append(0) for i in range(self.total)]
        #Initialize attraction point
        for i in range(self.main):
            lv_list.append(self.aim_main)
        for i in range(self.sub):
            lv_list.append(self.aim_sub)
        while len(lv_list) != self.total:
            lv_list.append(0)
        
        imp = self.get_important_indices()
        
        for i in imp:
            if self.core_head[i][1] != -1:
                for k in range(3):
                    lv_list[self.core_head[i][k]] -= self.get_level_at_core_list(i)
                    enhance_list[self.core_head[i][k]] += self.get_level_at_core_list(i)
                    if lv_list[self.core_head[i][k]] < 0:
                        lv_list[self.core_head[i][k]] = 0
        
        needs = 0
        for i in range(self.total):
            need_i = 0
            if lv_list[i] != 0:
                need_i += self.calculate_lack_exp(i, lv_list[i], flag = ENHANCE_FLAG)
            needs += ((need_i - 1) // CORE_EXP + 1) * CORE_EXP
        
        frags_clever = self.frags
        
        #Generate fragments from none - using enhance cores
        for i in range(self.total):
            if i not in imp:
                frags_clever += len(self.core_list[i]) * ENHANCE_FRAG
            
        if _print:
            print("Judegement Status(lack)")
            print(lv_list)
            print("Enhanced Status")
            print(enhance_list)
            print("---Fragment Need------")
            print(needs)
            print("----------------------")
                
        if needs > frags_clever:
            return False
        else:
            return True
            
    def simulate(self, _print = False):
        self.frags = 0
        
        for i in range(self.total):
            self.core_amount[i] = 0
            self.core_list[i] = []
            self.core_attr[i] = 0
            self.core_head[i] = [i, -1, -1]
        
        for i in range(self.skillneed):
            self.skill_list[i] = 0
        
        cores = 0
        while not self.judge():
            self.get_core()
            self.update_core_head()
            cores += 1
            
            if cores % 100 == 0 and _print:
                self.judge(_print = True)
                self.print_status(_print = True)
                print("Cores :" + str(cores))
                print("\n\n")

        if _print:
            print("*** Calculation end ***")
            self.judge(True)
            self.print_status()
            print("Cores : " + str(cores))
        return cores
        
    def print_status(self, _print = False):
        print("<Core Extraction status>")
        imp = self.get_important_indices(_print)
        for i in range(self.total):
            printstr = "At core head" + str(self.core_head[i]) + " : " + str(self.core_amount[i]) + ", Level : " + str(self.get_level_at_core_list(i))
            if i in imp:
                printstr += " <-- selected"
            print(printstr)
        print("fragments:" + str(self.frags) + "\n")

if __name__ == "__main__":
    #name = sys.stdin.readline()
    #user = User(name.split("\n")[0])
    user = User("에반", slot = 8)
    iter_num = 10
    
    sum_ = 0
    sq_sum = 0
    
    for i in range(iter_num):
        core = user.simulate(_print = False)
        sum_ += core
        sq_sum += core * core
    
    print("Job : " + user.job)
    print("Trial : " + str(iter_num))
    print("Average requirement : " + str((sum_ / iter_num)))
    stdev = math.sqrt(sq_sum * iter_num - sum_ * sum_) / iter_num
    print("STDEV : " + str(stdev))
    

    



