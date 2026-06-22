from dataclasses import dataclass
import collections
from itertools import combinations
from flask import request

#roles_index attacker: att, balancer: bal, supporter: sup
#style_index しっかり者 :ste, 冒険家: adv, 収集家: col, 知的好奇心: inq, 独創性: cre
@dataclass(frozen=True)
class Trekker:
    ID : int
    role : str 
    style : str 

trekkers = [
    Trekker(6, "att", "ste"),
    Trekker(7, "att", "adv"),
    Trekker(3, "att", "adv"),
    Trekker(20, "att", "adv"),
    Trekker(21, "att", "col"),
    Trekker(22, "att", "cre"),
    Trekker(23, "att", "cre"),
    Trekker(5, "att", "inq"),
    Trekker(24, "att", "inq"),
    Trekker(4, "att", "inq"),
    Trekker(2, "att", "inq"),
    Trekker(25, "sup", "ste"),
    Trekker(26, "sup", "ste"),
    Trekker(27, "sup", "adv"),
    Trekker(28, "sup", "col"),
    Trekker(9, "sup", "col"),
    Trekker(29, "sup", "inq"),
    Trekker(14, "bal", "ste"),
    Trekker(13, "bal", "ste"),
    Trekker(12, "bal", "cre"),
    Trekker(30, "bal", "adv"),
    Trekker(31, "bal", "adv"),
    Trekker(32, "bal", "adv"),
    Trekker(10, "bal", "col"),
    Trekker(33, "bal", "col"),
    Trekker(16, "bal", "col"),
    Trekker(15, "bal", "cre"),
    Trekker(34, "bal", "cre"),
    Trekker(17, "bal", "cre"),
    Trekker(35, "bal", "inq"),
    Trekker(18, "bal", "inq"),
    Trekker(19, "bal", "col"),
    Trekker(8, "att", "cre"),
    Trekker(11, "bal", "cre"),
    Trekker(1, "att", "inq"),
]

trekker_names = {
    1: 'Nanoha', 2: 'Gerie', 3: 'Shia', 
    4: 'Chitose', 5: 'Fuyuka', 6: 'Firenze', 
    7: 'Wraith', 8: 'Sparkla', 9: 'Nazuna', 
    10: 'Chixia', 11: 'Freesia', 12: 'Mistique', 
    13: 'Minova', 14: 'Nazuka', 15: 'Snowish Laru', 
    16: 'Springseek Coronis', 17: 'Donna', 18: 'Otoha', 
    19: 'Firefly', 20: 'Laru', 21: 'Amber', 
    22: 'Noya', 23: 'Caramel', 24: 'Shimiao', 
    25: 'Teresa', 26: 'Tilia', 27: 'Ann', 
    28: 'Flora', 29: 'Cosette', 30: 'Canace', 
    31: 'Coronis', 32: 'Kasimira', 33: 'Ridge', 
    34: 'Iris', 35: 'Jinglin'
    }

@dataclass(frozen=True)
class Condition:
    attribute : str #role, style
    value : object #what role/style the condition requires
    minimum : int #the number of mentioned value it needs to fill the requirement

@dataclass
class GroupRequirement:
    name : str
    group_size : int
    conditions : list[Condition] #条件集合

Group_Dorra = GroupRequirement(
    name = "dorra",#ドーラ
    group_size = 3,
    conditions = [Condition("role", "att", 2),Condition("role", "bal", 1), 
                  Condition("style", "adv", 1), Condition("style", "inq", 1)]
)

Group_Guide = GroupRequirement(
    name = "guide",#巡遊者ガイド
    group_size = 3,
    conditions = [Condition("role", "att", 2),Condition("role", "bal", 1), 
                  Condition("style", "adv", 1), Condition("style", "cre", 1)]
)

Group_Disk = GroupRequirement(
    name = "disc",#ロスレコ強化素材
    group_size = 3,
    conditions = [Condition("role","bal", 2), Condition("role", "sup", 1),
                  Condition("style", "col", 1), Condition("style", "adv", 1)]
)

Group_Hat = GroupRequirement(
    name = "hat",#巡遊者突破素材　怪奇ノ霊
    group_size = 3,
    conditions = [Condition("role","att", 2), Condition("role", "sup", 1),
                  Condition("style", "ste", 1), Condition("style", "inq", 1)]
)

Group_Count = GroupRequirement(
    name = "count", #巡遊者突破素材　空壺ノ王
    group_size = 3,
    conditions = [Condition("role","att", 2), Condition("role", "sup", 1),
                  Condition("style", "col", 1), Condition("style", "cre", 1)]
)

Group_Lumen = GroupRequirement(
    name = "lumen", #巡遊者突破素材　癒悦ノ光
    group_size = 3,
    conditions = [Condition("role","bal", 2), Condition("role", "sup", 1),
                  Condition("style", "ste", 1), Condition("style", "cre", 1)]
)

Group_Ghost = GroupRequirement(
    name = "ghost", #ロスレコ突破素材　ラビッシュの残滓
    group_size = 3,
    conditions = [Condition("role","bal", 2), Condition("role", "sup", 1),
                  Condition("style", "ste", 1), Condition("style", "adv", 1)]
)

Group_Fire = GroupRequirement(
    name = "fire", #ロスレコ突破素材　ドボの残滓
    group_size = 3,
    conditions = [Condition("role","att", 2), Condition("role", "sup", 1),
                  Condition("style", "col", 1), Condition("style", "inq", 1)]
)

Group_Light = GroupRequirement(
    name = "light", #ロスレコ突破素材　薄光の残滓
    group_size = 3,
    conditions = [Condition("role","bal", 2), Condition("role", "att", 1),
                  Condition("style", "cre", 1), Condition("style", "inq", 1)]
)

Group_Rhythm = GroupRequirement(
    name = "rhythm", #音楽力セット
    group_size = 3,
    conditions = [Condition("role","att", 2), Condition("role", "bal", 1),
                  Condition("style", "col", 1), Condition("style", "inq", 1)]
)

Group_Barrage  = GroupRequirement(
    name = "barrage", #弾幕力セット
    group_size = 3,
    conditions = [Condition("role","bal", 2), Condition("role", "att", 1),
                  Condition("style", "ste", 1), Condition("style", "cre", 1)]
)

Group_Fight = GroupRequirement(
    name = "fighting", #格闘力セット
    group_size = 3,
    conditions = [Condition("role","sup", 2), Condition("role", "bal", 1),
                  Condition("style", "ste", 1), Condition("style", "inq", 1)]
)

all_commissions = {
    "dorra": Group_Dorra, "guide": Group_Guide, "disk": Group_Disk,
    "hat": Group_Hat, "count": Group_Count, "lumen": Group_Lumen,
    "ghost": Group_Ghost, "fire": Group_Fire, "light": Group_Light,
    "rhythm": Group_Rhythm, "barrage": Group_Barrage, "fight": Group_Fight
}



nonaq_chars = set() #change this later

def check_group(
        group ,
        requirement,
        excluded_ids: set[int] | None = None
):
    if excluded_ids is None:
        excluded_ids = set()
    filtered_group = [char for char in group if char.ID not in excluded_ids]
    if len(filtered_group) != requirement.group_size:
        return False
    for condition in requirement.conditions:
        count = sum(1 for character in filtered_group
                    if getattr(character, condition.attribute) == condition.value)
        if count < condition.minimum:
            return False
    return True

def search (
        Commissions,
        candidates,
        index,
        used_ids,
        selected_groups
):
    if index == len(Commissions):
        return selected_groups
    req = Commissions[index]

    for candidate in candidates[req.name]:
        cand_ids = {Trekker.ID
                    for Trekker in candidate} 
        if used_ids & cand_ids:
            continue
        selected_groups[req.name] = candidate
        result = search(Commissions, candidates, index+1, 
                        used_ids | cand_ids, selected_groups) 
        if result is not None:
            return result
        del selected_groups[req.name]
    return None
