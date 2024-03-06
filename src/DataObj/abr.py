#alpha, beta, gammaのデータ構造を持ち、柔軟に引き抜けるようにメンバを持つクラス

class Piece:
    def __init__(self, workdate, modality, needs):
        self.__workdate = workdate
        self.__modality = modality
        self.__needs = needs 

    @property
    def workdate(self):
        return self.__workdate

    @property
    def modality(self):
        return self.__modality

    @property
    def needs(self):
        return self.__needs
        
# kinds = {'da': 0, 'dm': 1, 'dc': 2, 'df': 3, 'na': 4, 'nm': 5, 'nc': 6, 'nn': 7, 'dw': 8, 'ew': 9, 'do': 10, 'ho': 11}
class ABR:
    def __init__(self, pieces, kinds):
        if all(isinstance(piece, Piece) for piece in pieces):
            self.__pieces = pieces
        else:
            raise TypeError("All elements in 'pieces' must be of type 'Piece'")
        if isinstance(kinds, dict):
            self.__kinds = kinds
        else:
            raise TypeError("The 'kinds' must be of type 'dict'")
    
    def get_daily_needs(self):
        split_with_kinds = [[] for i in range(len(self.__kinds.keys()))]
        for key in self.__kinds:
            for piece in self.__pieces:
                if piece.modality.lower() == key:
                    split_with_kinds[int(self.__kinds[key])].append(piece)
        return [[piece.needs for piece in sorted(element, key=lambda x:x.workdate)] for element in split_with_kinds]
