from eclipse_competitor.EclipseBattlePolicy import MinimaxDepthLimited
from eclipse_competitor.EclipseTeamSelectionPolicy import StrategicTeamSelectionPolicy

from vgc.behaviour import BattlePolicy, TeamSelectionPolicy, TeamBuildPolicy

# from vgc.behaviour.BattlePolicies import Minimax
from vgc.behaviour.BattlePolicies import RandomPlayer
from vgc.behaviour.TeamBuildPolicies import PredictorMLP
from vgc.behaviour.TeamSelectionPolicies import (
    RandomTeamSelectionPolicy,
)
from vgc.competition.Competitor import Competitor


# from .EclipseBattlePolicy import EclipseBattlePolicy


class EclipseCompetitor(Competitor):

    def __init__(self, name: str = "EclipseCompetitor"):
        self._name = name
        self._battle_policy = MinimaxDepthLimited()
        self._team_build_policy = PredictorMLP()  # pre existing policy
        # self._team_selection_policy = RandomTeamSelectionPolicy()
        self._team_selection_policy = StrategicTeamSelectionPolicy()

    @property
    def name(self):
        return self._name

    @property
    def team_build_policy(self) -> TeamBuildPolicy:
        return self._team_build_policy

    @property
    def team_selection_policy(self) -> TeamSelectionPolicy:
        return self._team_selection_policy

    @property
    def battle_policy(self) -> BattlePolicy:
        return self._battle_policy
