# from pacman import util, search, gamestate

i = float("-inf")
print(i)
i = i**2
print(i)
print(0/2)


x = 0
y = 0
if min(x, y) < -1 or max(x, y) > 1:
    print("boop")
g = [7, 4, 5, 6, 3, 7]

for e, i in enumerate(g):
    s = set(g)
    print(f"e={e} i={i}, {len(g)}, {len(s)}")


"""
#ghost_types = []
    #ghost_moves = []
    #GHOST_MOVES_START = None
    #self.GHOST_MOVES_START = (no_move, no_move, no_move, no_move, no_move, no_move)
    #ghosts = gstate.ghosts
    #for g in ghosts:
    #self.ghost_types.append("R")
    #self.ghost_moves.append(list(self.GHOST_MOVES_START))
    #self.update_ghost_type(gstate)
    
    def update_ghost_type(self, gstate: gamestate.Gamestate):
        old_ghosts = self.previoud_gstate.ghosts
        ghosts = gstate.ghosts
        for index, ghost in enumerate(ghosts):
            move_vector: util.Vector = ghost - old_ghosts[index]
            x = move_vector.x
            y = move_vector.y
            if min(x, y) < -1 or max(x, y) > 1:
                self.ghost_moves[index] = list(self.GHOST_MOVES_START)  # ghost probibly died and moved home
                pass
            else:
                self.ghost_moves[index].pop(0)
                self.ghost_moves[index].append(move_vector)
            old_dis = self.distance_map.get_distance(self.previoud_gstate.pacman, old_ghosts[index])
            new_dis = self.distance_map.get_distance(gstate.pacman, ghost)
            towards_packman = (old_dis - new_dis) <= 0  # sees if ghost no further or getting closer
            different = len(set(self.ghost_moves[index]))  # sees the number of different moves
            if different <= 2:
                if towards_packman:
                    self.ghost_types[index] = "C"
                else:
                    self.ghost_types[index] = "P"
            else:
                self.ghost_types[index] = "R"
        self.previoud_gstate = gstate
"""


"""
C:\Users\dunne\PycharmProjects\ex1\venv\Scripts\python.exe C:/Users/dunne/PycharmProjects/ex1/run.py
Enter command-line arguments: -n 10 -d no contest
(1/10) contestLevel0_1: Pacman emerges victorious! Score: 1253
(1/10) contestLevel0_2: Pacman emerges victorious! Score: 1653
(1/10) contestLevel0_3: Pacman emerges victorious! Score: 1446
(1/10) contestLevel1_1: Pacman emerges victorious! Score: 1779
(1/10) contestLevel1_2: Pacman emerges victorious! Score: 1768
(1/10) contestLevel2_1: Pacman emerges victorious! Score: 3340
(1/10) contestLevel2_2: Pacman emerges victorious! Score: 4441
(1/10) contestLevel2_3: Pacman died! Score: 321
(1/10) contestLevel3_1: Pacman emerges victorious! Score: 5126
(1/10) contestLevel3_2: Pacman died! Score: 2828
(1/10) contestLevel3_3: Pacman died! Score: -378
(1/10) contestLevel3_4: Pacman died! Score: 665
(2/10) contestLevel0_1: Pacman emerges victorious! Score: 1655
(2/10) contestLevel0_2: Pacman emerges victorious! Score: 1652
(2/10) contestLevel0_3: Pacman emerges victorious! Score: 1651
(2/10) contestLevel1_1: Pacman emerges victorious! Score: 1765
(2/10) contestLevel1_2: Pacman died! Score: 726
(2/10) contestLevel2_1: Pacman died! Score: 1488
(2/10) contestLevel2_2: Pacman emerges victorious! Score: 4103
(2/10) contestLevel2_3: Pacman emerges victorious! Score: 4173
(2/10) contestLevel3_1: Pacman died! Score: 2640
(2/10) contestLevel3_2: Pacman emerges victorious! Score: 4221
(2/10) contestLevel3_3: Pacman emerges victorious! Score: 4670
(2/10) contestLevel3_4: Pacman died! Score: 1492
(3/10) contestLevel0_1: Pacman emerges victorious! Score: 1262
(3/10) contestLevel0_2: Pacman emerges victorious! Score: 1464
(3/10) contestLevel0_3: Pacman emerges victorious! Score: 1635
(3/10) contestLevel1_1: Pacman emerges victorious! Score: 1769
(3/10) contestLevel1_2: Pacman emerges victorious! Score: 1763
(3/10) contestLevel2_1: Pacman emerges victorious! Score: 3381
(3/10) contestLevel2_2: Pacman died! Score: 2668
(3/10) contestLevel2_3: Pacman died! Score: 2389
(3/10) contestLevel3_1: Pacman emerges victorious! Score: 4165
(3/10) contestLevel3_2: Pacman emerges victorious! Score: 4341
(3/10) contestLevel3_3: Pacman emerges victorious! Score: 4226
(3/10) contestLevel3_4: Pacman died! Score: 332
(4/10) contestLevel0_1: WARNING: max number of ticks reached (3000) pacman was destroyed, Big oof
Pacman died! Score: -2255
(4/10) contestLevel0_2: Pacman emerges victorious! Score: 1640
(4/10) contestLevel0_3: Pacman emerges victorious! Score: 1656
(4/10) contestLevel1_1: Pacman emerges victorious! Score: 1745
(4/10) contestLevel1_2: Pacman emerges victorious! Score: 1760
(4/10) contestLevel2_1: Pacman emerges victorious! Score: 3341
(4/10) contestLevel2_2: Pacman died! Score: 2218
(4/10) contestLevel2_3: Pacman emerges victorious! Score: 4541
(4/10) contestLevel3_1: Pacman died! Score: 2677
(4/10) contestLevel3_2: Pacman died! Score: 1433
(4/10) contestLevel3_3: Pacman died! Score: 3204
(4/10) contestLevel3_4: Pacman died! Score: 370
(5/10) contestLevel0_1: Pacman emerges victorious! Score: 1663
(5/10) contestLevel0_2: Pacman emerges victorious! Score: 1642
(5/10) contestLevel0_3: Pacman emerges victorious! Score: 1663
(5/10) contestLevel1_1: Pacman emerges victorious! Score: 1763
(5/10) contestLevel1_2: Pacman emerges victorious! Score: 1723
(5/10) contestLevel2_1: Pacman emerges victorious! Score: 2247
(5/10) contestLevel2_2: Pacman emerges victorious! Score: 3952
(5/10) contestLevel2_3: Pacman died! Score: 1095
(5/10) contestLevel3_1: Pacman emerges victorious! Score: 3719
(5/10) contestLevel3_2: Pacman emerges victorious! Score: 4338
(5/10) contestLevel3_3: Pacman died! Score: 3013
(5/10) contestLevel3_4: Pacman died! Score: 2901
(6/10) contestLevel0_1: Pacman emerges victorious! Score: 1454
(6/10) contestLevel0_2: Pacman emerges victorious! Score: 1669
(6/10) contestLevel0_3: Pacman emerges victorious! Score: 1473
(6/10) contestLevel1_1: Pacman emerges victorious! Score: 1749
(6/10) contestLevel1_2: Pacman emerges victorious! Score: 1768
(6/10) contestLevel2_1: Pacman emerges victorious! Score: 2241
(6/10) contestLevel2_2: Pacman emerges victorious! Score: 4300
(6/10) contestLevel2_3: Pacman died! Score: 2750
(6/10) contestLevel3_1: Pacman emerges victorious! Score: 4145
(6/10) contestLevel3_2: Pacman emerges victorious! Score: 4357
(6/10) contestLevel3_3: Pacman died! Score: -362
(6/10) contestLevel3_4: Pacman died! Score: 1231
(7/10) contestLevel0_1: Pacman emerges victorious! Score: 1659
(7/10) contestLevel0_2: Pacman emerges victorious! Score: 1637
(7/10) contestLevel0_3: Pacman emerges victorious! Score: 1643
(7/10) contestLevel1_1: Pacman emerges victorious! Score: 1757
(7/10) contestLevel1_2: Pacman emerges victorious! Score: 1777
(7/10) contestLevel2_1: Pacman died! Score: 1547
(7/10) contestLevel2_2: Pacman died! Score: 2954
(7/10) contestLevel2_3: Pacman died! Score: 1240
(7/10) contestLevel3_1: Pacman emerges victorious! Score: 3755
(7/10) contestLevel3_2: Pacman died! Score: -307
(7/10) contestLevel3_3: Pacman died! Score: 450
(7/10) contestLevel3_4: Pacman emerges victorious! Score: 3443
(8/10) contestLevel0_1: Pacman emerges victorious! Score: 1265
(8/10) contestLevel0_2: Pacman emerges victorious! Score: 1655
(8/10) contestLevel0_3: Pacman emerges victorious! Score: 1622
(8/10) contestLevel1_1: Pacman emerges victorious! Score: 1783
(8/10) contestLevel1_2: Pacman emerges victorious! Score: 1765
(8/10) contestLevel2_1: Pacman emerges victorious! Score: 2443
(8/10) contestLevel2_2: Pacman emerges victorious! Score: 3981
(8/10) contestLevel2_3: Pacman died! Score: 2042
(8/10) contestLevel3_1: Pacman emerges victorious! Score: 3910
(8/10) contestLevel3_2: Pacman died! Score: 2685
(8/10) contestLevel3_3: Pacman emerges victorious! Score: 3908
(8/10) contestLevel3_4: Pacman died! Score: 2943
(9/10) contestLevel0_1: Pacman emerges victorious! Score: 1450
(9/10) contestLevel0_2: Pacman emerges victorious! Score: 1644
(9/10) contestLevel0_3: Pacman emerges victorious! Score: 1451
(9/10) contestLevel1_1: Pacman emerges victorious! Score: 1782
(9/10) contestLevel1_2: Pacman died! Score: 690
(9/10) contestLevel2_1: Pacman emerges victorious! Score: 3570
(9/10) contestLevel2_2: Pacman emerges victorious! Score: 4149
(9/10) contestLevel2_3: Pacman emerges victorious! Score: 4688
(9/10) contestLevel3_1: Pacman emerges victorious! Score: 3964
(9/10) contestLevel3_2: Pacman emerges victorious! Score: 4577
(9/10) contestLevel3_3: Pacman emerges victorious! Score: 4326
(9/10) contestLevel3_4: Pacman died! Score: 1222
(10/10) contestLevel0_1: Pacman emerges victorious! Score: 1244
(10/10) contestLevel0_2: Pacman emerges victorious! Score: 1661
(10/10) contestLevel0_3: Pacman emerges victorious! Score: 1440
(10/10) contestLevel1_1: Pacman emerges victorious! Score: 1773
(10/10) contestLevel1_2: Pacman emerges victorious! Score: 1740
(10/10) contestLevel2_1: Pacman emerges victorious! Score: 2790
(10/10) contestLevel2_2: Pacman emerges victorious! Score: 3749
(10/10) contestLevel2_3: Pacman died! Score: 3554
(10/10) contestLevel3_1: Pacman emerges victorious! Score: 3556
(10/10) contestLevel3_2: Pacman emerges victorious! Score: 4549
(10/10) contestLevel3_3: Pacman died! Score: 2787
(10/10) contestLevel3_4: Pacman died! Score: 1348

Average score: 2316.3166666666666
Wins: 84/120 (70% win rate)

Process finished with exit code 0
"""


def start(self):
    return self.start, 0