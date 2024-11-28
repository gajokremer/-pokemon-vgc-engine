from typing import List


from vgc.balance.meta import MetaData
from vgc.behaviour import TeamBuildPolicy
from vgc.datatypes.Objects import Pkm, PkmTemplate, PkmFullTeam, PkmRoster, PkmTeam
from vgc.engine.PkmBattleEnv import PkmBattleEnv


class FixedTeamBuilder(TeamBuildPolicy):
    """
    Agent that always selects the same team.
    """

    def __init__(self):
        self.roster = None

    def set_roster(self, roster: PkmRoster, ver: int = 0):
        self.roster = roster

    def get_action(self, meta: MetaData) -> PkmFullTeam:
        pre_selection: List[PkmTemplate] = self.roster[0:3]
        team: List[Pkm] = []
        for pt in pre_selection:
            team.append(pt.gen_pkm([0, 1, 2, 3]))
        return PkmFullTeam(team)


def run_battles(pkm0, pkm1, agent0, agent1, n_battles):
    wins = [0, 0]
    t0 = PkmTeam([pkm0])
    t1 = PkmTeam([pkm1])
    env = PkmBattleEnv(
        (t0, t1), encode=(agent0.requires_encode(), agent1.requires_encode())
    )
    for _ in range(n_battles):
        s, _ = env.reset()
        t = False
        while not t:
            a0 = agent0.get_action(s[0])
            a1 = agent1.get_action(s[1])
            s, _, t, _, _ = env.step([a0, a1])
        wins[env.winner] += 1
    return wins
