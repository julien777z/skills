## Naming

- **Name things with the everyday word a reader expects.** The reader is this codebase's: a name
  says what its product, its users and its existing code call the thing, never a word that is right
  only in another field, such as a botanical Latin name for a plant in a garden shop's catalog.
  Where the domain or a provider has a term this codebase's readers use, use it. A parcel the
  carrier reports as delivered is `delivered`, never `parcel_arrived`, because an unusual synonym
  makes every reader translate it back. This covers identifiers, fields, messages, documentation and
  test names in every language.
- Choose a concrete term when a generic category would leave readers guessing. Use the domain
  name that identifies the object, such as a customer or a server.
- **A name says what it is about, so a reader never opens the body to learn what it acts on or
  holds.** That holds for every name: a function, Boolean, field, event, constant, class, module,
  file or package. Use a qualifier when it communicates a role, state, input or output that
  readers need to distinguish. Keep labels for design decisions, implementation preferences,
  or migration phases in the design record when they add no such distinction. A name built on
  a verb names the verb's object: `job.writes_files`,
  `assert_may_book_rooms`, never `writes(job)` or `assert_may_book`, whose reader asks "writes
  what?", "book what?". A receiver or argument supplies the subject only when it is the very thing
  the name is about: `loan.is_overdue` and `is_deliverable(message)` need nothing more, but a check
  on whether a member may change a club's bookings takes the club and is about its bookings, so it is
  `may_change_bookings(member, club)`, never `may_change(member, club)`. A generic noun says what it
  holds unless its receiver already does: `shipment.status` is the shipment's own state, but the
  state of its customs check is `customs_status`; a parsed recipe in a local variable is `recipe`,
  never `result` or `data`; a constant is `MAX_GUESTS_PER_TABLE`, never `LIMIT`; and a module of
  date helpers is `dates.py`, never `helpers.py` or `misc.py`. The one generic container name is
  the category package a language rule assigns, such as `utils/`, whose topic-named modules carry
  what it holds. A name a framework or protocol defines keeps its own spelling.
- **Name things for what they are, never for the caller, surface or task that uses them.** A
  qualifier naming who reads or calls a thing, such as `librarian_`, `kiosk_` or `partner_`, reads
  as what the thing belongs to or what kind it is, and misleads most where the codebase already uses
  the word for one of its own entities: with `librarian` meaning a staff account, the full record of
  a branch's loans that librarians read is `list_loan_records`, never `list_librarian_loans`, which
  reads as loans librarians took out. A thing that is itself the surface, such as the router serving
  the kiosk pages, takes that surface's name. A test needing a table with a secret column names it
  for that — a record with a secret — rather than borrowing the one real table the change was made
  for.
