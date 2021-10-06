import json


def best_player_team(team):
    top_player = {"rating": "0"}
    for player in team:
        if "N/A" not in player["rating"]:
            if float(player["rating"]) > float(top_player["rating"]):
                top_player = player
    return top_player


def ranked_players_on_team(data):
    ranked_players = {}
    for team in data:
        top_players_on_team = []
        top_player = best_player_team(team["players"])
        top_players_on_team.append(top_player)
        top_players_on_team.sort(key=lambda x: x["rating"], reverse=True)
        print(top_players_on_team)
        ranked_players[team["name"]] = top_players_on_team


def best_player_position_rank(team, position):
    top_player = {"rank": "1000th"}
    for player in team:
        if "N/A" not in player["rank"]:
            if player["position"].split(" ")[0] == position:
                player_rank = player["rank"].split(" ")[0]
                top_player_rank = top_player["rank"].split(" ")[0]
                if float(player_rank[:-2]) < float(top_player_rank[:-2]):
                    top_player = player
    return top_player


def ranked_players_at_position_rank(data, teams):
    positions = ["QB", "HB", "FB", "TE", "WR", "T", "G", "C", "CB", "S", "LB", "DI", "ED"]
    ranked_players = {}
    for position in positions:
        top_players_at_position = []
        for team in data:
            if team["name"] in teams:
                top_player = best_player_position_rank(team["players"], position)
                top_player["team"] = team["name"]
                top_players_at_position.append(top_player)
        top_players_at_position.sort(key=lambda x: x["rank"].split(" ")[0], reverse=False)
        print(top_players_at_position)
        ranked_players[position] = top_players_at_position
    return ranked_players


def best_player_position_rating(team, position):
    top_player = {"rating": "0"}
    for player in team:
        if "N/A" not in player["rating"]:
            if player["position"].split(" ")[0] == position:
                if float(player["rating"]) > float(top_player["rating"]):
                    top_player = player
    return top_player


def ranked_players_at_position_rating(data, teams):
    positions = ["QB", "HB", "FB", "TE", "WR", "T", "G", "C", "CB", "S", "LB", "DI", "ED"]
    ranked_players = {}
    for position in positions:
        top_players_at_position = []
        for team in data:
            if team["name"] in teams:
                top_player = best_player_position_rating(team["players"], position)
                top_player["team"] = team["name"]
                top_players_at_position.append(top_player)
        top_players_at_position.sort(key=lambda x: x["rating"], reverse=True)
        print(top_players_at_position)
        ranked_players[position] = top_players_at_position
    return ranked_players


if __name__ == '__main__':
    with open("PFF1633378544.8657935.json") as json_file:
        data = json.load(json_file)
    #ranked_players_at_position_rating(data, ["colts", "texans"])
    #ranked_players_on_team(data)
    ranked_players_at_position_rank(data, ["colts", "texans"])
