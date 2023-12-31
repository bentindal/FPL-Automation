import numpy as np
import pandas as pd
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor

class fpl_data:
    def __init__(self, data_location, season):
        """
        Initialize the fpl_data class.

        Args:
            data_location (str): The location of the data.
            season (str): The season of the data.
        """
        self.data_location = f'{data_location}'
        self.season = season
        self.prev_season = f'{int(season[:4])-1}-{int(season[5:])-1}'
        self.player_list = self.get_player_list(season)
        self.team_list = self.get_team_list(season)
        self.id_to_name = self.id_to_name_dict()

    def get_player_list(self, season):
        """
        Retrieve the player list for a given season.

        Args:
            season (str): The season of the data.

        Returns:
            dict: The player list for the specified season.
        """
        player_list = pd.read_csv(f'{self.data_location}/{season}/cleaned_players.csv')
        # Merge first_name and second_name columns into one column
        player_list['name'] = player_list['first_name'] + ' ' + player_list['second_name']
        player_list = player_list[['name', 'element_type']]
        player_list = player_list.set_index('name')
        player_list = player_list.rename(columns={'element_type': 'position'})
        # Convert to dictionary
        player_dict = player_list.to_dict(orient='dict')['position']
        return player_dict
    
    def get_team_list(self, season):
        """
        Retrieve the team list for a given season.

        Args:
            season (str): The season of the data.

        Returns:
            pandas.DataFrame: The team list for the specified season.
        """
        team_list = pd.read_csv(f'{self.data_location}/{season}/teams.csv')
        team_list = team_list[['name', 'strength_attack_home', 'strength_attack_away', 'strength_defence_home', 'strength_defence_away']]
        return team_list.set_index('name')
    
    def get_gw_data(self, season, week_num):
        """
        Retrieve the game week data for a given season and week.

        Args:
            season (str): The season of the data.
            week_num (int): The week number of the data.

        Returns:
            pandas.DataFrame: The game week data for the specified season and week.
        """
        if week_num < 1:
            gw_data = pd.read_csv(f'{self.data_location}/{self.prev_season}/gws/gw{38 + week_num}.csv')
        else:
            gw_data = pd.read_csv(f'{self.data_location}/{season}/gws/gw{week_num}.csv')
        gw_data = gw_data[['name', 'position', 'team', 'assists', 'bps', 'clean_sheets', 'creativity', 'goals_conceded', 'goals_scored', 'ict_index', 'influence', 'minutes', 'own_goals', 'penalties_missed', 'penalties_saved', 'red_cards', 'saves', 'threat', 'total_points', 'yellow_cards', 'selected', 'was_home', 'value']]
        return gw_data.set_index('name')

    def get_pos_data(self, season, week_num, position):
        """
        Retrieve player data for a specific position in a given season and week.

        Args:
            season (str): The season of the data.
            week_num (int): The week number of the data.
            position (str): The position of the players to retrieve.

        Returns:
            pandas.DataFrame: Player data for the specified position in the given season and week.
        """
        gw_data = self.get_gw_data(season, week_num)
        gw_data = gw_data[gw_data['position'] == position]
        # Append team data to player data
        gw_data = gw_data.join(self.team_list, on='team')
        # I'd also like to add the total points column from the previous weeks data to this
        
        # Drop rows with NaN values
        gw_data = gw_data.dropna()
        gw_data = gw_data.drop(['position', 'team', 'ict_index'], axis=1)
        return gw_data
    
    def get_all_pos_data(self, season, week_num):
        """
        Retrieve player data for all positions in a given season and week.

        Args:
            season (str): The season of the data.
            week_num (int): The week number of the data.

        Returns:
            tuple: Player data for all positions in the given season and week.
        """
        gk_data = self.get_pos_data(season, week_num, 'GK')
        def_data = self.get_pos_data(season, week_num, 'DEF')
        mid_data = self.get_pos_data(season, week_num, 'MID')
        fwd_data = self.get_pos_data(season, week_num, 'FWD')
        return gk_data, def_data, mid_data, fwd_data
    
    def sum_player_data(self, season, from_gw, to_gw):
        """
        Summarize player data for a given season and range of game weeks.

        Args:
            season (str): The season of the data.
            from_gw (int): The starting game week.
            to_gw (int): The ending game week.

        Returns:
            tuple: Summarized player data for each position.
        """
        if self.season == '2022-23' and from_gw == 7:
            from_gw = 8

        gk_data = self.get_pos_data(season, from_gw, 'GK')
        def_data = self.get_pos_data(season, from_gw, 'DEF')
        mid_data = self.get_pos_data(season, from_gw, 'MID')
        fwd_data = self.get_pos_data(season, from_gw, 'FWD')

        for i in range(from_gw + 1, to_gw + 1):
            if self.season == '2022-23' and i == 7:
                continue
            gk_data = pd.concat((gk_data, self.get_pos_data(season, i, 'GK')))
            def_data = pd.concat((def_data, self.get_pos_data(season, i, 'DEF')))
            mid_data = pd.concat((mid_data, self.get_pos_data(season, i, 'MID')))
            fwd_data = pd.concat((fwd_data, self.get_pos_data(season, i, 'FWD')))

        # Group by player name and calculate the average
        gk_data = gk_data.groupby('name').mean().reset_index().set_index('name')
        def_data = def_data.groupby('name').mean().reset_index().set_index('name')
        mid_data = mid_data.groupby('name').mean().reset_index().set_index('name')
        fwd_data = fwd_data.groupby('name').mean().reset_index().set_index('name')

        return gk_data, def_data, mid_data, fwd_data
    
    def prune_features(self, features):
        """
        Remove unnecessary columns from the features.

        Args:
            features (pandas.DataFrame): The features to be pruned.

        Returns:
            pandas.DataFrame: The pruned features.
        """
        # Drop the remaining columns that are not features
        features = features.drop(['total_points', 'bps', 'selected', 'was_home'], axis=1)

        return features
    
    def prune_all_features(self, features):
        """
        Remove unnecessary columns from the features for all positions.

        Args:
            features (tuple): The features for all positions.

        Returns:
            tuple: The pruned features for all positions.
        """
        gk_features, def_features, mid_features, fwd_features = features
        gk_features = self.prune_features(gk_features)
        def_features = self.prune_features(def_features)
        mid_features = self.prune_features(mid_features)
        fwd_features = self.prune_features(fwd_features)
        return (gk_features, def_features, mid_features, fwd_features)
    
    def extract_labels(self, features):
        """
        Extract the labels from the features.

        Args:
            features (pandas.DataFrame): The features.

        Returns:
            pandas.Series: The labels.
        """
        labels = features['total_points']
        return labels
    
    def extract_all_labels(self, features):
        """
        Extract the labels for all positions from the features.

        Args:
            features (tuple): The features for all positions.

        Returns:
            tuple: The labels for all positions.
        """
        gk_features, def_features, mid_features, fwd_features = features
        gk_labels = self.extract_labels(gk_features)
        def_labels = self.extract_labels(def_features)
        mid_labels = self.extract_labels(mid_features)
        fwd_labels = self.extract_labels(fwd_features)
        return (gk_labels, def_labels, mid_labels, fwd_labels)
    
    def get_training_data(self, season, week_num):
        """
        Get the training data for a given season and week.

        Args:
            season (str): The season of the data.
            week_num (int): The week number of the data.

        Returns:
            tuple: The training data for each position.
        """
        features = self.get_all_pos_data(season, week_num)

        feature_labels = self.extract_all_labels(features)

        # Drop the remaining columns that are not features
        features = self.prune_all_features(features)

        # Group features & labels for convenience
        training_gk = (features[0], feature_labels[0])
        training_def = (features[1], feature_labels[1])
        training_mid = (features[2], feature_labels[2])
        training_fwd = (features[3], feature_labels[3])

        return training_gk, training_def, training_mid, training_fwd

    def get_training_data_all(self, season, from_gw, to_gw):
        """
        Get the training data for a given season and range of game weeks.

        Args:
            season (str): The season of the data.
            from_gw (int): The starting game week.
            to_gw (int): The ending game week.

        Returns:
            tuple: The training data and test data for each position.
        """
        for i in range(from_gw, to_gw):
            if i == from_gw:
                if i < 1:
                    training_gk, training_def, training_mid, training_fwd = self.get_training_data(self.prev_season, 37 + i)
                else:
                    training_gk, training_def, training_mid, training_fwd = self.get_training_data(season, i)
            else:
                if i < 1:
                    training_gk_new, training_def_new, training_mid_new, training_fwd_new = self.get_training_data(self.prev_season, 38 + i)
                else:
                    training_gk_new, training_def_new, training_mid_new, training_fwd_new = self.get_training_data(season, i)
                training_gk = (pd.concat((training_gk[0], training_gk_new[0])), pd.concat((training_gk[1], training_gk_new[1])))
                training_def = (pd.concat((training_def[0], training_def_new[0])), pd.concat((training_def[1], training_def_new[1])))
                training_mid = (pd.concat((training_mid[0], training_mid_new[0])), pd.concat((training_mid[1], training_mid_new[1])))
                training_fwd = (pd.concat((training_fwd[0], training_fwd_new[0])), pd.concat((training_fwd[1], training_fwd_new[1])))
            
        gk_features_train, gk_features_test, gk_labels_train, gk_labels_test = train_test_split(training_gk[0], training_gk[1], test_size=0.2, random_state=42)
        def_features_train, def_features_test, def_labels_train, def_labels_test = train_test_split(training_def[0], training_def[1], test_size=0.2, random_state=42)
        mid_features_train, mid_features_test, mid_labels_train, mid_labels_test = train_test_split(training_mid[0], training_mid[1], test_size=0.2, random_state=42)
        fwd_features_train, fwd_features_test, fwd_labels_train, fwd_labels_test = train_test_split(training_fwd[0], training_fwd[1], test_size=0.2, random_state=42)

        training_gk = (gk_features_train, gk_labels_train)
        training_def = (def_features_train, def_labels_train)
        training_mid = (mid_features_train, mid_labels_train)
        training_fwd = (fwd_features_train, fwd_labels_train)

        test_gk = (gk_features_test, gk_labels_test)
        test_def = (def_features_test, def_labels_test)
        test_mid = (mid_features_test, mid_labels_test)
        test_fwd = (fwd_features_test, fwd_labels_test)

        training_data = [training_gk, training_def, training_mid, training_fwd]
        test_data = [test_gk, test_def, test_mid, test_fwd]

        return training_data, test_data

    def get_model(self, model_type, training_data):
        """
        Get the model for a given model type and training data.

        Args:
            model_type (str): The type of model to use.
            training_data (tuple): The training data for each position.

        Returns:
            tuple: The models for each position.
        """
        # Pick a model type
        if model_type == 'linear':
            gk_model = linear_model.LinearRegression()
            def_model = linear_model.LinearRegression()
            mid_model = linear_model.LinearRegression()
            fwd_model = linear_model.LinearRegression()
            
        elif model_type == 'randomforest':
            gk_model = RandomForestRegressor(oob_score = True, n_estimators = 1000, max_features = 5)
            def_model = RandomForestRegressor(oob_score = True, n_estimators = 1000, max_features = 5)
            mid_model = RandomForestRegressor(oob_score = True, n_estimators = 1000, max_features = 5)
            fwd_model = RandomForestRegressor(oob_score = True, n_estimators = 1000, max_features = 5)

        elif model_type == 'gradientboost':
            loss_function = 'squared_error'
            n_est = 50 # keep at 100 whilst in development for speed
            l_rate = 0.2
            max_f = 10
            max_leaf = 20
            gk_model = GradientBoostingRegressor(max_features=max_f, n_estimators=n_est, max_leaf_nodes=max_leaf, learning_rate=l_rate, criterion='squared_error', loss=loss_function, random_state=42)
            def_model = GradientBoostingRegressor(max_features=max_f,n_estimators=n_est, max_leaf_nodes=max_leaf, learning_rate=l_rate, criterion='squared_error', loss=loss_function, random_state=42)
            mid_model = GradientBoostingRegressor(max_features=max_f,n_estimators=n_est, max_leaf_nodes=max_leaf, learning_rate=l_rate, criterion='squared_error', loss=loss_function, random_state=42)
            fwd_model = GradientBoostingRegressor(max_features=max_f,n_estimators=n_est, max_leaf_nodes=max_leaf, learning_rate=l_rate, criterion='squared_error', loss=loss_function, random_state=42)

        # Fit training data to model
        gk_model.fit(training_data[0][0], training_data[0][1])
        def_model.fit(training_data[1][0], training_data[1][1])
        mid_model.fit(training_data[2][0], training_data[2][1])
        fwd_model.fit(training_data[3][0], training_data[3][1])

        return gk_model, def_model, mid_model, fwd_model
    
    def get_player_predictions(self, season, from_gw, to_gw, models):
        """
        Get the player predictions for a given season, range of game weeks, and models.

        Args:
            season (str): The season of the data.
            from_gw (int): The starting game week.
            to_gw (int): The ending game week.
            models (tuple): The models for each position.

        Returns:
            pandas.DataFrame: The player predictions.
        """
        
        features = self.sum_player_data(season, from_gw, to_gw - 1)
        gk_player_names = features[0].index.values
        def_player_names = features[1].index.values
        mid_player_names = features[2].index.values
        fwd_player_names = features[3].index.values

        player_names = [gk_player_names, def_player_names, mid_player_names, fwd_player_names]

        pruned_features = self.prune_all_features(features)

        gk_predictions = models[0].predict(pruned_features[0])
        def_predictions = models[1].predict(pruned_features[1])
        mid_predictions = models[2].predict(pruned_features[2])
        fwd_predictions = models[3].predict(pruned_features[3])

        # Round predictions
        round_to = 2
        gk_predictions = np.round(gk_predictions, round_to)
        def_predictions = np.round(def_predictions, round_to)
        mid_predictions = np.round(mid_predictions, round_to)
        fwd_predictions = np.round(fwd_predictions, round_to)

        predictions = [gk_predictions, def_predictions, mid_predictions, fwd_predictions]
        return player_names, predictions
    
    def get_price(self, week_num, player):
        gw_data = self.get_gw_data(self.season, week_num)
        gw_data = gw_data[['value']]
        gw_data = gw_data / 10
        # Turn gw_data into dictionary (name --> value)
        gw_data = gw_data.to_dict()['value']
        if player in gw_data:
            return gw_data[player]
        else:
            return None
    
    def actual_points_dict(self, season, week_num):
        gw_data = self.get_gw_data(season, week_num)
        # Name --> Actual Points (Dictionary)
        gw_data = gw_data[['total_points']]
        gw_data = gw_data.to_dict()['total_points']
        return gw_data
    
    def position_dict(self, week_num):
        pos_data = self.get_gw_data(self.season, week_num)
        return pos_data.to_dict()['position']
    
    def get_players_who_didnt_play(self, gameweek):
        gw_data = self.get_gw_data(self.season, gameweek)
        gw_data = gw_data[gw_data['minutes'] == 0]
        # conver to dict (name --> id)
        gw_data = gw_data.to_dict()['minutes']
        return gw_data

    def post_model_weightings(self, predictions):
        # For each pos in predictions
        for pos in predictions:
            # For each player in pos
            for player in pos:
                # Check for injuries
                    # If significant injury, xP = 0

                    # Slight injury, xP *= 0.8
            
                # Check for suspension
                    # If player is suspended, xP = 0
            
            
                # Difficulty of fixture (based on team)
                    # Players Team Rating - Other Teams Rating
                    # If pos, xP *= 1.2
                    # If neg, xP *= 0.8
                
                # Home *= 1.1
                # Away *= 0.9
            
                # Check for form? 
                pass
            # Convert back to [[Player, xP]]
            pass

        return None #[gk_predictions, def_predictions, mid_predictions, fwd_predictions]
    
    def id_to_name_dict(self):
        """
        Get the id to name dictionary.

        Returns:
            dict: The id to name dictionary.
        """
        players = pd.read_csv(f'{self.data_location}/{self.season}/player_idlist.csv')
        # Combine name = first name + last_name
        players['name'] = players['first_name'] + ' ' + players['second_name']

        # Create dict (id --> name)
        id_to_name = players.set_index('id')['name'].to_dict()

        return id_to_name
        