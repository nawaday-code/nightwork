import os

class TrustPath:
    def __init__(self, path):
        assert os.path.exists(path), "指定されたパスは存在しません"
        self.__path = path

    @property
    def value(self):
        return self.__path
    
    @classmethod
    def from_access_file(cls, path):
        assert path.endswith('.access'), "パスは.accessファイルを指定してください"
        return cls(path)

    @classmethod
    def from_csv_file(cls, path):
        assert path.endswith('.csv'), "パスは.csvファイルを指定してください"
        return cls(path)
    
    @classmethod
    def from_json_file(cls, path):
        assert path.endswith('.json'), "パスは.jsonファイルを指定してください"
        return cls(path)
