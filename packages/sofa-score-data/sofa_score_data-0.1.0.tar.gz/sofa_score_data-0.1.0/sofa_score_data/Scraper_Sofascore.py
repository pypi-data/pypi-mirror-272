import requests
import pandas as pd


class Sofascore:
    ############################################################################
    def __init__(self):
        self.requests_headers = {
            "authority": "api.sofascore.com",
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "dnt": "1",
            "if-none-match": 'W/"4bebed6144"',
            "origin": "https://www.sofascore.com",
            "referer": "https://www.sofascore.com/",
            "sec-ch-ua": '"Not.A/Brand";v="8", "Chromium";v="114"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 "
            + "Safari/537.36",
        }

    ############################################################################
    def get_match_id(self, match_url):
        """Get match id from a Sofascore match url

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            string: Match id for a SofaScore match. Used in Urls
        """
        # this can also be found in the 'id' key of the dict returned from
        # get_match_data(), if the format of the match url ever changes
        match_id = match_url.split(":")[-1]
        return match_id

    ############################################################################
    def get_player_ids(self, match_url):
        """Get the player ids for a Sofascore match

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            dict: Name and ids of every player in the match
                Key: Name
                Value: Id
        """
        match_id = self.get_match_id(match_url)

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/lineups",
            headers=self.requests_headers,
        )

        teams = ["home", "away"]
        player_ids = {}
        for team in teams:
            data = response.json()[team]["players"]

            for item in data:
                player_data = item["player"]
                player_ids[player_data["name"]] = player_data["id"]

        return player_ids

    ############################################################################
    def get_match_data(self, match_url):
        """Get match general data

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            dict: Generic data about a match
        """

        match_id = self.get_match_id(match_url)

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}", headers=self.requests_headers
        )
        data = response.json()["event"]
        return data

    ############################################################################
    def get_team_names(self, match_url):
        """Get the team names for the home and away teams

        Args:
            match_url (string): Full link to a SofaScore match

        Returns:
            strings: Name of home and away team.
        """

        data = self.get_match_data(match_url)

        home_team = data["homeTeam"]["name"]
        away_team = data["awayTeam"]["name"]

        return home_team, away_team

    def match_momentum(self, match_url):
        """Get the match momentum values

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            fig, ax: Plot of match momentum and fig/axes for further customization
        """
        match_id = self.get_match_id(match_url)
        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/graph",
            headers=self.requests_headers,
        )
        match_momentum_df = pd.DataFrame(response.json()["graphPoints"])

        return match_momentum_df

    ############################################################################
    def get_general_match_stats(self, match_url):
        """Get general match statistics (possession, passes, duels) by teams.

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrame: Each row is a general statistic and the columns show the
                values for home and away Teams.
        """
        match_id = self.get_match_id(match_url)

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/statistics",
            headers=self.requests_headers,
        )

        df = pd.DataFrame()
        for i in range(len(response.json()["statistics"][0]["groups"])):
            df_valores = pd.DataFrame(
                response.json()["statistics"][0]["groups"][i]["statisticsItems"]
            )
            df = pd.concat([df, df_valores])
        df = df[["name", "home", "homeValue", "homeTotal", "away", "awayValue", "awayTotal"]]
        return df

    ############################################################################
    def get_players_match_stats(self, match_url):
        """Returns match data for each player.

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrames: A DataFrame for home and away teams with each row being
                a player and in each columns a different statistic or data of
                the player
        """

        match_id = self.get_match_id(match_url)
        home_name, away_name = self.get_team_names(match_url)

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/lineups",
            headers=self.requests_headers,
        )

        names = {"home": home_name, "away": away_name}
        dataframes = {}
        for team in names.keys():
            data = pd.DataFrame(response.json()[team]["players"])
            columns_list = [
                data["player"].apply(pd.Series),
                data["shirtNumber"],
                data["jerseyNumber"],
                data["position"],
                data["substitute"],
                data["statistics"].apply(pd.Series, dtype=object),
                data["captain"],
            ]
            df = pd.concat(columns_list, axis=1)
            df["team"] = names[team]
            dataframes[team] = df

        return dataframes["home"], dataframes["away"]

    ############################################################################
    def get_players_average_positions(self, match_url):
        """Return player averages positions for each team

        Args:
            match_url (str): Full link to a SofaScore match

        Returns:
            DataFrame: Each row is a player and columns averageX and averageY
                denote their average position on the match.
        """
        match_id = self.get_match_id(match_url)
        home_name, away_name = self.get_team_names(match_url)

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/average-positions",
            headers=self.requests_headers,
        )

        names = {"home": home_name, "away": away_name}
        dataframes = {}
        for team in names.keys():
            data = pd.DataFrame(response.json()[team])
            df = pd.concat([data["player"].apply(pd.Series), data.drop(columns=["player"])], axis=1)
            df["team"] = names[team]
            dataframes[team] = df

        return dataframes["home"], dataframes["away"]

    ############################################################################
    def get_player_heatmap(self, match_url, player):
        """Get the x-y coordinates to create a player heatmap. Use Seaborn's
        `kdeplot()` to create the heatmap image.

        Args:
            match_url (str): Full link to a SofaScore match
            player (str): Name of the player (must be the SofaScore one). Use
                Sofascore.get_player_ids()

        Returns:
            DataFrame: Pandas dataframe with x-y coordinates for the player
        """
        match_id = self.get_match_id(match_url)

        player_ids = self.get_player_ids(match_url)
        player_id = player_ids[player]

        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/player/{player_id}/heatmap",
            headers=self.requests_headers,
        )
        heatmap = pd.DataFrame(response.json()["heatmap"])

        return heatmap

    def get_match_shotmap(self, match_url):
        match_id = self.get_match_id(match_url)
        response = requests.get(
            f"https://api.sofascore.com/api/v1/event/{match_id}/shotmap",
            headers=self.requests_headers,
        )
        return response
