import random
from typing import Set, Tuple

from vgc.behaviour import TeamSelectionPolicy
from vgc.datatypes.Constants import DEFAULT_TEAM_SIZE
from vgc.datatypes.Objects import PkmFullTeam
from vgc.datatypes.Types import PkmType


# class BalancedTeamSelectionPolicy(TeamSelectionPolicy):

#     def __init__(
#         self,
#         teams_size: int = DEFAULT_TEAM_SIZE,
#         selection_size: int = DEFAULT_TEAM_SIZE,
#     ):
#         self.teams_size = teams_size
#         self.selection_size = selection_size

#     def get_action(self, d: Tuple[PkmFullTeam, PkmFullTeam]) -> Set[int]:
#         """
#         Selects a balanced team based on overall stats.
#         :param d: (self, opponent)
#         :return: idx list of selected pokémon
#         """
#         team = d[0].pkm_list
#         # Assuming team is a list of Pokémon objects with a `stats` attribute
#         stats = [(i, sum(p.stats.values())) for i, p in enumerate(team)]
#         stats.sort(key=lambda x: x[1], reverse=True)
#         selected_ids = [i for i, _ in stats[: self.selection_size]]
#         return set(selected_ids)


# class TypeBasedTeamSelectionPolicy(TeamSelectionPolicy):

#     def __init__(
#         self,
#         teams_size: int = DEFAULT_TEAM_SIZE,
#         selection_size: int = DEFAULT_TEAM_SIZE,
#     ):
#         self.teams_size = teams_size
#         self.selection_size = selection_size

#     def get_action(self, d: Tuple[PkmFullTeam, PkmFullTeam]) -> Set[int]:
#         """
#         Selects a team based on type diversity.
#         :param d: (self, opponent)
#         :return: idx list of selected pokémon
#         """
#         team = d[0].pkm_list
#         type_count = {}
#         selected_ids = set()
#         for i, p in enumerate(team):
#             for p_type in p.types:
#                 if p_type not in type_count:
#                     type_count[p_type] = 0
#                 type_count[p_type] += 1
#         sorted_types = sorted(type_count, key=type_count.get)
#         for p_type in sorted_types:
#             for i, p in enumerate(team):
#                 if p_type in p.types and len(selected_ids) < self.selection_size:
#                     selected_ids.add(i)
#         return selected_ids

# class StrategicTeamSelectionPolicy(TeamSelectionPolicy):

#     def __init__(
#         self,
#         teams_size: int = DEFAULT_TEAM_SIZE,
#         selection_size: int = DEFAULT_TEAM_SIZE,
#     ):
#         self.teams_size = teams_size
#         self.selection_size = selection_size

#     def get_action(self, d: Tuple[PkmFullTeam, PkmFullTeam]) -> Set[int]:
#         """
#         Strategic team selection based on opponent's team composition.
#         :param d: (self, opponent)
#         :return: idx list of selected pokémon
#         """
#         my_team = d[0].pkm_list
#         opponent_team = d[1].pkm_list
#         selected_ids = self.strategic_selection(my_team, opponent_team)
#         return set(selected_ids)

#     def strategic_selection(self, my_team, opponent_team):
#         # Example logic: Prioritize type advantages and balance the team
#         type_advantages = self.calculate_type_advantages(my_team, opponent_team)
#         selected_ids = sorted(
#             range(len(my_team)), key=lambda i: type_advantages[i], reverse=True
#         )
#         return selected_ids[: self.selection_size]

#     def calculate_type_advantages(self, my_team, opponent_team):
#         # Simplified example: Assign scores based on type advantages
#         scores = [0] * len(my_team)
#         for i, my_pkm in enumerate(my_team):
#             for opponent_pkm in opponent_team:
#                 if self.has_type_advantage(my_pkm, opponent_pkm):
#                     scores[i] += 1
#         return scores

#     def has_type_advantage(self, my_pkm, opponent_pkm):
#         # Example function to determine if my_pkm has a type advantage over opponent_pkm
#         # You can replace this with actual type checking logic
#         return random.choice([True, False])  # Placeholder


class StrategicTeamSelectionPolicy(TeamSelectionPolicy):

    def __init__(
        self,
        teams_size: int = DEFAULT_TEAM_SIZE,
        selection_size: int = DEFAULT_TEAM_SIZE,
    ):
        self.teams_size = teams_size
        self.selection_size = selection_size

    def get_action(self, d: Tuple[PkmFullTeam, PkmFullTeam]) -> Set[int]:
        """
        Strategic team selection based on opponent's team composition.
        :param d: (self, opponent)
        :return: idx list of selected pokémon
        """
        my_team = d[0].pkm_list
        opponent_team = d[1].pkm_list
        selected_ids = self.strategic_selection(my_team, opponent_team)
        return set(selected_ids)

    def strategic_selection(self, my_team, opponent_team):
        # Example logic: Prioritize type advantages and balance the team
        type_advantages = self.calculate_type_advantages(my_team, opponent_team)
        balanced_team_ids = self.balance_team(type_advantages, my_team)
        selected_ids = self.select_top_n(
            type_advantages, balanced_team_ids, self.selection_size
        )
        return selected_ids

    def calculate_type_advantages(self, my_team, opponent_team):
        # Initialize scores for each Pokémon in my_team
        scores = [0] * len(my_team)

        # Compare each Pokémon in my_team with each opponent's Pokémon
        for i, my_pkm in enumerate(my_team):
            for opponent_pkm in opponent_team:
                if self.has_type_advantage(my_pkm, opponent_pkm):
                    scores[i] += 1

        return scores

    def has_type_advantage(self, my_pkm, opponent_pkm):
        # Determine if my_pkm has a type advantage over opponent_pkm
        my_types = my_pkm.types
        opponent_types = opponent_pkm.types

        for my_type in my_types:
            for opponent_type in opponent_types:
                if self.type_advantage_matrix[my_type][opponent_type]:
                    return True

        return False

    def balance_team(self, type_advantages, my_team):
        # Example: Ensure the team is balanced based on type advantages
        avg_advantage = sum(type_advantages) / len(type_advantages)
        balanced_team_ids = [
            i for i, adv in enumerate(type_advantages) if adv >= avg_advantage
        ]
        return balanced_team_ids

    def select_top_n(self, type_advantages, balanced_team_ids, n):
        # Select top n Pokémon based on type advantages and team balance
        sorted_ids = sorted(
            balanced_team_ids, key=lambda i: type_advantages[i], reverse=True
        )
        return sorted_ids[:n]

    type_advantage_matrix = {
        # Add more type advantages as needed
        PkmType.NORMAL: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.FIRE: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: True,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: True,
            PkmType.ICE: True,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: True,
            PkmType.FAIRY: False,
        },
        PkmType.WATER: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: True,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: True,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.ELECTRIC: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: True,
            PkmType.FLYING: True,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.GRASS: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: True,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: True,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: True,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.ICE: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: True,
            PkmType.FLYING: True,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: True,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.FIGHT: {
            PkmType.NORMAL: True,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: True,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: True,
            PkmType.STEEL: True,
            PkmType.FAIRY: False,
        },
        PkmType.POISON: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: True,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: True,
            PkmType.STEEL: False,
            PkmType.FAIRY: True,
        },
        PkmType.GROUND: {
            PkmType.NORMAL: False,
            PkmType.FIRE: True,
            PkmType.WATER: False,
            PkmType.ELECTRIC: True,
            PkmType.GRASS: True,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: True,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: True,
            PkmType.FAIRY: False,
        },
        PkmType.FLYING: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: True,
            PkmType.ICE: True,
            PkmType.FIGHT: True,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.PSYCHIC: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: True,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: True,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.BUG: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.ROCK: {
            PkmType.NORMAL: False,
            PkmType.FIRE: True,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: True,
            PkmType.FLYING: True,
            PkmType.PSYCHIC: False,
            PkmType.BUG: True,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.GHOST: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: True,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.DRAGON: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: True,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: True,
        },
        PkmType.DARK: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: True,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: True,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
        PkmType.STEEL: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: False,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: False,
            PkmType.STEEL: False,
            PkmType.FAIRY: True,
        },
        PkmType.FAIRY: {
            PkmType.NORMAL: False,
            PkmType.FIRE: False,
            PkmType.WATER: False,
            PkmType.ELECTRIC: False,
            PkmType.GRASS: False,
            PkmType.ICE: False,
            PkmType.FIGHT: True,
            PkmType.POISON: False,
            PkmType.GROUND: False,
            PkmType.FLYING: False,
            PkmType.PSYCHIC: False,
            PkmType.BUG: False,
            PkmType.ROCK: False,
            PkmType.GHOST: False,
            PkmType.DRAGON: False,
            PkmType.DARK: True,
            PkmType.STEEL: False,
            PkmType.FAIRY: False,
        },
    }
