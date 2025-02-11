import pygame

from Pieces import Pieces

pygame.init()

class Board:
    def __init__(self):
        #FOREIGNERS
        self.pieces = Pieces()

        #Properties
        self.cell_size = 100
        self.light = (234, 182, 118)
        self.dark = (135, 62, 35)

        self.turn = 1
        self.clicked_square = ""
        self.destination_square = ""
        
        self.map = {"a8": "black_rook", "b8": "black_knight", "c8": "black_bishop", "d8": "black_queen", "e8": "black_king", "f8": "black_bishop", "g8": "black_knight", "h8": "black_rook",
                    "a7": "black_pawn", "b7": "black_pawn", "c7": "black_pawn", "d7": "black_pawn", "e7": "black_pawn", "f7": "black_pawn", "g7": "black_pawn", "h7": "black_pawn",
                    "a6": None, "b6": None, "c6": None, "d6": None, "e6": None, "f6": None, "g6": None, "h6": None,
                    "a5": None, "b5": None, "c5": None, "d5": None, "e5": None, "f5": None, "g5": None, "h5": None,
                    "a4": None, "b4": None, "c4": None, "d4": None, "e4": None, "f4": None, "g4": None, "h4": None,
                    "a3": None, "b3": None, "c3": None, "d3": None, "e3": None, "f3": None, "g3": None, "h3": None,
                    "a2": "white_pawn", "b2": "white_pawn", "c2": "white_pawn", "d2": "white_pawn", "e2": "white_pawn", "f2": "white_pawn", "g2": "white_pawn", "h2": "white_pawn",
                    "a1": "white_rook", "b1": "white_knight", "c1": "white_bishop", "d1": "white_queen", "e1": "white_king", "f1": "white_bishop", "g1": "white_knight", "h1": "white_rook"
                    }

        
        """self.map = {"a8": "black_rook", "b8": "black_knight", "c8": "black_bishop", "d8": "black_queen", "e8": "black_king", "f8": "black_bishop", "g8": "black_knight", "h8": None,
                    "a7": None, "b7": None, "c7": None, "d7": "black_pawn", "e7": None, "f7": None, "g7": None, "h7": "white_pawn",
                    "a6": None, "b6": None, "c6": None, "d6": None, "e6": None, "f6": None, "g6": None, "h6": None,
                    "a5": None, "b5": None, "c5": None, "d5": None, "e5": None, "f5": None, "g5": None, "h5": None,
                    "a4": None, "b4": None, "c4": None, "d4": None, "e4": None, "f4": None, "g4": None, "h4": None,
                    "a3": None, "b3": None, "c3": None, "d3": None, "e3": None, "f3": None, "g3": None, "h3": None,
                    "a2": None, "b2": None, "c2": None, "d2": None, "e2": None, "f2": None, "g2": None, "h2": None,
                    "a1": "white_rook", "b1": "white_knight", "c1": "white_bishop", "d1": "white_queen", "e1": "white_king", "f1": "white_bishop", "g1": "white_knight", "h1": "white_rook"
                    }"""

        self.squares = [
                    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
                    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
                    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
                    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
                    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
                    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
                    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
                    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]

        self.potential_squares = []

    def hover(self, surface):
        x,y = pygame.mouse.get_pos()
        if self.over_clicked(x, y):
            return
        x = x // self.cell_size
        y = y // self.cell_size 
        box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
        pygame.draw.rect(surface, "gray", box)

    def find_coord(self, x, y):
        x = x // self.cell_size
        y = y // self.cell_size
        return  x + y*8
    
    def is_clicking_one_potential_square(self, x, y):
        if self.potential_squares:
            if self.squares[self.find_coord(x, y)] in self.potential_squares or (self.squares[self.find_coord(x, y)] + "!") in self.potential_squares:
                self.destination_square = self.squares[self.find_coord(x, y)]
                return self.move_piece()
        return False

    def move_piece(self):
        self.clicked_piece = self.map[self.clicked_square]
        self.destination_piece = self.map[self.destination_square]

        #WHITE
        if self.pieces.white_can_short_castle:
            #WHITE SHORT CASTLE
            if self.clicked_square == "e1" and self.destination_square == "g1":
                self.map["f1"] = self.map["h1"]
                self.map["h1"] = None   
            #CANCELING WHITE SHORT CASTLE   
            if self.clicked_square == "h1" or self.map[self.clicked_square] == "white_king":
                self.pieces.white_can_short_castle = False

        if self.pieces.white_can_long_castle:
            #WHITE LONG CASTLE
            if self.clicked_square == "e1" and self.destination_square == "c1":
                self.map["d1"] = self.map["a1"]
                self.map["a1"] = None   
            #CANCELING WHITE LONG CASTLE   
            if self.clicked_square == "a1" or self.map[self.clicked_square] == "white_king":
                self.pieces.white_can_long_castle = False

        #BLACK
        if self.pieces.black_can_short_castle:
            #BLACK SHORT CASTLE
            if self.clicked_square == "e8" and self.destination_square == "g8":
                self.map["f8"] = self.map["h8"]
                self.map["h8"] = None
            #CANCELING WHITE SHORT CASTLE
            if self.clicked_square == "h8" or self.map[self.clicked_square] == "black_king":
                self.pieces.black_can_short_castle = False

        if self.pieces.black_can_long_castle:
            #BLACK LONG CASTLE
            if self.clicked_square == "e8" and self.destination_square == "c8":
                self.map["d8"] = self.map["a8"]
                self.map["a8"] = None   
            #CANCELING BLACK LONG CASTLE   
            if self.clicked_square == "a8" or self.map[self.clicked_square] == "black_king":
                self.pieces.black_can_long_castle = False

        #MOVING PIECE
        self.map[self.destination_square] = self.map[self.clicked_square]
        self.map[self.clicked_square] = None

        if self.pieces.is_square_attacked("white", self.pieces.find_square("white_king", self.squares, self.map), self.squares, self.map):
            self.pieces.white_in_check = True
            if self.turn:
                print("Move not Allowed") 
                self.map[self.clicked_square] = self.clicked_piece
                self.map[self.destination_square] = self.destination_piece
                self.turn = -(self.turn - 1)
            else: print("check")
        else: self.pieces.white_in_check = False

        if self.pieces.is_square_attacked("black", self.pieces.find_square("black_king", self.squares, self.map), self.squares, self.map):
            self.pieces.black_in_check = True
            if not self.turn:
                print("Move not Allowed") 
                self.map[self.clicked_square] = self.clicked_piece
                self.map[self.destination_square] = self.destination_piece
                self.turn = -(self.turn - 1)
            else: print("check")
        else: self.pieces.black_in_check = False

        self.clicked_square = ""
        self.destination_square = ""
        self.potential_squares = ""

        return True

    def over_clicked(self, x, y):
        return self.clicked_square == self.squares[self.find_coord(x, y)]
    
    def render(self, surface):
        #COLOUR CHESS BOARD
        surface.fill(self.light)
        for i in range(8):
            if i % 2 == 0:
                for j in range(8):
                    if j % 2 != 0:
                        cell = pygame.Rect(i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(surface, self.dark, cell)
            else:
                for j in range(8):
                    if j % 2 == 0:
                        cell = pygame.Rect(i*self.cell_size, j*self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(surface, self.dark, cell)

        #COLOUR CLICKED PIECES SQUARES (DARK GREEN)
        #COLOUR POSSIBLE DESTINATION SQUARES (DARK BLUE)
        #COLOUR POSSIBLE CAPTURE SQUARES (DARK RED)
        count = 0
        for z in self.squares:
            x = (count % 8)   
            y = (count // 8)
            if z == self.clicked_square:
                box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                pygame.draw.rect(surface, "dark green", box)
            if self.potential_squares:
                if z in self.potential_squares:
                    box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(surface, "dark blue", box)
                else:
                    string = z + "!"
                    if string in self.potential_squares:
                        box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                        pygame.draw.rect(surface, "dark red", box)
            count += 1


        #COLOUR CHECKED KING (DARK RED)
        if self.pieces.is_square_attacked("white", self.pieces.find_square("white_king", self.squares, self.map), self.squares, self.map):
            count = 0
            for z in self.squares:
                x = (count % 8)   
                y = (count // 8)
                if self.map[z] == "white_king":
                    box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(surface, "dark red", box)
                count += 1

        if self.pieces.is_square_attacked("black", self.pieces.find_square("black_king", self.squares, self.map), self.squares, self.map):
            count = 0
            for z in self.squares:
                x = (count % 8)   
                y = (count // 8)
                if self.map[z] == "black_king":
                    box = pygame.Rect(x*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size)
                    pygame.draw.rect(surface, "dark red", box)
                count += 1

    def select_square(self, x, y):
        if self.map[self.squares[self.find_coord(x, y)]]:
            if self.turn and "white" in self.map[self.squares[self.find_coord(x, y)]]:
                self.clicked_square = self.squares[self.find_coord(x, y)]
                self.potential_squares = self.pieces.possible_squares(self.map[self.squares[self.find_coord(x, y)]][6:], "white", self.find_coord(x, y), self.squares, self.map)
            elif not self.turn and "black" in self.map[self.squares[self.find_coord(x, y)]]:
                self.clicked_square = self.squares[self.find_coord(x, y)]
                self.potential_squares = self.pieces.possible_squares(self.map[self.squares[self.find_coord(x, y)]][6:], "black", self.find_coord(x, y), self.squares, self.map)
        else:
            self.clicked_square = ""
            self.potential_squares = []

    def draw_lines(self, surface):
        length = 800
        width = 5
        #Horizontal
        for i in range(1, 8):
            x = 0
            y = (i * 100) - (width / 2)
            line = pygame.draw.line(surface, "black", (x, y), (length, y), width)
        #Vertical
        for i in range(1, 8):
            y = 0
            x = (i * 100) - (width / 2)
            line = pygame.draw.line(surface, "black", (x, y), (x, length), width)       