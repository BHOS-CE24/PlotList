import random



class LLNode:
    def __init__(self, item):
        self.item = item
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, item):
        new_node = LLNode(item)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def contains(self, title):
        current = self.head
        while current:
            if current.item.title.lower() == title.lower():
                return True
            current = current.next
        return False

    def display(self):
        current = self.head
        if current is None:
            print("Favourites list is empty.")
            return
        print("\nFavourites:")
        while current:
            print(f"  {current.item}")
            current = current.next



class StackNode:
    def __init__(self, data):
        self.data = data
        self.next = None

class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        node = StackNode(data)
        node.next = self.top
        self.top = node

    def pop(self):
        if self.is_empty():
            return None
        data = self.top.data
        self.top = self.top.next
        return data

    def is_empty(self):
        return self.top is None


class Item:
    def __init__(self, title, item_type, rating):
        self.title = title
        self.item_type = item_type
        self.rating = rating

    def __str__(self):
        return f"{self.title} ({self.item_type}) - {self.rating}/10"


class GenreNode:
    def __init__(self, genre):
        self.genre = genre
        self.items = []
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None
        self.favourites = LinkedList()
        self.undo_stack = Stack()
        self.redo_stack = Stack()

    def _snapshot(self):
        nodes = []
        self._inorder(self.root, nodes)
        snapshot = []
        for node in nodes:
            for item in node.items:
                snapshot.append((node.genre, item.title, item.item_type, item.rating))
        return snapshot

    def _restore(self, snapshot):
        self.root = None
        for genre, title, item_type, rating in snapshot:
            self.root = self._insert(self.root, genre)
            node = self._search(self.root, genre)
            node.items.append(Item(title, item_type, rating))

    def _insert(self, node, genre):
        if node is None:
            return GenreNode(genre)
        if genre < node.genre:
            node.left = self._insert(node.left, genre)
        elif genre > node.genre:
            node.right = self._insert(node.right, genre)
        return node

    def _search(self, node, genre):
        if node is None:
            return None
        if genre == node.genre:
            return node
        if genre < node.genre:
            return self._search(node.left, genre)
        return self._search(node.right, genre)

    def _inorder(self, node, result):
        if node is None:
            return
        self._inorder(node.left, result)
        result.append(node)
        self._inorder(node.right, result)

    def _min_node(self, node):
        while node.left:
            node = node.left
        return node

    def _delete_genre_node(self, node, genre):
        if node is None:
            return None
        if genre < node.genre:
            node.left = self._delete_genre_node(node.left, genre)
        elif genre > node.genre:
            node.right = self._delete_genre_node(node.right, genre)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            successor = self._min_node(node.right)
            node.genre = successor.genre
            node.items = successor.items
            node.right = self._delete_genre_node(node.right, successor.genre)
        return node

    def add_item(self, genre, title, item_type, rating):
        self.undo_stack.push(self._snapshot())
        self.redo_stack = Stack()
        self.root = self._insert(self.root, genre)
        node = self._search(self.root, genre)
        node.items.append(Item(title, item_type, rating))
        print(f'Added "{title}" to {genre}.')

    def delete_item(self, genre, title):
        node = self._search(self.root, genre)
        if node is None:
            print("Genre not found.")
            return
        for item in node.items:
            if item.title.lower() == title.lower():
                self.undo_stack.push(self._snapshot())
                self.redo_stack = Stack()
                node.items.remove(item)
                print(f'Deleted "{item.title}".')
                if not node.items:
                    self.root = self._delete_genre_node(self.root, genre)
                return
        print("Title not found.")

    def rate_item(self, genre, title, new_rating):
        node = self._search(self.root, genre)
        if node is None:
            print("Genre not found.")
            return
        for item in node.items:
            if item.title.lower() == title.lower():
                item.rating = new_rating
                print(f'Updated "{item.title}" to {new_rating}/10.')
                return
        print("Title not found.")

    def search_genre(self, genre):
        node = self._search(self.root, genre)
        if node is None:
            print("Genre not found.")
            return
        print(f'\n{genre}:')
        for item in node.items:
            print(f'  {item}')

    def binary_search(self, title):
        nodes = []
        self._inorder(self.root, nodes)
        all_items = []
        for node in nodes:
            for item in node.items:
                all_items.append((node.genre, item))

        all_items.sort(key=lambda x: x[1].title.lower())

        low, high = 0, len(all_items) - 1
        while low <= high:
            mid = (low + high) // 2
            mid_title = all_items[mid][1].title.lower()
            if mid_title == title.lower():
                genre, item = all_items[mid]
                print(f'Found: [{genre}] {item}')
                return
            elif mid_title < title.lower():
                low = mid + 1
            else:
                high = mid - 1
        print("Not found.")

    def show_all(self):
        if self.root is None:
            print("Nothing here yet.")
            return
        nodes = []
        self._inorder(self.root, nodes)
        for node in nodes:
            print(f'\n{node.genre}:')
            for item in node.items:
                print(f'  {item}')

    def sort_by_rating(self):
        nodes = []
        self._inorder(self.root, nodes)
        all_items = []
        for node in nodes:
            for item in node.items:
                all_items.append((node.genre, item))

        n = len(all_items)
        for i in range(n):
            for j in range(0, n - i - 1):
                if all_items[j][1].rating < all_items[j + 1][1].rating:
                    all_items[j], all_items[j + 1] = all_items[j + 1], all_items[j]

        print("\nSorted by rating:")
        for genre, item in all_items:
            print(f'  [{genre}] {item}')

    def show_top_rated(self, min_rating=8):
        if self.root is None:
            print("Nothing here yet.")
            return
        nodes = []
        self._inorder(self.root, nodes)
        top = [(n.genre, item) for n in nodes for item in n.items if item.rating >= min_rating]
        if not top:
            print(f"No items with rating >= {min_rating}.")
            return
        top.sort(key=lambda x: x[1].rating, reverse=True)
        print(f'\nTop rated (>= {min_rating}/10):')
        for genre, item in top:
            print(f'  [{genre}] {item}')

    def add_to_favourites(self, genre, title):
        node = self._search(self.root, genre)
        if node is None:
            print("Genre not found.")
            return
        for item in node.items:
            if item.title.lower() == title.lower():
                if self.favourites.contains(title):
                    print("Already in favourites.")
                    return
                self.favourites.append(item)
                print(f'Added "{item.title}" to favourites.')
                return
        print("Title not found.")

    def show_favourites(self):
        self.favourites.display()

    def recommend(self, genre):
        node = self._search(self.root, genre)
        if node is None:
            print("Genre not found.")
            return
        pick = random.choice(node.items)
        print(f'How about: {pick}')

    def undo(self):
        if self.undo_stack.is_empty():
            print("Nothing to undo.")
            return
        self.redo_stack.push(self._snapshot())
        self._restore(self.undo_stack.pop())
        print("Undone.")

    def redo(self):
        if self.redo_stack.is_empty():
            print("Nothing to redo.")
            return
        self.undo_stack.push(self._snapshot())
        self._restore(self.redo_stack.pop())
        print("Redone.")


def get_valid_rating():
    while True:
        try:
            r = int(input("Rating (1-10): "))
            if 1 <= r <= 10:
                return r
            print("Enter a number between 1 and 10.")
        except ValueError:
            print("Numbers only.")


def main():
    bst = BST()

    bst.add_item("Sci-Fi", "Inception", "movie", 9)
    bst.add_item("Drama", "The Shawshank Redemption", "movie", 10)
    bst.add_item("Sci-Fi", "Dune", "book", 8)
    bst.add_item("Fantasy", "The Hobbit", "book", 9)
    bst.add_item("Drama", "1984", "book", 7)
    bst.add_item("Action", "Mad Max: Fury Road", "movie", 8)

    while True:
        print("\n1. Add item")
        print("2. Delete item")
        print("3. Update rating")
        print("4. Show all")
        print("5. Search by genre")
        print("6. Search by title")
        print("7. Sort by rating")
        print("8. Top rated")
        print("9. Add to favourites")
        print("10. Show favourites")
        print("11. Get a recommendation")
        print("12. Undo")
        print("13. Redo")
        print("14. Exit")

        choice = input("\n> ").strip()

        if choice == "1":
            title = input("Title: ").strip()
            genre = input("Genre: ").strip()
            item_type = input("movie or book: ").strip().lower()
            if item_type not in ("movie", "book"):
                print('Type "movie" or "book".')
                continue
            rating = get_valid_rating()
            bst.add_item(genre, title, item_type, rating)

        elif choice == "2":
            genre = input("Genre: ").strip()
            title = input("Title: ").strip()
            bst.delete_item(genre, title)

        elif choice == "3":
            genre = input("Genre: ").strip()
            title = input("Title: ").strip()
            rating = get_valid_rating()
            bst.rate_item(genre, title, rating)

        elif choice == "4":
            bst.show_all()

        elif choice == "5":
            genre = input("Genre: ").strip()
            bst.search_genre(genre)

        elif choice == "6":
            title = input("Title: ").strip()
            bst.binary_search(title)

        elif choice == "7":
            bst.sort_by_rating()

        elif choice == "8":
            try:
                min_r = int(input("Minimum rating (default 8): ").strip() or "8")
            except ValueError:
                min_r = 8
            bst.show_top_rated(min_r)

        elif choice == "9":
            genre = input("Genre: ").strip()
            title = input("Title: ").strip()
            bst.add_to_favourites(genre, title)

        elif choice == "10":
            bst.show_favourites()

        elif choice == "11":
            genre = input("Genre: ").strip()
            bst.recommend(genre)

        elif choice == "12":
            bst.undo()

        elif choice == "13":
            bst.redo()

        elif choice == "14":
            print("Bye.")
            break

        else:
            print("Pick a number from 1 to 14.")


main()