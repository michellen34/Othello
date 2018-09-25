#be able to take whatever the user inputed (rows, columns, mode, and first board)
#Take the 4 inputs and create your own board
#to do so you have to convert the strings that were inputed in the UI to numbers
#after you make a board, you want to be able to count the pieces in the board
#so each piece should have an identity aka its color
#we can refer to the color as a way to determine what turn it is
#we switch turns if the player has no more valid moves (multiply by -1)
#the most updated board should print
#and then the user should be able to make a move '1 2' (row one, place 2) (remember 0 based indexing so -1 to whatever they input)
#we have to be able to check if a move is valid
#a valid move is like a sandwich move (BWB)->(BBB)
#if there are no more valid moves, then hey, raise an exception and move on to the next player
#but what if no player can make a move? end game
#how to end game? well count all the pieces and then determine the winner based off the game mode


class InvalidMoveError(Exception):
    pass


class GameState:
    def __init__(self, rows, columns, player1, mode, first_board):
        #this takes in all the values that the user inputed
        self.rows = rows
        self.columns = columns
        self.mode = mode
        self.player1 = player1
        self.player2 = ''
        if self.player1 == 'B':
            self.player2 = 'W'
        elif self.player1 == 'W':
            self.player2 = 'B'
        self.first_board = first_board
        self.board = self.convert_first_board()
        self.whosturn = self.player1


    def convert_first_board(self)-> [[int]]:
        '''the user inputed the given parameters in the UI, now
            take all that information and make a new board that
            has integers instead of strings and make it a 2D list'''

        board = []
        for row in range(self.rows):
            board.append([])
            #creates empty row lists that can be filled with pieces
            for col in range(self.columns):
                conv=self.convert(self.first_board[row][col])
                board[-1].append(conv)
                #filled up the empty lists with actual game pieces
                #uses function convert to change the pieces from str to int
        return board


    def convert(self, player)->int: 
        '''changes player piece strings into 1, -1, or 0
            if player 1 is the same as the player passed through
            the parameter, then set it to 1'''
        
        if self.player1 == player:
            return 1
        if self.player2 == player:
            return -1
        else:
            return 0
        

    def convert_back(self, number)->str:
        '''converts int player pieces back to str'''
        if number == 1:
            number = self.player1
            return number
        if number == -1:
            number = self.player2
            return number
        else:
            number = '.'
            return number

    def count_pieces(self)-> tuple:
        '''count the pieces of the latest board and return
            a score board'''
        p1pieces = 0
        p2pieces = 0
        score_board = [p1pieces, p2pieces]
        for row in self.board:
            for piece in row:
                
                if piece == self.convert(self.player1):
                    p1pieces +=1
                if piece == self.convert(self.player2):
                    p2pieces +=1
        score_board = [p1pieces, p2pieces]
        return score_board


    def turn(self)-> bool:
        ''''if check_all_moves() returns False, that means a player has no more
            available moves and the next player should make a move, if both players
            cannot make a move then return False'''
        
        if self.player1 == self.whosturn:
            self.alternate()
            if self.check_all_moves() == False:

                if self.player2 == self.whosturn:
                    if self.check_all_moves() == False:
                        return False
        elif self.player2 == self.whosturn:
            self.alternate()
            if self.check_all_moves() == False:
                
                if self.player1 == self.whosturn:
                    if self.check_all_moves == False:
                        return False
        
        return True
                        
        
                    
            
    def alternate(self):
        '''switches the player turn by multiplying the player value by -1'''
        self.whosturn = self.convert_back(-1 * self.convert(self.whosturn))
        
    def check_dimensions(self, move_input, board)-> bool:
        x = int(move_input[0]) - 1
        y = int(move_input[0]) - 1
        if board[x][y] == 0:
            if x > self.rows:
                raise InvalidMoveError
            elif y > self.columns:
                raise InvalidMoveError
            else:
                return True
        else:
            return False

    def check_all_moves(self)->bool:
        '''checks if any of the empty spots on the board can produce a valid move'''
        #if self.valid_move(move_input) == True:
        for row in range(self.rows):
            for pieces in range(self.columns):

                #55if self.board[row][pieces] == 0:
                    b =self.valid_move((row, pieces))
                    #print(b)
                    
                    if self.valid_move((row+1,pieces+1)) == True:
                        #if there is a possible move for one of the empty spaces,
                        #then return True
                        #must check every every empty spot before returning False
                        return True
        
        return False
    def flip_direct(self, row, col, x, y):
        inc_x= x
        inc_y= y

        self.board[row][col]=self.whosturn
        while 0<=row<self.rows and 0<= col < self.columns and self.board[row][col]!=0:
            self.board[row][col]=self.convert(self.whosturn)
            row+=x
            col+=y
            
    def flip_all(self, move_input):
        x = int(move_input[0]) - 1
        y = int(move_input[1]) - 1
        if self.check_valid(move_input,0,1) == True:

            self.flip_direct(x,y,0, 1)
        if self.check_valid(move_input,1,1) == True:

            self.flip_direct(x,y, 1, 1)
        if self.check_valid(move_input,1,0) == True:

            self.flip_direct(x,y, 1, 0)

        if self.check_valid(move_input,1,-1) == True:

            self.flip_direct(x,y, 1, -1)
        if self.check_valid(move_input,0,-1) == True:

            self.flip_direct(x, y, 0, -1)
        if self.check_valid(move_input,-1,-1) == True:

            self.flip_direct(x, y, -1, -1)
        if self.check_valid(move_input,-1,0) == True:

            self.flip_direct(x,y, -1, 0)
        if self.check_valid(move_input,-1,1) == True:
            self.flip_direct(x, y, -1, 1)

    def valid_move(self,move_input) -> bool:
        '''checks if any of the 8 possible directions of a piece is possible'''
        
        b= self.check_valid(move_input, 0, 1) \
                or self.check_valid(move_input, 1, 1) \
                or self.check_valid(move_input, 1, 0) \
                or self.check_valid(move_input, 1, -1) \
                or self.check_valid(move_input, 0, -1) \
                or self.check_valid(move_input, -1, -1) \
                or self.check_valid(move_input, -1, 0) \
                or self.check_valid(move_input, -1, 1)
       
        return b


    def check_valid(self, move_input, shift_x, shift_y)-> bool:
        #given a spot on the board, check if that spot is empty, if not abandon ship
        #ok now that that spot is empty, check the 8 directions it can move
        #if the outward direction is not your piece then yay! if not, abandon ship
        #now move outwards again, if its your piece, then stop and flip all the ones
        #that was going that direction from your initial point
        #but if its not your piece, keep going, if its empty abandon ship
        #keep checking until you see your piece again
        #however if you reach the boundaries of the board, then return FALSE
        #if you can flip your pieces, return true

        x = int(move_input[0]) - 1
        y = int(move_input[1]) - 1
        next_shiftx = shift_x
        next_shifty = shift_y
        first = True
        
        while True:
            #print(x  + next_shiftx,y  + next_shifty)
            if 0 <= x  + next_shiftx < self.rows and 0 <= y  + next_shifty < self.columns:
                    if (self.board[x][y]!=0):
                        
                        return False
                #this makes sure that when checking the next outward position, it does not check past the boundaries of the board
                #if GameState.check_dimensions(self, move_input, board):
                    #print('index {} {}  found {}'.format(x+shift_x,y+shift_y,self.board[x+shift_x][y+shift_y]))
                    
                    if first:
                       
                        #if self.board[x + shift_x][y + shift_y] != self.convert(self.whosturn):
                            #checks the first outward position and makes sure it is not its own piece
                        #    first = False
                        if self.board[x + shift_x][y + shift_y] == 0:
                            #if the first outward position is empty, can't make the move
                            return False
                        
                        if self.board[x + shift_x][y + shift_y] == self.convert(self.whosturn):
                            #if the first outward position is itself, can't make move
                            return False
                        first = False
                    else:


                        if self.board[x  + next_shiftx][y  + next_shifty] == 0:
                            #if there is an empty piece, you cannot move here
                            return False
                        if self.board[x  + next_shiftx][y + next_shifty] == self.convert(self.whosturn):
                            #because we have passed the first outward movement, if the next piece we hit is the identity of the player
                            #then you can go back and flip all the pieces (in flip function)
                            return True
                    
                    next_shiftx += shift_x
                    next_shifty += shift_y
            else:
                
                return False


    def get_winner(self, mode):
        '''if no more players can make a turn, return the final score and end game'''
        score = self.count_pieces()
        p1pieces = score[0]
        p2pieces = score[1]
        if self.turn() == False:
            if self.mode == '>':
                if p1pieces > p2pieces:
                    print('WINNER: ' + self.player1)
                if p2pieces > p1pieces:
                    print('WINNER: ' + self.player2)
                if p1pieces == p2pieces:
                    print('WINNER: NONE')
            if self.mode == '<':
                if p1pieces > p2pieces:
                    print('WINNER: ' + self.player2)
                if p2pieces > p1pieces:
                    print('WINNER: ' + self.player1)
                if p1pieces == p2pieces:
                    print('WINNER: NONE')          
            
    def print_board(self):
        board = ''
        for row in range(self.rows):
            board = ''
            for pieces in range(self.columns):
                board += str(self.convert_back(self.board[row][pieces])) + ' '
            print(board) 
        

'''
board = [['.','.','.','.'], ['W','W','W','.'],['.','W','B','.'], ['.','.','.','.']]
test = GameState(4, 4, 'B', '>', board)
print(test.print_board())
test.alternate()
check = test.check_all_moves()
print(test.whosturn)
#check = test.check_valid((3,4),0,-1)
print(test.count_pieces())
#next_step = test.flip_all((2,4))
#print(test.board)
'''





    
