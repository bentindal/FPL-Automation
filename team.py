import pandas as pd
import vastaav
class team:
    def __init__(self, season, gameweek):
        self.vastaav_data = vastaav.vastaav_data('data', season)
        self.season = season
        self.gameweek = gameweek
        self.gk = []
        self.defs = []
        self.mids = []
        self.fwds = []
        self.subs = []
        self.gk_xp = pd.read_csv(f'predictions/gw{self.gameweek}_GK.tsv', sep='\t')
        self.def_xp = pd.read_csv(f'predictions/gw{self.gameweek}_DEF.tsv', sep='\t')
        self.mid_xp = pd.read_csv(f'predictions/gw{self.gameweek}_MID.tsv', sep='\t')
        self.fwd_xp = pd.read_csv(f'predictions/gw{self.gameweek}_FWD.tsv', sep='\t')
        self.gk_player_list = dict(zip(self.gk_xp.Name, self.gk_xp.xP))
        self.def_player_list = dict(zip(self.def_xp.Name, self.def_xp.xP))
        self.mid_player_list = dict(zip(self.mid_xp.Name, self.mid_xp.xP))
        self.fwd_player_list = dict(zip(self.fwd_xp.Name, self.fwd_xp.xP))
        self.price_list = self.vastaav_data.price_list(self.gameweek)
        self.gk_xp_dict = dict(zip(self.gk_xp.Name, self.gk_xp.xP))
        self.def_xp_dict = dict(zip(self.def_xp.Name, self.def_xp.xP))
        self.mid_xp_dict = dict(zip(self.mid_xp.Name, self.mid_xp.xP))
        self.fwd_xp_dict = dict(zip(self.fwd_xp.Name, self.fwd_xp.xP))
        self.xp_dict = {**self.gk_xp_dict, **self.def_xp_dict, **self.mid_xp_dict, **self.fwd_xp_dict}
        self.player_list = self.gk_xp.Name.tolist() + self.def_xp.Name.tolist() + self.mid_xp.Name.tolist() + self.fwd_xp.Name.tolist()
        self.captain = ''
        self.vice_captain = ''

    def add_player(self, player, position):
        if position == 'GK':
            if player in self.gk_player_list and len(self.gk) < 2:
                self.gk.append(player)
            else:
                print(f'Player {player} {position} not found or max players reached')

        elif position == 'DEF':
            if player in self.def_player_list and len(self.defs) < 5:
                self.defs.append(player)
            else:
                print(f'Player {player} {position} not found or max players reached')
        elif position == 'MID':
            if player in self.mid_player_list and len(self.mids) < 5:
                self.mids.append(player)
            else:
                print(f'Player {player} {position} not found or max players reached')
        elif position == 'FWD':
            if player in self.fwd_player_list and len(self.fwds) < 3:
                self.fwds.append(player)
            else:
                print(f'Player {player} {position} not found or max players reached')
        else:
            print('Invalid position')
    
    def remove_player(self, player, position):
        if position == 'GK':
            self.gk.remove(player)
        elif position == 'DEF':
            self.defs.remove(player)
        elif position == 'MID':
            self.mids.remove(player)
        elif position == 'FWD':
            self.fwds.remove(player)
        else:
            print('Invalid position')

    def display(self):
        print(f'GW{self.gameweek}:')
        print(f'GK: {self.gk}')
        print(f'DEF: {self.defs}')
        print(f'MID: {self.mids}')
        print(f'FWD: {self.fwds}')
        print(f'SUBS: {self.subs}')
        print(f'C: {self.captain}, VC: {self.vice_captain}')

    def get_team(self):
        return self.gk, self.defs, self.mids, self.fwds
    
    def get_gk(self):
        return self.gk
    
    def get_defs(self):
        return self.defs
    
    def get_mids(self):
        return self.mids
    
    def get_fwds(self):
        return self.fwds
    
    def get_subs(self):
        return self.subs
    
    def suggest_subs(self):
        # Rank each player by their xP, list the lowest xP first
        ranked_gk = []
        for player in self.gk:
            ranked_gk.append([player, self.gk_player_list[player], 'GK'])
        # Sort by xP
        ranked_gk.sort(key=lambda x: float(x[1]))
        ranked_others = []
        for player in self.defs:
            ranked_others.append([player, self.def_player_list[player], 'DEF'])
        for player in self.mids:
            ranked_others.append([player, self.mid_player_list[player], 'MID'])
        for player in self.fwds:
            ranked_others.append([player, self.fwd_player_list[player], 'FWD'])
        ranked_others.sort(key=lambda x: float(x[1]))

        # Suggest subs
        subs = []
        subs.append([ranked_gk[0][0], 'GK'])
        
        # Limit substitution of maximum two players of the same position (except GK)
        positions_substituted = {'GK': 1}
        for player in ranked_others:
            if positions_substituted.get(player[2], 0) < 2 and len(subs) < 4:
                subs.append([player[0], player[2]])
                positions_substituted[player[2]] = positions_substituted.get(player[2], 0) + 1

        return subs

    def make_subs(self, subs):
        # Remove players from team
        for sub in subs:
            self.remove_player(sub[0], sub[1])

        # Add subs to list
        self.subs = subs
    
    def auto_subs(self):
        subs = self.suggest_subs()
        self.make_subs(subs)

    def player_xp(self, player, position):
        if position == 'GK':
            xp_dict = self.gk_xp_dict
        elif position == 'DEF':
            xp_dict = self.def_xp_dict
        elif position == 'MID':
            xp_dict = self.mid_xp_dict
        elif position == 'FWD':
            xp_dict = self.fwd_xp_dict

        # return xP for player
        if player in xp_dict:
            return xp_dict[player]
        else:
            print(f'Player {player} {position} not found')
            return 0
        
    def get_all_xp(self):
        # List of players and their xP
        team_xp = []
        # Get xP for each player in team

        for player in self.gk:
            team_xp.append([player, self.player_xp(player, 'GK')])
        for player in self.defs:
            team_xp.append([player, self.player_xp(player, 'DEF')])
        for player in self.mids:
            team_xp.append([player, self.player_xp(player, 'MID')])
        for player in self.fwds:
            team_xp.append([player, self.player_xp(player, 'FWD')])

        return team_xp
    
    def team_xp(self):
        # Get xP for each player in team
        xp_list = self.get_all_xp()
        total_xp = 0
        for player in xp_list:
            total_xp += player[1]

        return total_xp
    
    def player_value(self, player):
        # Get price for player
        price = self.price_list[player]
        return price
    
    def suggest_captaincy(self):
        # Get xP for each player in team
        xp_list = self.get_all_xp()
        # Sort by xP
        xp_list.sort(key=lambda x: float(x[1]), reverse=True)
        # Suggest captain & Co-captain
        return xp_list[0], xp_list[1]
    
    def update_captain(self, captain, vice_captain):
        self.captain = captain
        self.vice_captain = vice_captain
    
    def auto_captain(self):
        captain, vice_captain = self.suggest_captaincy()
        self.update_captain(captain, vice_captain)
    
    
    