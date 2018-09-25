
import My_Othello_Logic

print('FULL')

def get_row()->int:
    rows = int(input('type the number of rows: '))
    return rows
    
def get_column()->int:
    columns = int(input('type the number of columns: '))
    return columns

def first_turn()->str:
    first = input('who goes first?: ')
    return first

def game_mode()->str:
    mode = input('what is the game mode: ')
    return mode

def first_board()->[[str]]:
    first_board = []
    for rows in range(get_row):
        initialize = input('create the first board: ')
        board = initialize.strip('\n').split()
        first_board.append(board)
    return first_board
    

def make_move()-> list:
    move = input('what is the move: ')
    return move.split()


if __name__ == '__main__':
    get_row = get_row()
    get_column = get_column()
    first_turn = first_turn()
    game_mode = game_mode()
    first_board = first_board()
    game_state = My_Othello_Logic.GameState(get_row, get_column, first_turn, game_mode, first_board)
    #this gives the gamestate
    #if the game is still running, continue to make moves and update 
    
    while game_state.check_all_moves():
        score = game_state.count_pieces()
        print('{}: {} {}:{}'.format(game_state.player1,score[0],game_state.player2,score[1]))
        print('TURN: {}'.format(game_state.whosturn))
        game_state.print_board()
        move = make_move()

        if game_state.valid_move(move) == True:
            print('VALID')
            game_state.flip_all(move)
            print(game_state.turn())
            
        else: 
            print('INVALID')
        score = game_state.count_pieces()
        print('{}: {} {}:{}'.format(game_state.player1,score[0],game_state.player2,score[1]))
        print('its {} turn'.format(game_state.whosturn))
        game_state.print_board()
           
    game_state.get_winner(game_mode)
