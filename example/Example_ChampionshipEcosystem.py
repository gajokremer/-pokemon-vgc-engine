from Example_Competitor import ExampleCompetitor

from eclipse_competitor.EclipseCompetitor import EclipseCompetitor

from vgc.balance.meta import StandardMetaData
from vgc.competition.Competitor import CompetitorManager
from vgc.ecosystem.ChampionshipEcosystem import ChampionshipEcosystem
from vgc.util.generator.PkmRosterGenerators import RandomPkmRosterGenerator


# N_PLAYERS = 16
N_PLAYERS = 2


def example_vs_eclipse(ce: ChampionshipEcosystem):
    c1 = CompetitorManager(ExampleCompetitor("Example Player 1"))
    c2 = CompetitorManager(EclipseCompetitor("Eclipse Player 2"))
    ce.register(c1)
    ce.register(c2)


def main():
    generator = RandomPkmRosterGenerator()
    roster = generator.gen_roster()
    move_roster = generator.base_move_roster
    meta_data = StandardMetaData()
    meta_data.set_moves_and_pkm(roster, move_roster)
    ce = ChampionshipEcosystem(roster, meta_data, debug=True)
    # for i in range(N_PLAYERS):
    #     cm = CompetitorManager(ExampleCompetitor("Player %d" % i))
    #     ce.register(cm)

    for i in range(N_PLAYERS):
        cm = CompetitorManager(EclipseCompetitor("Player %d" % i))
        ce.register(cm)

    # example_vs_eclipse(ce)
    ce.run(n_epochs=10, n_league_epochs=10)  # 10 epochs, 10 league epochs


if __name__ == "__main__":
    main()
