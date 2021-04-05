import copy
import random
import time

class Game():

    def __init__(self):
        self.board = [["-" for i in range(8)] for j in range(8)]
        self.prev_moves = [] #previous moves made in the game, initially none
        self.board[7] = ["r", "n", "b", "q", "k", "b", "n", "r"]
        self.board[6] = ["p", "p", "p", "p", "p", "p", "p", "p"]

        self.board[1] = ["P", "P", "P", "P", "P", "P", "P", "P"]
        self.board[0] = ["R", "N", "B", "Q", "K", "B", "N", "R"]

        

class Player():
    def __init__(self, game):
        self.game = game
        self.board = game.board
        self.whitePieces = ["R", "N", "B", "Q", "K", "P"]
        self.blackPieces = ["r", "n", "b", "q", "k", "p"]

    def displayBoard(self, board=0):
        if(board == 0):
            board = self.board
        result = ""
        for i in range(8):
            tmpRow = ""
            for piece in board[i]:
                tmpRow += piece + " "
            result = tmpRow + "\n" + result
        result = result + "\n"

        cooldisplay = 1 #TODO: JUST TEMPORARY FOR SHOWING THE BOARD
        if(cooldisplay != 1):
            print(result)
        else:
            
            print(result)
            


    
    def setPiece(self, pieceSymbol, x, y, board=0): #duplicate method of
        if(board == 0):
            board = self.board
        try:
            board[y][x] = pieceSymbol
        except:
            print("Error in setPiece method.")
            return 0

    def getPiece(self, x, y, board=0): #returns piece in position (x,y)
        if(board == 0):
            board = self.board
        if(x < 0 or y < 0):
            return None
        try:
            return board[y][x]
        except:
            return None
    
    def isPlayerCheck(self, board):
        """RETURNS tuple (check_white, check_black) where True is if white is in check, or False for not in check.
        If black is in check in the current position but not white, it will return (0,1)"""
        moves_white = self.getUnfinishedMoves("white", board)
        moves_black = self.getUnfinishedMoves("black", board)
        
        #find out where the kings-position is:
        for y in range(8):
            for x in range(8):
                if(board[y][x] == "k"):
                    king_b_x = x
                    king_b_y = y
                if(board[y][x] == "K"):
                    king_w_x = x
                    king_w_y = y

        check_black = False
        check_white = False
        #see if white king is in check
        for move in moves_black:
            if(int(move[-2:][0]) == king_w_x and int(move[-2:][1]) == king_w_y): #black piece can capture white king
                check_white = True
        for move in moves_white:
            if(int(move[-2:][0]) == king_b_x and int(move[-2:][1]) == king_b_y): #white piece can capture black king
                check_black = True

        return (check_white, check_black)
    
    def makeMove(self, move, myboard=0):
        """board, move. move is a string.
        RETURNS A BOARD"""
        if(myboard == 0):
            myboard = self.board
        parts = []
        for i in range(len(move)//2):
            parts.append(move[i*2:(i+1)*2])
        
        if(len(parts) == 2):
            firstPiece = self.getPiece(int(parts[0][0]), int(parts[0][1]), myboard) #(x, y)
            firstPos = (int(parts[0][0]), int(parts[0][1]))
            secondPos = (int(parts[1][0]), int(parts[1][1]))
            #setting the pieces
            self.setPiece(firstPiece, secondPos[0], secondPos[1], myboard)
            self.setPiece("-", firstPos[0], firstPos[1], myboard)
        
        elif(len(parts) == 4): #example: castling 40607050, or promoting to a queen 4647.QQ47
            #logic
            firstPos = (int(parts[0][0]), int(parts[0][1]))
            secondPos = (int(parts[1][0]), int(parts[1][1]))
            fourthPos = (int(parts[3][0]), int(parts[3][1]))

            firstPiece = self.getPiece(int(parts[0][0]), int(parts[0][1]), myboard)
            if(parts[2] in ["QQ", "BB", "NN", "RR", "qq", "bb", "nn", "rr"]):
                secondPiece = parts[2][0:1]
                self.setPiece(firstPiece, secondPos[0], secondPos[1], myboard)
                self.setPiece("-", firstPos[0], firstPos[1], myboard)
                self.setPiece(secondPiece, fourthPos[0], fourthPos[1], myboard)
            else:
                secondPiece = self.getPiece(int(parts[2][0]), int(parts[2][1]), myboard)
                thirdPos = (int(parts[2][0]), int(parts[2][1]))
                self.setPiece(firstPiece, secondPos[0], secondPos[1], myboard)
                self.setPiece("-", firstPos[0], firstPos[1], myboard)
                self.setPiece(secondPiece, fourthPos[0], fourthPos[1], myboard)
                self.setPiece("-", thirdPos[0], thirdPos[1], myboard)
        
        return myboard

    def getUnfinishedMoves(self, playerTurn, board=0, prevMoves=0):
        """RETURNS list of not-validated moves for checks"""
        if(board == 0):
            board = self.board
        if(prevMoves == 0):
            prevMoves = self.game.prev_moves
        
        if(playerTurn == "white"):
            opponentsPieces = self.blackPieces
            ownPieces = self.whitePieces
        else:
            opponentsPieces = self.whitePieces
            ownPieces = self.blackPieces

        tmpMoves = []
        #bla gjennom hver 
        for y in range(8):
            for x in range(8):
                tmpPiece = self.getPiece(x, y, board)
                if(tmpPiece != None): #hvis det er en brikke, finn alle trekkene til den brikken.
                    if(playerTurn == "white"):
                        if(tmpPiece == "P"): #TODO: legg inn support for en-passant, ved sjekke tidligere moves.
                            #check 1 up
                            tmpY = y + 1
                            square = self.getPiece(x, tmpY, board)
                            tmpMove = str(x) + str(y) + str(x) + str(tmpY)
                            if(square == None): #outside of board, this is actually never gonna happen but whatevs
                                pass
                            if(square == "-"): #open square ahead
                                if(tmpY == 7): #promote
                                    tmpMove += "QQ" + str(x) + str(tmpY)
                                tmpMoves.append(tmpMove)
                                if(y == 1): #if pawn is at starting position, it can move 2 up if clear.
                                    tmpY = y + 2
                                    square = self.getPiece(x, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(x) + str(tmpY)
                                    if(square == "-"): #if that square is clear
                                        tmpMoves.append(tmpMove)
                            
                            #check upright
                            tmpY = y + 1
                            tmpX = x + 1
                            square = self.getPiece(tmpX, tmpY, board)
                            tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                            if(square in opponentsPieces):
                                if(tmpY == 7): #promote
                                    tmpMove += "QQ" + str(tmpX) + str(tmpY)
                                tmpMoves.append(tmpMove)
                            

                            #check upleft
                            tmpX = x - 1
                            square = self.getPiece(tmpX, tmpY, board)
                            tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                            if(square in opponentsPieces):
                                if(tmpY == 7): #promote
                                    tmpMove += "QQ" + str(tmpX) + str(tmpY)
                                tmpMoves.append(tmpMove)

                        elif(tmpPiece == "R"):
                            #append the moves to moves-array
                            #check above
                            rookjumps = [[(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                                        [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                                        [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                                        [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)]]
                            for direction in rookjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)

                        elif(tmpPiece == "N"):
                            #checks in all directions
                            horsejumps = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
                            for k in range(8):
                                tmpX = x + horsejumps[k][0]
                                tmpY = y + horsejumps[k][1]
                                square = self.getPiece(tmpX, tmpY, board)
                                tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                if(square != "-" and (square in opponentsPieces)): #opponents piece
                                    tmpMoves.append(tmpMove)
                                elif(square == "-"):
                                    tmpMoves.append(tmpMove)

                        elif(tmpPiece == "B"):
                            #check up-right
                            bishopjumps = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                                            [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                                            [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                                            [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]]
                            for direction in bishopjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)
                            
                        elif(tmpPiece == "Q"):
                            #append the moves to moves-array
                            #check above
                            queenjumps = [
                                        [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                                        [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                                        [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                                        [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)],
                                        [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                                        [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                                        [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                                        [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]
                                        ]
                            for direction in queenjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)

                        elif(tmpPiece == "K"):
                            kingjumps = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
                            for k in range(8):
                                tmpX = x + kingjumps[k][0]
                                tmpY = y + kingjumps[k][1]
                                square = self.getPiece(tmpX, tmpY, board)
                                tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                if(square != "-" and (square in opponentsPieces)): #opponents piece
                                    tmpMoves.append(tmpMove)
                                elif(square == "-"):
                                    tmpMoves.append(tmpMove)

                    elif(playerTurn == "black"):
                        if(tmpPiece == "p"): #TODO: legg inn support for en-passant, ved sjekke tidligere moves.
                            #check 1 down
                            tmpY = y - 1
                            square = self.getPiece(x, tmpY, board)
                            tmpMove = str(x) + str(y) + str(x) + str(tmpY)
                            if(square == None): #outside of board, this is actually never gonna happen but whatevs
                                pass
                            if(square == "-"): #open square ahead
                                if(tmpY == 0): #promote
                                    tmpMove += "qq" + str(x) + str(tmpY)
                                tmpMoves.append(tmpMove)
                                if(y == 6): #if pawn is at starting position, it can move 2 down if clear.
                                    tmpY = y - 2
                                    square = self.getPiece(x, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(x) + str(tmpY)
                                    if(square == "-"): #if that square is clear
                                        tmpMoves.append(tmpMove)
                            
                            #check downright
                            tmpY = y - 1
                            tmpX = x + 1
                            square = self.getPiece(tmpX, tmpY, board)
                            tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                            if(square in opponentsPieces):
                                if(tmpY == 0): #promote
                                    tmpMove += "qq" + str(tmpX) + str(tmpY)
                                tmpMoves.append(tmpMove)

                            #check downleft
                            tmpX = x - 1
                            square = self.getPiece(tmpX, tmpY, board)
                            tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                            if(square in opponentsPieces):
                                if(tmpY == 0): #promote
                                    tmpMove += "qq" + str(tmpX) + str(tmpY)
                                tmpMoves.append(tmpMove)

                        elif(tmpPiece == "r"):
                            #append the moves to moves-array
                            #check above
                            rookjumps = [
                                [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                                [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                                [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                                [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)]
                                ]
                            for direction in rookjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    # print(str(tmpX) + str(tmpY))
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)

                        elif(tmpPiece == "n"):
                            #checks in all directions
                            horsejumps = [(1,2), (1,-2), (2,1), (2,-1), (-1,2), (-1,-2), (-2,1), (-2,-1)]
                            for k in range(8):
                                tmpX = x + horsejumps[k][0]
                                tmpY = y + horsejumps[k][1]
                                square = self.getPiece(tmpX, tmpY, board)
                                tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                if(square != "-" and (square in opponentsPieces)): #opponents piece
                                    tmpMoves.append(tmpMove)
                                elif(square == "-"):
                                    tmpMoves.append(tmpMove)

                        elif(tmpPiece == "b"):
                            #check up-right
                            bishopjumps = [[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                                            [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                                            [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                                            [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]]
                            for direction in bishopjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)
                            
                        elif(tmpPiece == "q"):
                            #append the moves to moves-array
                            #check above
                            queenjumps = [
                                        [(0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7)],
                                        [(0,-1), (0,-2), (0,-3), (0,-4), (0,-5), (0,-6), (0,-7)],
                                        [(1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0)],
                                        [(-1,0), (-2,0), (-3,0), (-4,0), (-5,0), (-6,0), (-7,0)],
                                        [(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)],
                                        [(-1,1), (-2,2), (-3,3), (-4,4), (-5,5), (-6,6), (-7,7)],
                                        [(1,-1), (2,-2), (3,-3), (4,-4), (5,-5), (6,-6), (7,-7)],
                                        [(-1,-1), (-2,-2), (-3,-3), (-4,-4), (-5,-5), (-6,-6), (-7,-7)]
                                        ]
                            for direction in queenjumps:
                                for k in range(7):
                                    tmpX = x + direction[k][0]
                                    tmpY = y + direction[k][1]
                                    square = self.getPiece(tmpX, tmpY, board)
                                    tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                    if(square == None): #outside of board
                                        break
                                    elif(square != "-" and (square in ownPieces)): #then it is my own piece ffs.
                                        break
                                    elif(square != "-" and (square in opponentsPieces)): #opponents piece
                                        tmpMoves.append(tmpMove)
                                        break
                                    elif(square == "-"):
                                        tmpMoves.append(tmpMove)

                        elif(tmpPiece == "k"):
                            kingjumps = [(1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1), (0,1)]
                            for k in range(8):
                                tmpX = x + kingjumps[k][0]
                                tmpY = y + kingjumps[k][1]
                                square = self.getPiece(tmpX, tmpY, board)
                                tmpMove = str(x) + str(y) + str(tmpX) + str(tmpY)
                                if(square != "-" and (square in opponentsPieces)): #opponents piece
                                    tmpMoves.append(tmpMove)
                                elif(square == "-"):
                                    tmpMoves.append(tmpMove)

        return tmpMoves #just temporary return to check if it works.

    def getAllowedMoves(self, playerTurn, board=0, prevMoves=0):
        if(board == 0):
            board = self.board
        if(prevMoves == 0):
            prevMoves = self.game.prev_moves
        if(playerTurn == "white"):
            opponentColor = "black"
            playerInt = 0
        else:
            opponentColor = "white"
            playerInt = 1

        unFinishedMoves = self.getUnfinishedMoves(playerTurn, board, prevMoves)
        
        approved_moves = []
        for move in unFinishedMoves:
            #try to do the move and see if itself is in check
            testBoard = copy.deepcopy(board)
            newBoard = self.makeMove(move, testBoard)
            if(self.isPlayerCheck(newBoard)[playerInt] == False):
                approved_moves.append(move)
        
        return approved_moves

    def playerStatus(self, playerTurn, board=0, prevMoves=0):
        """RETURNS:
        1 - Checkmate
        2 - Stalemate
        3 - Nothing at all, player has legal moves"""
        #if he has no legal moves, and his king is in check => checkmate maate
        if(playerTurn == "white"):
            playerInt = 0
        else:
            playerInt = 1

        mymoves = self.getAllowedMoves(playerTurn, board, prevMoves)
        if(len(mymoves) == 0):
            if(self.isPlayerCheck(board)[playerInt] == True):
                return 1 #1 is checkmate
            else:
                return 2 #stalemate, player has no moves left, but is not in check.
        else:
            return 3


def main():
    mygame = Game()
    myplayer = Player(mygame)
    myplayer.displayBoard()

    i = 0
    while(i < 1000):
        if(i % 2 == 0): #white to move
            playerTurn = "white"
        else:
            playerTurn = "black"
        
        moves = myplayer.getAllowedMoves(playerTurn, myplayer.board)
        status = myplayer.playerStatus(playerTurn, myplayer.board)
        if(status == 3): #nothing at all
            move_to_make = moves[random.randint(0, len(moves)-1)]
            myplayer.board = myplayer.makeMove(move_to_make, myplayer.board)
        elif(status == 2): #stalemate
            print("STALEMATE")
            return 2
        elif(status == 1): #checkmate
            print("CHECKMATE")
            return 1
        myplayer.displayBoard()
        time.sleep(0.01)
        i += 1


    


if(__name__ == "__main__"):
    main()

