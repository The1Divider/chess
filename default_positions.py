# dummy aliases
WHITE, BLACK = "", ""
def dummy(x): pass


r = n = b = q = k = p = dummy


class Dummy:
    def __init__(self):
        self.w_king, self.b_king = None, None
        starting_board_with_pieces = {
            "a8": r(BLACK), "b8": n(BLACK), "c8": b(BLACK), "d8": q(BLACK), "e8": self.b_king, "f8": b(BLACK),
            "g8": n(BLACK), "h8": r(BLACK),
            "a7": p(BLACK), "b7": p(BLACK), "c7": p(BLACK), "d7": p(BLACK), "e7": p(BLACK), "f7": p(BLACK),
            "g7": p(BLACK), "h7": p(BLACK),
            "a6": None, "b6": None, "c6": None, "d6": None, "e6": None, "f6": None, "g6": None, "h6": None,
            "a5": None, "b5": None, "c5": None, "d5": None, "e5": None, "f5": None, "g5": None, "h5": None,
            "a4": None, "b4": None, "c4": None, "d4": None, "e4": None, "f4": None, "g4": None, "h4": None,
            "a3": None, "b3": None, "c3": None, "d3": None, "e3": None, "f3": None, "g3": None, "h3": None,
            "a2": p(WHITE), "b2": p(WHITE), "c2": p(WHITE), "d2": p(WHITE), "e2": p(WHITE), "f2": p(WHITE),
            "g2": p(WHITE), "h2": p(WHITE),
            "a1": r(WHITE), "b1": n(WHITE), "c1": b(WHITE), "d1": q(WHITE), "e1": self.w_king, "f1": b(WHITE),
            "g1": n(WHITE), "h1": r(WHITE)}


starting_board = {
    "a8": "p", "b8": "p", "c8": "p", "d8": "p", "e8": "p", "f8": "p", "g8": "p", "h8": "p",
    "a7": "p", "b7": "p", "c7": "p", "d7": "p", "e7": "p", "f7": "p", "g7": "p", "h7": "p",
    "a6": None, "b6": None, "c6": None, "d6": None, "e6": None, "f6": None, "g6": None, "h6": None,
    "a5": None, "b5": None, "c5": None, "d5": None, "e5": None, "f5": None, "g5": None, "h5": None,
    "a4": None, "b4": None, "c4": None, "d4": None, "e4": None, "f4": None, "g4": None, "h4": None,
    "a3": None, "b3": None, "c3": None, "d3": None, "e3": None, "f3": None, "g3": None, "h3": None,
    "a2": "p", "b2": "p", "c2": "p", "d2": "p", "e2": "p", "f2": "p", "g2": "p", "h2": "p",
    "a1": "p", "b1": "p", "c1": "p", "d1": "p", "e1": "p", "f1": "p", "g1": "p", "h1": "p"}

starting_fen = None

starting_png = None



