# Encrypted PDF Handling Flow

This document explains how PDF Toolkit handles encrypted PDFs
during merge operations.

The system uses:

- background worker threads
- GUI password prompts
- threading.Event synchronization

This design prevents the GUI from freezing while still allowing
the user to enter passwords when required.

---

This document explains how password-protected PDFs are handled during the merge process, using threading and dynamic GUI interactions in CustomTkinter.

It is especially useful for understanding how the password prompt synchronizes with the background merging task.


```md
┌────────────────────────────────────────┐
│         User clicks "Merge"            │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ run_task_with_progress(...)            │
│ - Shows ProgressBar modal              │
│ - Starts worker thread                 │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ [Background Thread]                    │
│ Calls merge_pdf(...)                   │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ For each input PDF:                    │
│   if encrypted:                        │
│     Call ask_password_callback(path)   │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ make_gui_password_callback() returns:  │
│   callback(file_path):                 │
│     → ask_password(...)                │
│     → wait for threading.Event()       │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ ask_password(...)                      │
│ - Shows password UI                    │
│ - Injects EncryptedPdfFrame            │
└────────────────────────────────────────┘
                   │
                   ▼
┌────────────────────────────────────────┐
│ User sees prompt:                      │
│  ┌────────────┐ ┌──────┐ ┌────────────┐│
│  │ Submit     │ │ Skip │ │ Skip All   ││
│  └────────────┘ └──────┘ └────────────┘│
└────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
  User enters pwd        User skips
        │                     │
        ▼                     ▼
EncryptedPdfFrame.submit()    EncryptedPdfFrame.skip() / skip_all()
        │                     │
        ▼                     ▼
Calls self.on_complete(("password", pwd)) or skip variant
        │
        ▼
handle_response() in ask_password()
- Updates global flags if skipped
- Calls on_result(password or None)
        │
        ▼
on_password_result() sets:
- password_container["value"]
- event.set()
        │
        ▼
Background thread resumes after event.wait()
- password returned from callback
        │
        ▼
merge_pdf() continues:
- Tries decrypting PDF with password
- Appends to merger if successful
        │
        ▼
Next file OR finish merge
        │
        ▼
ProgressBar is closed
on_done(result) called
Final result shown to user
```

---

## Legend

| Symbol     | Meaning                      |
| ---------- | ---------------------------- |
| │ / ▼ / └  | Flow direction               |
| [Brackets] | Thread/process description   |
| Boxes      | Logical steps or UI elements |

---

## 🧠 Key Takeaways

- **Two threads**: UI (main) and merging (background).
- **Password prompt is GUI-driven**, but password is passed back to the worker thread through an `Event`.
- **User actions (submit, skip)** directly affect the control flow using callback mechanics.
- The system **pauses safely** while waiting for user input — without freezing the UI.

---

## Flow summary diagram

```text
Main GUI Thread                         Worker Thread
-----------------                      --------------------
merge_pdf_gui() ->
│
├── run_task_with_progress()
│    ├── ProgressBar shown
│    └── Thread started (worker)
│
└── [ UI event loop continues ]

                                       └─> merge_pdf()
                                              │
                                              └─> detect ENCRYPTED PDF
                                                  │
                                                  └─> password = ask_password_callback(file)
                                                       │
                                                       └─> ask_password()
                                                            └─> show_password_prompt() on GUI
                                                                 (uses EncryptedPdfFrame)

[User types password or skips] ⟶ EncryptedPdfFrame triggers on_complete(("password", pwd))
                                                 ↓
                                            handle_response() in ask_password
                                                 ↓
                                            on_result(password)
                                                 ↓
                                       on_password_result(password)
                                                 ↓
                                            event.set()
                                                 ↓
                                       callback() resumes and returns password
                                                 ↓
                                merge_pdf() uses password and continues

```
