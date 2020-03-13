# Quick and dirty test tool to set up game state and render it

from apologies.domain import Game, RED, BLUE, YELLOW, GREEN
from apologies.render.board import renderBoard

game = Game(players=4)
game.players[RED].pieces[0].move_to_safe(0)
game.players[BLUE].pieces[2].move_to_square(43)
game.players[GREEN].pieces[1].move_to_home()

renderBoard(game)
