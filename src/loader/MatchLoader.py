import pandas as pd


class MatchLoader:
    def load_all_matches(self, selected_sport: Sport) -> pd.DataFrame:
        if selected_sport == Sport.FOOTBALL:
            return FootballMatchLoader().load_all_matches()
        elif selected_sport == Sport.TENNIS:
            return TennisMatchLoader().load_all_matches()
        elif selected_sport == Sport.LOL:
            return LOLMatchLoader().load_all_matches()
        elif selected_sport == Sport.BASKETBALL:
            return BasketballMatchLoader().load_all_matches()
        elif selected_sport == Sport.VOLLEY:
            return VolleyMatchLoader().load_all_matches()
        else:
            raise Exception("Sport non supporté")
