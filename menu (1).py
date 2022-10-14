import sys

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker
from notebook import Notebook, Base


class Menu:
    """Display a menu and respond to choices when run."""

    def __init__(self):
        self._session = Session()
        #get notebook from db
        self._notebook = self._session.query(Notebook).first()
        if not self._notebook:
            self._notebook = Notebook()
            self._session.add(self._notebook)
            self._session.commit()
        self._choices = {
            "1": self._show_notes,
            "2": self._search_notes,
            "3": self._add_note,
            "4": self._modify_note,
            "5": self._quit,
        }

    def display_menu(self):
        print(
            """
Notebook Menu

1. Show all Notes
2. Search Notes
3. Add Note
4. Modify Note
5. Quit
"""
        )


    def run(self):
        """Display the menu and respond to choices."""
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))

    def _show_notes(self, notes=None):
        if not notes:
            notes = self._notebook.all_notes()
        for note in notes:
            print(str(note))

    def _search_notes(self):
        filter = input("Search for: ")
        notes = self._notebook.search(filter)
        self._show_notes(notes)

    def _add_note(self):
        memo = input("Enter a memo: ")
        self._notebook.new_note(memo, self._session)
        print("Your note has been added.")
        self._session.commit()

    def _modify_note(self):
        id = input("Enter a note id: ")
        memo = input("Enter a memo: ")
        tags = input("Enter tags: ")
        if memo:
            self._notebook.modify_memo(id, memo, self._session)
        if tags:
            self._notebook.modify_tags(id, tags, self._session)
        self._session.commit()



    def _quit(self):
        print("Thank you for using your notebook today.")
        sys.exit(0)


if __name__ == "__main__":
    engine = sqlalchemy.create_engine("sqlite:///notebook.db")

    # Only needs to happen once. If the tables already exist this does nothing.
    # If you change your schema (table names, column names, relationships) then
    # you must rebuild the database
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)
    
    Menu().run()