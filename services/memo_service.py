class MemoService:
    def __init__(self):
        self.memos = []

    def add_memo(self, memo):
        self.memos.append(memo)

    def delete_memo(self, index):
        if 0 <= index < len(self.memos):
            self.memos.pop(index)

    def get_memos(self):
        return self.memos