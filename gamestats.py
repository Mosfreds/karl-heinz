
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
        for foe in self.game.heroes:
            self.motivations.append((self.likelyhood_of_attack(foe), 'attack', foe.pos, foe))
        for mine in self.game.mines:
            self.motivations.append((self.likelyhood_of_mining(mine), 'mine', (0,0) , mine))
        for tavern in self.game.taverns_locs:
            self.motivations.append((self.likelyhood_of_drinking(tavern), 'drink', tavern))
        sorted(self.motivations, key=itemgetter(1))

    def likelyhood_of_mining(self, mine):
        me = self.game.hero
        if mine in me.mines:
            return 0
        else:
            return 5 - me.mine_count

    def likelyhood_of_drinking(self, tavern):
        me = self.game.hero
        return 100-me.life
    
    def likelyhood_of_attack(self, foe):
        me = self.game.hero
        life_factor = 1
        gold_factor = -1
        mine_factor = -1
        return sum([ life_factor * (me.life-foe.life)
                     , gold_factor * (me.gold-foe.gold)
                     , mine_factor * (me.mine_count-foe.mine_count)])


           
