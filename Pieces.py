import pygame
import copy
import os

pygame.init()

current_path = os.path.dirname(os.path.abspath(__file__))

class Pieces:
    def __init__(self):
        self.size = (90, 90)
        self.white_pieces = ["white", "white_pawn", "white_rook", "white_bishop", "white_knight", "white_queen", "white_king"]
        self.black_pieces = ["black", "black_pawn", "black_rook", "black_bishop", "black_knight", "black_queen", "black_king"]
        self.white_pawn_home_squares = ["a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2"]
        self.black_pawn_home_squares = ["a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7"]
        self.white_can_short_castle = True
        self.black_can_short_castle = True
        self.white_can_long_castle = True
        self.black_can_long_castle = True
        self.white_in_check = False
        self.black_in_check = False
        
    def render(self, surface, map={}):
        count = 0
        for i in map:
            if map[i] != None:
                x = (count % 8) * 100
                y = (count // 8) * 100
                self.piece = pygame.image.load(f"{current_path}\\sprites\\{map[i]}.png").convert_alpha()
                self.piece = pygame.transform.scale(self.piece, self.size)
                surface.blit(self.piece, (x + 5, y + 2.5))
            count += 1

    def is_square_attacked(self, colour="", square="", squares=[], map={}):
        targets = []
        
        if colour == "white":
            position = 0
            for i in squares:
                if map[i] == "black_pawn":
                    targets += self.pawn("black", position, squares, map)
                if map[i] == "black_knight":
                    targets += self.knight("black", position, squares, map)
                if map[i] == "black_rook":
                    targets += self.rook("black", position, squares, map)
                if map[i] == "black_bishop":
                    targets += self.bishop("black", position, squares, map)
                if map[i] == "black_queen":
                    targets += self.queen("black", position, squares, map)
                position += 1
        elif colour == "black":
            position = 0
            for i in squares:
                if map[i] == "white_pawn":
                    targets += self.pawn("white", position, squares, map)
                if map[i] == "white_knight":
                    targets += self.knight("white", position, squares, map)
                if map[i] == "white_rook":
                    targets += self.rook("white", position, squares, map)
                if map[i] == "white_bishop":
                    targets += self.bishop("white", position, squares, map)
                if map[i] == "white_queen":
                    targets += self.queen("white", position, squares, map)
                position += 1
        return square in targets
    
    def find_square(self, piece, squares=[], map={}):
        for i in squares:
            if map[i] == piece:
                return i + "!"

#PIECE MOVING SQUARES
    def possible_squares(self, type="", colour="",pos=0, squares=[], map={}):
        if type == "pawn":
            return self.pawn(colour, pos, squares, map)
        elif type == "knight":
            return self.knight(colour, pos, squares, map)
        elif type == "rook":
            return self.rook(colour, pos, squares, map)
        elif type == "bishop":
            return self.bishop(colour, pos, squares, map)
        elif type == "queen":
            return self.queen(colour, pos, squares, map)
        elif type == "king":
            return self.king(colour, pos, squares, map)
        
    def pawn(self, colour="", pos=0, squares=[], map={}):
        targets = []
        current = copy.deepcopy(pos)
        #WHITE
        if colour=="white":
            #TWO STEPS
            if squares[pos] in self.white_pawn_home_squares:
                for i in range(2):
                    if not map[squares[current - 8]]: 
                        targets.append(squares[current - 8])
                        current -= 8
                    else:  
                        break
            #ONE STEP
            else:
                if not map[squares[pos - 8]]: 
                        targets.append(squares[pos - 8])

            #TOP LEFT
            if (pos % 8) >= 1:
                if map[squares[pos - 9]] in self.black_pieces:
                    targets.append(squares[pos - 9] + "!")
            
            #TOP RIGHT
            if (pos % 8) <= 6:
                if map[squares[pos - 7]] in self.black_pieces:
                    targets.append(squares[pos - 7] + "!")
       
        #BLACK
        else:
            #TWO STEPS
            if squares[pos] in self.black_pawn_home_squares:
                for i in range(2):
                    if not map[squares[current + 8]]: 
                        targets.append(squares[current + 8])
                        current += 8
                    else:  
                        break
            #ONE STEP
            else:
                if not map[squares[pos + 8]]: 
                        targets.append(squares[pos + 8])

            #BOTTOM LEFT
            if (pos % 8) >= 1:
                if map[squares[pos + 7]] in self.white_pieces:
                    targets.append(squares[pos + 7] + "!")
            
            #BOTTOM RIGHT
            if (pos % 8) <= 6:
                if map[squares[pos + 9]] in self.white_pieces:
                    targets.append(squares[pos + 9] + "!")

        return targets
    
    def knight(self, colour="", pos=0, squares=[], map={}):
        targets = []
        #MID UP LEFT
        if (pos % 8) >= 2 and (pos // 8) >= 1:
            if not map[squares[pos - 10]]:
                targets.append(squares[pos - 10])
            elif (map[squares[pos - 10]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 10]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos - 10] + "!")  
        
        #UP LEFT
        if (pos % 8) >= 1 and (pos // 8) >= 2:
            if not map[squares[pos - 17]]:
                targets.append(squares[pos - 17])
            elif (map[squares[pos - 17]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 17]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos - 17] + "!")  
        
        #UP RIGHT
        if (pos % 8) <= 6 and (pos // 8) >= 2:
            if not map[squares[pos - 15]]:
                targets.append(squares[pos - 15])
            elif (map[squares[pos - 15]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 15]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos - 15] + "!")  

        #MID UP RIGHT
        if (pos % 8) <= 5 and (pos // 8) >= 1:
            if not map[squares[pos - 6]]:
                targets.append(squares[pos - 6])
            elif (map[squares[pos - 6]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 6]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos - 6] + "!")  
        
        #MID LOW RIGHT
        if (pos % 8) <= 5 and (pos // 8) <= 6:
            if not map[squares[pos + 10]]:
                targets.append(squares[pos + 10])
            elif (map[squares[pos + 10]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 10]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos + 10] + "!")  

        #LOW RIGHT
        if (pos % 8) <= 6 and (pos // 8) <= 5:
            if not map[squares[pos + 17]]:
                targets.append(squares[pos + 17])
            elif (map[squares[pos + 17]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 17]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos + 17] + "!")  

        #LOW LEFT
        if (pos % 8) >= 1 and (pos // 8) <= 5:
            if not map[squares[pos + 15]]:
                targets.append(squares[pos + 15])
            elif (map[squares[pos + 15]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 15]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos + 15] + "!")  

        #MID UP LEFT
        if (pos % 8) >= 2 and (pos // 8) <= 6:
            if not map[squares[pos + 6]]:
                targets.append(squares[pos + 6])
            elif (map[squares[pos + 6]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 6]] in self.black_pieces and colour in self.white_pieces):
                targets.append(squares[pos + 6] + "!")  
        return targets

    def rook(self, colour="", pos=0, squares=[], map={}):
        targets = [] 
        #UP
        if (pos // 8) >= 1:
            targets += self.find_up(colour, pos, squares, map, targets)
        
        #RIGHT
        if (pos % 8) <= 6:
            targets += self.find_right(colour, pos, squares, map, targets)

        #DOWN
        if (pos // 8) <= 6:
            targets += self.find_down(colour, pos, squares, map, targets)
        
        #LEFT
        if (pos % 8) >= 1:
            targets += self.find_left(colour, pos, squares, map, targets)
        return targets

    def bishop(self, colour="", pos=0, squares=[], map={}):
        targets = []
        #TOP LEFT
        if (pos % 8) >= 1 and (pos // 8) >= 1:
            targets += self.find_top_left(colour, pos, squares, map, targets)
        
        #TOP RIGHT
        if (pos % 8) <= 6 and (pos // 8) >= 1:
            targets += self.find_top_right(colour, pos, squares, map, targets)
            
        #BOTTOM LEFT
        if (pos % 8) >= 1 and (pos // 8) <= 6:
            targets += self.find_bottom_left(colour, pos, squares, map, targets)

        #BOTTOM RIGHT
        if (pos % 8) <= 6 and (pos // 8) <= 6:
            targets += self.find_bottom_right(colour, pos, squares, map, targets)
        
        return targets

    def queen(self, colour="", pos=0, squares=[], map={}):
        targets = [] 
        #UP
        if (pos // 8) >= 1:
            targets += self.find_up(colour, pos, squares, map, targets)
        
        #RIGHT
        if (pos % 8) <= 6:
            targets += self.find_right(colour, pos, squares, map, targets)

        #DOWN
        if (pos // 8) <= 6:
            targets += self.find_down(colour, pos, squares, map, targets)
        
        #LEFT
        if (pos % 8) >= 1:
            targets += self.find_left(colour, pos, squares, map, targets)
    
        #TOP LEFT
        if (pos % 8) >= 1 and (pos // 8) >= 1:
            targets += self.find_top_left(colour, pos, squares, map, targets)
        
        #TOP RIGHT
        if (pos % 8) <= 6 and (pos // 8) >= 1:
            targets += self.find_top_right(colour, pos, squares, map, targets)
            
        #BOTTOM LEFT
        if (pos % 8) >= 1 and (pos // 8) <= 6:
            targets += self.find_bottom_left(colour, pos, squares, map, targets)

        #BOTTOM RIGHT
        if (pos % 8) <= 6 and (pos // 8) <= 6:
            targets += self.find_bottom_right(colour, pos, squares, map, targets)
    
        return targets

    def king(self, colour="", pos=0, squares=[], map={}):
        targets = []
        #UP
        if (pos // 8) >= 1:
            if not map[squares[pos - 8]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 8], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 8], squares, map))):
                targets.append(squares[pos - 8])
            elif ((map[squares[pos - 8]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 8]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 8], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 8], squares, map))):
                targets.append(squares[pos - 8] + "!")
        #DOWN
        if (pos // 8) <= 6:
            if not map[squares[pos + 8]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 8], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 8], squares, map))):
                targets.append(squares[pos + 8])
            elif ((map[squares[pos + 8]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 8]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 8], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 8], squares, map))):
                targets.append(squares[pos + 8] + "!")
        
        #LEFT
        if (pos % 8) >= 1:
            if not map[squares[pos - 1]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 1], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 1], squares, map))):
                targets.append(squares[pos - 1])
            elif ((map[squares[pos - 1]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 1]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 1], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 1], squares, map))):
                targets.append(squares[pos - 1] + "!")

        #RIGHT
        if (pos % 8) <= 6:
            if not map[squares[pos + 1]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 1], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 1], squares, map))):
                targets.append(squares[pos + 1])
            elif ((map[squares[pos + 1]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 1]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 1], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 1], squares, map))):
                targets.append(squares[pos + 1] + "!")

        #TOP LEFT
        if (pos % 8) >= 1 and (pos // 8) >= 1:
            if not map[squares[pos - 9]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 9], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 9], squares, map))):
                targets.append(squares[pos - 9])
            elif ((map[squares[pos - 9]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 9]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 9], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos -9], squares, map))):
                targets.append(squares[pos - 9] + "!")

        #TOP RIGHT
        if (pos % 8) <= 6 and (pos // 8) >= 1:
            if not map[squares[pos - 7]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 7], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 7], squares, map))):
                targets.append(squares[pos - 7])
            elif ((map[squares[pos - 7]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 7]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos - 7], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos - 7], squares, map))):
                targets.append(squares[pos - 7] + "!")
            
        #BOTTOM LEFT
        if (pos % 8) >= 1 and (pos // 8) <= 6:
            if not map[squares[pos + 7]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 7], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 7], squares, map))):
                targets.append(squares[pos + 7])
            elif ((map[squares[pos + 7]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 7]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 7], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 7], squares, map))):
                targets.append(squares[pos + 7] + "!")

        #BOTTOM RIGHT
        if (pos % 8) <= 6 and (pos // 8) <= 6:
            if not map[squares[pos + 9]] and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 9], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 9], squares, map))):
                targets.append(squares[pos + 9])
            elif ((map[squares[pos + 9]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 9]] in self.black_pieces and colour in self.white_pieces)) and ((colour in self.white_pieces and not self.is_square_attacked("white", squares[pos + 9], squares, map)) or (colour in self.black_pieces and not self.is_square_attacked("black", squares[pos + 9], squares, map))):
                targets.append(squares[pos + 9] + "!")

        #CASTLE
        #SHORT CASTLE
        if ((colour=="white" and self.white_can_short_castle) or (colour=="black" and self.black_can_short_castle)) and not ((self.white_in_check or self.is_square_attacked("white", "f1", squares, map) or self.is_square_attacked("white", "g1", squares, map)) or (self.black_in_check or self.is_square_attacked("black", "f8", squares, map) or self.is_square_attacked("black", "g8", squares, map))):     
            if not (map[squares[pos + 1]] or map[squares[pos + 2]]):
                targets.append(squares[pos + 2])
            #LONG CASTLE
        if (colour=="white" and self.white_can_long_castle) or (colour=="black" and self.black_can_long_castle):    
            if not (map[squares[pos - 1]] or map[squares[pos - 2]] or map[squares[pos - 3]]):
                targets.append(squares[pos - 2])

        return targets

    #VERTICAL MOVEMENT
    def find_up(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos - 8]]:
            targets.append(squares[pos - 8])
            if ((pos - 8) // 8) >= 1:
                self.find_up(colour, pos - 8, squares, map, targets)
        elif (map[squares[pos - 8]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 8]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos - 8] + "!")

        return targets

    def find_down(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos + 8]]:
            targets.append(squares[pos + 8])
            if ((pos + 8) // 8) <= 6:
                self.find_down(colour, pos + 8, squares, map, targets)
        elif (map[squares[pos + 8]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 8]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos + 8] + "!")

        return targets
    
    #HORIZONTAL MOVEMENT
    def find_left(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos - 1]]:
            targets.append(squares[pos - 1])
            if ((pos - 1) % 8) >= 1:
                self.find_left(colour, pos - 1, squares, map, targets)
        elif (map[squares[pos - 1]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 1]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos - 1] + "!")

        return targets
    
    def find_right(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos + 1]]:
            targets.append(squares[pos + 1])
            if ((pos + 1) % 8) <= 6:
                self.find_right(colour, pos + 1, squares, map, targets)
        elif (map[squares[pos + 1]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 1]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos + 1] + "!")

        return targets
    
    #DIAGONAL MOVEMENT
    def find_top_left(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos - 9]]:
            targets.append(squares[pos - 9])
            if ((pos - 9) % 8) >= 1 and ((pos - 9) // 8) >= 1:
                self.find_top_left(colour, pos - 9, squares, map, targets)
        elif (map[squares[pos - 9]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 9]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos - 9] + "!")
        return targets
    
    def find_top_right(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos - 7]]:
            targets.append(squares[pos - 7])
            if ((pos - 7) % 8) <= 6 and ((pos - 7) // 8) >= 1:
                self.find_top_right(colour, pos - 7, squares, map, targets)
        elif (map[squares[pos - 7]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos - 7]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos - 7] + "!")
        return targets
    
    def find_bottom_left(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos + 7]]:
            targets.append(squares[pos + 7])
            if ((pos + 7) % 8) >= 1 and ((pos + 7) // 8) <= 6:
                self.find_bottom_left(colour, pos + 7, squares, map, targets)
        elif (map[squares[pos + 7]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 7]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos + 7] + "!")
        return targets
    
    def find_bottom_right(self, colour="", pos=0, squares=[], map={}, targets=[]):
        if not map[squares[pos + 9]]:
            targets.append(squares[pos + 9])
            if ((pos + 9) % 8) <= 6 and ((pos + 9) // 8) <= 6:
                self.find_bottom_right(colour, pos + 9, squares, map, targets)
        elif (map[squares[pos + 9]] in self.white_pieces and colour in self.black_pieces) or (map[squares[pos + 9]] in self.black_pieces and colour in self.white_pieces):
            targets.append(squares[pos + 9] + "!")
        return targets