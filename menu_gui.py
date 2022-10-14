import tkinter as tk
import pickle
from notebook import Notebook


class Menu:
    """Display a menu and respond to choices when run."""

    def __init__(self):

        self._window = tk.Tk()
        self._window.title("MY NOTEBOOK")

        self._notebook = Notebook()
        self._options_frame = tk.Frame(self._window)

        tk.Button(self._options_frame,
                  text="Show all Notes",
                  command=self._show_notes).grid(row=1, column=1)
        tk.Button(self._options_frame,
                  text="Search Notes",
                  command=self._search_notes).grid(row=1, column=3)
        tk.Button(self._options_frame,
                  text="Add Note",
                  command=self._add_note).grid(row=1, column=4)
        tk.Button(self._options_frame,
                  text="Save",
                  command=self._save).grid(row=1, column=5)
        tk.Button(self._options_frame,
                  text="Load",
                  command=self._load).grid(row=1, column=6)

        self._list_frame = tk.Frame(self._window)
        self._options_frame.grid(row=0, column=1, columnspan=2)
        self._entry_frame = tk.Frame(self._window)
        self._entry_frame.grid(row=1, column=1)
        self._list_frame.grid(row=2, column=1, columnspan=1, sticky="w")

        self._notes_strvars = {}

        self._window.mainloop()

    def _show_notes(self, notes=None):
        if notes is None:
            notes = self._notebook.all_notes()
        # re-uses existing widgets
        row = 0
        for x in notes:
            if x._id not in self._notes_strvars:
                # sets up a dictionary of StringVars associated with the buttons created
                self._notes_strvars[x._id] = tk.StringVar(value=str(x))
                tk.Button(self._list_frame, text=x, textvariable=self._notes_strvars[x._id], command=Menu.ModifyNoteHandler(
                    x, self)).grid(row=row, column=1)
            else:
                # reuse the old button, but set the StringVar to change its label
                self._notes_strvars[x._id].set(str(x))
            row += 1

        # #another way to do this would be to delete all of the buttons and recreate a new set with the the proper text
        # for x in self._list_frame.winfo_children():
        #     #get all the widgets in the frame and destroy them
        #     x.destroy()
        # row = 0
        # for x in notes:
        #     tk.Button(self._list_frame, text=x, command=Menu.ModifyNoteHandler(x)).grid(row=row, column=1)
        #     row += 1

    def _search_notes(self):
        filter = input("Search for: ")
        notes = self._notebook.search(filter)
        self._show_notes(notes)

    def _add_note(self):
        def add_callback():
            self._notebook.new_note(e1.get())
            e1.destroy()
            b.destroy()
            l1.destroy()
            self._show_notes()

        l1 = tk.Label(self._options_frame, text="Memo:")
        l1.grid(row=2, column=1)
        e1 = tk.Entry(self._options_frame)
        e1.grid(row=3, column=1)

        b = tk.Button(self._options_frame, text="Enter", command=add_callback)
        b.grid(row=3, column=2)

    def _modify_note(self, note):
        def modify_callback():
            note.update_memo(memo_entry.get())
            note.update_tags(tags_entry.get())
            memo_label.destroy()
            memo_entry.destroy()
            tags_entry.destroy()
            tags_label.destroy()
            enter_button.destroy()
            self._show_notes()

        memo_label = tk.Label(self._entry_frame, text="Memo:")
        memo_label.grid(row=1, column=1)
        memo_entry = tk.Entry(self._entry_frame)
        memo_entry.grid(row=2, column=1)

        tags_label = tk.Label(self._entry_frame, text="Tags:")
        tags_label.grid(row=1, column=2)
        tags_entry = tk.Entry(self._entry_frame)
        tags_entry.grid(row=2, column=2)

        enter_button = tk.Button(
            self._entry_frame, text="Enter", command=modify_callback)
        enter_button.grid(row=2, column=3)

    class ModifyNoteHandler:
        def __init__(self, note, menu):
            self._note = note
            self._menu = menu

        def __call__(self):
            self._menu._modify_note(self._note)

    def _save(self):
        with open("notebook_save.pickle", "wb") as f:
            pickle.dump(self._notebook, f)

    def _load(self):
        with open("notebook_save.pickle", "rb") as f:
            self._notebook = pickle.load(f)


if __name__ == "__main__":
    Menu()



