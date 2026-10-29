# knowledgebooks

A public repository of books that build knowledge, maintained by the
[Center for Educational Progress](https://educationprogress.org).

This repository is the source of truth for the reading list for developing
readers. The CEP website reads these files and renders them as the published
list; nothing else in the website repository defines a book.

## Layout

| Path | What it holds |
| --- | --- |
| `books/<slug>.md` | One book per file. Front matter only — the body is unused. |
| `books-vocabulary.json` | Every allowed value and its exact wording. The one file the suggestion form, the publishing script and the website all read. |
| `check-books.py` | Validates every book against the vocabulary. Run it before opening a pull request: `python3 check-books.py` |
| `archive/books/` | Books drafted for an earlier version of the list. Not published and not checked; kept to draw on later. |

## A book file

```markdown
---
title: "March: Book One"
author: "John Lewis, Andrew Aydin and Nate Powell"
year: 2013
category: young-adult
domain: [history, civics, biography]
format: graphic-novel
form: nonfiction
use: [independent, class-set]
appeal: [classrooms]
review: "John Lewis's own account of the civil rights movement, in comics. Nonviolent resistance as a trained discipline."
reviewer_role: educator
---
```

`category`, `domain`, `format`, `form`, `use`, `appeal` and `reviewer_role`
must use values that appear in `books-vocabulary.json`. `format`, `appeal`,
`series`, `year` and `draft` are optional. A file with `draft: true` is kept
out of the published list.

Every New adult book shows "May include sexual content". Set
`sexual_content: false` on a New adult book that has none to hide that label;
the book stays in New adult.

Ages are not stored per book. They come from the book's `category`, which
carries the age range in `books-vocabulary.json`.

## How books get here

A suggestion is made on a Google Form, reviewed by CEP in a Google Sheet, and
written to this repository by an Apps Script when it is approved. The script
and its runbook live in the website repository under
`scripts/reading-list/`.

Changing a choice's wording in `books-vocabulary.json` means changing the
matching wording in the form, or submissions using that choice stop being
recognised.

Because the Apps Script writes here without a human reading the result,
`check-books.py` runs on every push (`.github/workflows/books-check.yml`) and
fails the build on any entry that breaks the vocabulary.

## The archive

`archive/books/` holds the 198 books drafted before launch. The launch list
was chosen separately and came in through the Google Form like any other
suggestion. Nothing reads the archive: the website, the form's duplicate
check and `check-books.py` look only at `books/`.

To bring an archived book back, suggest it through the form rather than moving
the file. The form adds the ISBN, the Amazon link and a review, and it
records who approved the book. Archived files may use vocabulary values that
have since changed, so treat them as notes, not finished entries.

## Licence

Released under [CC0 1.0](LICENSE): no rights reserved. The book titles,
authors and cover content remain the property of their respective owners.
