class MemoService:
    """
    Service class for managing memos.

    Provides methods to perform CRUD operations on memos stored in memory.
    """

    def __init__(self):
        """
        Initialize the MemoService.

        Initializes an empty memos list and sets the next ID to 1.
        """
        self.memos = []
        self.next_id = 1

    def get_memos(self):
        """
        Retrieve all memos.

        Returns:
            list: A list of all memo dictionaries.
        """
        return self.memos
    
    def get_memo(self, id):
        """
        Retrieve a single memo by ID.

        Args:
            id (int): The ID of the memo to retrieve.

        Returns:
            dict or None: The memo dictionary if found, None otherwise.
        """
        for memo in self.memos:
            if memo["id"] == id:
                return memo
        return None

    def add_memo(self, content):
        """
        Add a new memo.

        Creates a new memo with the provided content and appends it to the list.

        Args:
            content (str): The content of the memo.
        """
        memo = {"id": self.next_id, "content": content}
        self.memos.append(memo)
        self.next_id += 1

    def update_memo(self, id, content):
        """
        Update an existing memo.

        Updates the content of the memo with the specified ID.

        Args:
            id (int): The ID of the memo to update.
            content (str): The new content for the memo.
        """
        for memo in self.memos:
            if memo["id"] == id:
                memo["content"] = content

    def delete_memo(self, id):
        """
        Delete a memo by ID.

        Removes the memo with the specified ID from the list.

        Args:
            id (int): The ID of the memo to delete.
        """
        self.memos = [m for m in self.memos if m["id"] != id]

    