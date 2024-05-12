from spellbound.utils.exception import NotFoundException


class SpellBook:
    def __init__(self, spells=None):
        self.spells = {} if spells is None else spells

    def register(self, name, spell_class):
        """
        Register a new spell.

        Args:
            name (str): spell name
            spell_class (class): spell class to learn
        """
        self.spells[name] = spell_class

    def find(self, name):
        """
        Find a spell class by name.

        Args:
            name (str): spell name

        Returns:
            class: spell class
        """
        if name in self.spells:
            return self.spells[name]
        raise NotFoundException(f"This spellbook does not have Spell `{name}`.")

    def update(self, another_book):
        """
        Update the spells in this book with spells from another book.
        If a spell with the same name already exists, it will be overwritten.

        Args:
            another_book (SpellBook): another spell book

        Returns:
            SpellBook: this spell book
        """
        self.spells.update(another_book.spells)
        return self

    def to_list(self):
        """
        Return a list of all spells in this book.

        Returns:
            List[Tuple(name, spell_class)]: list of spells
        """
        return list(self.spells.items())

    def copy(self):
        """
        Copy this spell book.

        Returns:
            SpellBook: cloned spell book
        """
        return SpellBook(self.spells.copy())
