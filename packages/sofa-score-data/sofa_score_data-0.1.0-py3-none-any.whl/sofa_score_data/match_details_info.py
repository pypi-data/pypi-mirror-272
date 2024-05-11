def get_attendance(match_details) -> int:
    return match_details["content"]["matchFacts"]["infoBox"]["Attendance"]


def get_top_players(match_details) -> dict:
    return match_details["content"]["matchFacts"]["topPlayers"]["homeTopPlayers"][0]
