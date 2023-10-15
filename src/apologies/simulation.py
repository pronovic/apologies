# -*- coding: utf-8 -*-
# vim: set ft=python ts=4 sw=4 expandtab:
# pylint: disable=line-too-long:

"""
Run a simulation to see how well different character input sources behave.
"""

from __future__ import annotations  # so we can return a type from one of its own methods

import csv
import statistics
from itertools import combinations_with_replacement
from typing import Dict, List, Optional, Sequence

import pendulum
from attrs import frozen
from pendulum import DateTime  # type: ignore[attr-defined,unused-ignore]

from .engine import Character, Engine
from .game import MAX_PLAYERS, MIN_PLAYERS, GameMode, Player
from .source import CharacterInputSource

BASE_HEADERS = [
    "Scenario",
    "Mode",
    "Iterations",
    "Players",
    "Player 1",
    "Player 2",
    "Player 3",
    "Player 4",
    "Median Turns",
    "Overall Mean Turns",
    "Overall Median Duration (ms)",
    "Overall Mean Duration (ms)",
]

SOURCE_HEADERS = [
    "Median Turns",
    "Mean Turns",
    "Median Duration (ms)",
    "Mean Duration (ms)",
    "Wins",
    "Win %",
]


def _mean(data: Sequence[float]) -> Optional[float]:
    """Calculate the mean rounded to 2 decimal places or return None if there is not any data."""
    return round(statistics.mean(data), 2) if data else None


def _median(data: Sequence[float]) -> Optional[float]:
    """Calculate the median rounded to 2 decimal places or return None if there is not any data."""
    return round(statistics.median(data), 2) if data else None


@frozen
class _Result:

    """Result of a single game within a scenario."""

    start: DateTime
    stop: DateTime
    character: Character
    player: Player


@frozen
class _Statistics:

    """Scenario statistics for a source."""

    source: Optional[str]
    median_turns: Optional[float]
    mean_turns: Optional[float]
    median_duration: Optional[float]
    mean_duration: Optional[float]
    wins: int
    win_percent: float

    @staticmethod
    def for_results(name: Optional[str], results: List[_Result]) -> _Statistics:
        in_scope = [result for result in results if name is None or result.character.source.name == name]
        turns = [result.player.turns for result in in_scope]
        durations_ms = [result.stop.diff(result.start).microseconds / 1000 for result in in_scope]  # type: ignore[no-untyped-call,unused-ignore]
        median_turns = _median(turns)
        mean_turns = _mean(turns)
        median_duration = _median(durations_ms)
        mean_duration = _mean(durations_ms)
        wins = len(in_scope)
        win_percent = 0.0 if len(results) == 0 else round(100.0 * (wins / len(results)), 1)
        return _Statistics(name, median_turns, mean_turns, median_duration, mean_duration, wins, win_percent)


@frozen
class _Analysis:
    """Groups together information analyzed for a scenario."""

    scenario: str
    mode: str
    iterations: int
    players: int
    playernames: List[str]
    overall_stats: _Statistics
    source_stats: Dict[str, _Statistics]


def _analyze_scenario(
    scenario: int,
    mode: GameMode,
    iterations: int,
    players: int,
    sources: Sequence[CharacterInputSource],
    combination: Sequence[CharacterInputSource],
    results: List[_Result],
) -> _Analysis:
    """Analyze a scenario, generating data that can be written to the CSV file."""
    playernames = [source.name for source in combination] + [""] * (MAX_PLAYERS - len(combination))
    overall_stats = _Statistics.for_results(None, results)
    source_stats = {name: _Statistics.for_results(name, results) for name in sorted(list({source.name for source in sources}))}
    return _Analysis("Scenario %d" % scenario, mode.name, iterations, players, playernames, overall_stats, source_stats)


def _write_header(csvwriter, sources: List[CharacterInputSource]) -> None:  # type: ignore
    """Write the header into the CSV file."""
    headers = BASE_HEADERS[:]
    for name in sorted(list({source.name for source in sources})):
        for column in SOURCE_HEADERS:
            headers += ["%s - %s" % (name, column)]
    csvwriter.writerow(headers)


def _write_scenario(csvwriter, analysis: _Analysis) -> None:  # type: ignore
    """Write analysis results for a scenario into the CSV file."""
    row = [analysis.scenario, analysis.mode, analysis.iterations, analysis.players]
    row += analysis.playernames
    row += [
        analysis.overall_stats.median_turns,
        analysis.overall_stats.mean_turns,
        analysis.overall_stats.median_duration,
        analysis.overall_stats.mean_duration,
    ]
    for stats in analysis.source_stats.values():
        row += [stats.median_turns, stats.mean_turns, stats.median_duration, stats.mean_duration, stats.wins, stats.win_percent]
    csvwriter.writerow(row)


def _run_scenario(prefix: str, iterations: int, engine: Engine) -> List[_Result]:
    """Run a particular scenario, playing a game repeatedly for a set number of iterations."""
    results = []
    for i in range(0, iterations):
        print(" " * 100, end="\r", flush=True)
        print("%siteration %d" % (prefix, i), end="\r", flush=True)
        start = pendulum.now()
        engine.reset()
        engine.start_game()
        while not engine.completed:
            engine.play_next()
        stop = pendulum.now()
        character, player = engine.winner()  # type: ignore
        results.append(_Result(start, stop, character, player))
    return results


# pylint: disable=too-many-locals,line-too-long
def run_simulation(iterations: int, output: str, sources: List[CharacterInputSource]) -> None:
    """
    Run a simulation.

    Args:
        iterations(int): The number of iterations (number of times to play the game)
        output(str): Path to the output file to write
        sources(List[CharacterInputSource]): The source to use for each player in the game
    """
    with open(output, "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        _write_header(csvwriter, sources)

        start = pendulum.now()
        print("Starting simulation at %s, using %d iterations per scenario" % (start.to_datetime_string(), iterations))  # type: ignore[no-untyped-call,unused-ignore]

        scenario = 0
        results = []
        for mode in GameMode:
            for players in range(MIN_PLAYERS, MAX_PLAYERS + 1):
                case = 0
                for combination in combinations_with_replacement(sources, players):
                    case += 1
                    scenario += 1
                    prefix = "Scenario %d: %s mode with %d players (case %d): " % (scenario, mode.name, players, case)
                    characters = [Character(name=source.name, source=source) for source in combination]
                    engine = Engine(mode=mode, characters=characters)
                    print(" " * 100, end="\r", flush=True)
                    print("%sstarting" % prefix, end="\r", flush=True)
                    results = _run_scenario(prefix, iterations, engine)
                    print("%sanalyzing" % prefix, end="\r", flush=True)
                    analysis = _analyze_scenario(scenario, mode, iterations, players, sources, combination, results)
                    print("%swriting CSV" % prefix, end="\r", flush=True)
                    _write_scenario(csvwriter, analysis)
                    print("%sdone" % prefix, end="\r", flush=True)

        stop = pendulum.now()
        print(" " * 100, end="\r", flush=True)
        print("Simulation completed after %s at %s" % (stop.diff(start).in_words(), stop.to_datetime_string()))  # type: ignore[no-untyped-call,unused-ignore]
