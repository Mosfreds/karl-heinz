
from utils import positions
from game import Game
from operator import itemgetter




class GameStats:
    def __init__(self, game):
        self.game = game
#        self.heros_dists   = [self.shortest_path_dist(self.game.hero.pos, h.pos) for h in self.game.heroes]
#        self.mines_dists   = [self.shortest_path_dist(self.game.hero.pos, m) for m in self.game.mines_locs]
#        self.taverns_dists = [self.shortest_path_dist(self.game.hero.pos, t) for t in self.game.taverns_locs]
        me = self.game.hero
        self.motivations = []

        # motivation is (prio, dist, type of activity, target location, target)
        for foe in self.game.heroes:
            self.motivations.append((self.likelyhood_of_attack(foe), positions.manhattan_dist(me.pos, foe.pos), 'attack', foe.pos, foe))
        for mine_loc in self.game.mines_locs:
            mine_dist = positions.manhattan_dist(me.pos, mine_loc)
            self.motivations.append((self.likelyhood_of_mining(self.game.mines[mine_loc], mine_dist), mine_dist, 'mine', mine_loc , mine_loc))
        for tavern in self.game.taverns_locs:
            self.motivations.append((self.likelyhood_of_drinking(tavern), positions.manhattan_dist(me.pos,tavern), 'drink', tavern, tavern))
        self.motivations.append((0, 0, 'wait', me.pos, str(me.bot_id)))
        self.motivations.sort(key=itemgetter(1)) 
        self.motivations.sort(key=itemgetter(0), reverse=True)


    def likelyhood_of_mining(self, mine_owner, mine_dist):
        me = self.game.hero
        mine_weight = 20
        mine_max = 100/mine_weight
        if mine_owner == str(me.bot_id):
            return 0
        else:
            return mine_weight*(5 - me.mine_count)*(me.life > (20 + mine_dist))

    def likelyhood_of_drinking(self, tavern):
        me = self.game.hero
        return (100-me.life)*(me.gold >= 2) 
    
    def likelyhood_of_attack(self, foe):
        me = self.game.hero
        life_factor = 1
        gold_factor = 1
        mine_factor = 0.1
        distance_factor = 4
        bloodlust_factor = 30
        return bloodlust_factor * sum([ life_factor * (me.life-foe.life)
                     , gold_factor * (foe.gold-me.gold) * (me.gold < foe.gold)
                     , mine_factor * (foe.mine_count-me.mine_count) * (me.mine_count < foe.mine_count)])/(distance_factor * (1+ positions.manhattan_dist(me.pos,foe.pos)))


           
