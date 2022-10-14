from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime
import functools

Base = declarative_base()


class Notebook(Base):
    """Represent a collection of notes that can be tagged,
    modified, and searched."""

    __tablename__ = "notebook"

    _id = Column(Integer, primary_key=True)
    # backref is unnecessary, but useful for the example
    _notes = relationship("Note", backref=backref("notebook")) 



    # def __init__(self):
    #     """Initialize a notebook with an empty list."""
    #     self._notes = []

    def new_note(self, memo, session, tags=""):
        """Create a new note and add it to the list."""
        n = Note(memo, tags)
        self._notes.append(n) # sqlalchemy initialized the list for us
        session.add(n)


    def _find_note(self, note_id):
        """Locate the note with the given id."""
        for note in self._notes:
            if note.id_matches(note_id):
                return note
        return None

    def modify_memo(self, note_id, memo, session):
        """Find the note with the given id and change its
        memo to the given value."""
        note = self._find_note(note_id)
        if note:
            note.update_memo(memo)
            session.add(note)
            return True
        return False

    def modify_tags(self, note_id, tags, session):
        """Find the note with the given id and change its
        tags to the given value."""
        note = self._find_note(note_id)
        if note:
            note.update_tags(tags)
            session.add(note)
            return True
        return False

    def search(self, filter):
        """Find all notes that match the given filter
        string."""
        
        # Can update this to be a sql query
        return [note for note in self._notes if note.match(filter)]

    def all_notes(self):
        """Returns all notes in the notebook"""

        # could be sorted as below, or organized some other way
        return sorted(self._notes)




@functools.total_ordering
class Note(Base):
    """Represent a note in the notebook. Match against a
    string in searches and store tags for each note."""

    __tablename__ = "note"

    _id = Column(Integer, primary_key=True)
    _notebook_id = Column(Integer, ForeignKey("notebook._id"))
    _memo = Column(String)
    _tags = Column(String)
    _creation_date = Column(DateTime)
    
    # last_id = 0

    def __init__(self, memo, tags=""):
        """initialize a note with memo and optional
        space-separated tags. Automatically set the note's
        creation date and a unique id."""

        self._memo = memo
        self._tags = tags
        self._creation_date = datetime.today()

        # Note.last_id += 1
        # self._id = Note.last_id


    def match(self, filter):
        """Determine if this note matches the filter
        text. Return True if it matches, False otherwise.

        Search is case sensitive and matches both text and
        tags."""

        return filter in self._memo or filter in self._tags

    def id_matches(self, id):
        """
        Determine if this note has the given id
        """
        return self._id == int(id)

    def update_memo(self, memo):
        self._memo = memo

    def update_tags(self, tags):
        self._tags = tags

    def __str__(self):
        # this doesn't belong here. it's just to demonstrate the backref
        print(self.notebook)
        return f"{self._id}: {self._memo}\n{self._tags}"

    def __lt__(self, other):
        return self._id < other._id

    def __eq__(self, other):
        return self._id == other._id


if __name__ == "__main__":
    # if the db file already exists, this does nothing
    engine = create_engine(f"sqlite:///notebook.db")
    Base.metadata.create_all(engine)




# class MyTime(TypeDecorator):
#     impl = String

#     def __init__(self, length=None, format="%Y-%m-%d", **kwargs):
#         super().__init__(length, **kwargs)
#         self.format = format

#     def process_literal_param(self, value, dialect):
#         # allow passing string or time to column
#         if isinstance(value, str):
#             value = datetime.strptime(value, self.format).time()

#         # convert python time to sql string
#         return value.strftime(self.format) if value is not None else None

#     process_bind_param = process_literal_param

#     def process_result_value(self, value, dialect):
#         # convert sql string to python time
#         return datetime.strptime(value, self.format).date() if value is not None else None
