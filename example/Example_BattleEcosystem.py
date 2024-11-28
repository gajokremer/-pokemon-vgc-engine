import sys
import os

# Add project_root to Python path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from eclipse_competitor.EclipseCompetitor import EclipseCompetitor

# from Example_Competitor import ExampleCompetitor
from vgc.balance.meta import StandardMetaData
from vgc.competition.Competitor import CompetitorManager
from vgc.ecosystem.BattleEcosystem import BattleEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator
from vgc.util.generator.PkmTeamGenerators import RandomTeamFromRoster

# N_PLAYERS = 16
N_PLAYERS = 2


def main():
    roster = RandomPkmRosterGenerator().gen_roster()
    meta_data = StandardMetaData()
    le = BattleEcosystem(meta_data, debug=True)
    for i in range(N_PLAYERS):
        # cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
        cm = CompetitorManager(EclipseCompetitor())
        cm.team = RandomTeamFromRoster(roster).get_team()
        le.register(cm)
    le.run(10)


if __name__ == "__main__":
    main()
