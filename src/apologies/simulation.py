# vim: set ft=python ts=4 sw=4 expandtab:
# ruff: noqa: T201

"""
Run a simulation to see how well different character input sources behave.
"""

import csv
import statistics
import typing
from collections.abc import Sequence
from itertools import combinations_with_replacement
from pathlib import Path

from arrow import Arrow
from arrow import now as arrow_now
from attrs import frozen

from apologies.engine import Character, Engine
from apologies.game import MAX_PLAYERS, MIN_PLAYERS, GameMode, Player
from apologies.source import CharacterInputSource
from apologies.util import ISO_TIMESTAMP_FORMAT

if typing.TYPE_CHECKING:
    # noinspection PyUnusedImports
    from _csv import _writer

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


def _mean(data: Sequence[float]) -> float | None:
    """Calculate the mean rounded to 2 decimal places or return None if there is not any data."""
    return round(statistics.mean(data), 2) if data else None


def _median(data: Sequence[float]) -> float | None:
    """Calculate the median rounded to 2 decimal places or return None if there is not any data."""
    return round(statistics.median(data), 2) if data else None


@frozen
class _Result:
    """Result of a single game within a scenario."""

    start: Arrow
    stop: Arrow
    character: Character
    player: Player


@frozen
class _Statistics:
    """Scenario statistics for a source."""

    source: str | None
    median_turns: float | None
    mean_turns: float | None
    median_duration: float | None
    mean_duration: float | None
    wins: int
    win_percent: float

    @staticmethod
    def for_results(name: str | None, results: list[_Result]) -> "_Statistics":
        in_scope = [result for result in results if name is None or result.character.source.name == name]
        turns = [result.player.turns for result in in_scope]
        durations_ms = [(result.stop - result.start).microseconds / 1000 for result in in_scope]
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
    playernames: list[str]
    overall_stats: _Statistics
    source_stats: dict[str, _Statistics]


# pylint: disable=too-many-positional-arguments
def _analyze_scenario(  # noqa: PLR0917,PLR0913
    scenario: int,
    mode: GameMode,
    iterations: int,
    players: int,
    sources: Sequence[CharacterInputSource],
    combination: Sequence[CharacterInputSource],
    results: list[_Result],
) -> _Analysis:
    """Analyze a scenario, generating data that can be written to the CSV file."""
    playernames = [source.name for source in combination] + [""] * (MAX_PLAYERS - len(combination))
    overall_stats = _Statistics.for_results(None, results)
    source_stats = {name: _Statistics.for_results(name, results) for name in sorted({source.name for source in sources})}
    return _Analysis(f"Scenario {scenario}", mode.name, iterations, players, playernames, overall_stats, source_stats)


def _write_header(csvwriter: "_writer", sources: list[CharacterInputSource]) -> None:
    """Write the header into the CSV file."""
    headers = BASE_HEADERS[:]
    for name in sorted({source.name for source in sources}):
        for column in SOURCE_HEADERS:
            headers += [f"{name} - {column}"]
    csvwriter.writerow(headers)


def _write_scenario(csvwriter: "_writer", analysis: _Analysis) -> None:
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


def _run_scenario(prefix: str, iterations: int, engine: Engine) -> list[_Result]:
    """Run a particular scenario, playing a game repeatedly for a set number of iterations."""
    results = []
    for i in range(iterations):
        print(" " * 100, end="\r", flush=True)
        print(f"{prefix}iteration {i}", end="\r", flush=True)
        start = arrow_now()
        engine.reset()
        engine.start_game()
        while not engine.completed:
            engine.play_next()
        stop = arrow_now()
        character, player = engine.winner()
        results.append(_Result(start, stop, character, player))
    return results


# pylint: disable=too-many-locals,line-too-long
def run_simulation(iterations: int, output: str, sources: list[CharacterInputSource]) -> None:
    """
    Run a simulation.

    Args:
        iterations(int): The number of iterations (number of times to play the game)
        output(str): Path to the output file to write
        sources(List[CharacterInputSource]): The source to use for each player in the game
    """
    with Path(output).open("w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        _write_header(csvwriter, sources)

        start = arrow_now()
        print(f"Starting simulation at {start.format(ISO_TIMESTAMP_FORMAT)}, using {iterations} iterations per scenario")

        scenario = 0
        results = []
        for mode in GameMode:
            for players in range(MIN_PLAYERS, MAX_PLAYERS + 1):
                for case, combination in enumerate(combinations_with_replacement(sources, players), start=0):
                    scenario += 1
                    prefix = f"Scenario {scenario}: {mode.name} mode with {players} players (case {case}): "
                    characters = [Character(name=source.name, source=source) for source in combination]
                    engine = Engine(mode=mode, characters=characters)
                    print(" " * 100, end="\r", flush=True)
                    print(f"{prefix}starting", end="\r", flush=True)
                    results = _run_scenario(prefix, iterations, engine)
                    print(f"{prefix}analyzing", end="\r", flush=True)
                    analysis = _analyze_scenario(scenario, mode, iterations, players, sources, combination, results)
                    print(f"{prefix}writing CSV", end="\r", flush=True)
                    _write_scenario(csvwriter, analysis)
                    print(f"{prefix}done", end="\r", flush=True)

        stop = arrow_now()
        print(" " * 100, end="\r", flush=True)
        duration = stop.humanize(start, only_distance=True)
        finished = stop.format(ISO_TIMESTAMP_FORMAT)
        print(f"Simulation completed after {duration} at {finished}")
