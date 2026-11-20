# Product Copy

What text and forms a product's reader meets follow. `SKILL.md` names this file at the point a
change writes or changes them.

## Forms

- Sections that require user input start expanded. If input in a section becomes required during
  the flow, expand the section when that requirement takes effect.

## Copy

- **Every line of product text changes what the reader does or understands; anything else is
  cut.** A label that restates what a control, price or heading already shows, or reassures the
  reader about a cost they are not paying, such as "Sharing is free" beside a paid plan's share
  button, adds reading without information and can make the reader doubt what they paid for. Before
  adding a line, name what it helps the reader do or understand; when there is nothing, leave it out.
- **Text a person reads sends them to another place with a link, never a route to follow.** "Open
  Library, then Shared albums" makes the reader follow a map; the place's name, linked, takes them
  there in one action. Where the text renders markup, the name is the link. Where it is plain text
  its reader can copy or follow, such as an API or tool message, an email body or a command's
  output, it carries the place's absolute URL. A surface that cannot hold a link, such as a toast,
  refers to no other place, and the way forward goes on the page itself. Text about a
  control on the same page names that control where the reader sees it, as in "Turn on Sync
  above", and never links to the page it sits on. It names the thing the control acts on, never
  quotes a label that is already an instruction into a sentence that gives its own: a switch
  labeled "Enable offline mode" is "Turn on offline mode", never "Turn on Enable offline mode".
- **A refusal an end user reads is a short, friendly request for their next step**, such as "This
  library card cannot be used. Please use a different card." It says what to do rather than passing
  a verdict on what was done or on the reader, as "You can't use this library card." does, and it
  never repeats back what the reader just entered or chose — a file name, a typed value, a picked
  item — which they already know. It holds wherever that message is written: the error message of
  an API or tool whose text reaches an end user, a server-side enum or constant that holds the
  text, a test fixture, and wording a brief proposes to a worker.
- **Text an end user reads speaks in what the reader cares about, never in the system's exact
  values or its inner workings.** Where a precise number, state or count changes nothing the reader
  does, say it in plain words: a fuel tank holding a few drops is "empty", a wait of 59 seconds is
  "a minute". Keep the exact value only where the reader acts on it, such as a price, a quantity
  they choose or a figure they compare, and never add a qualifier such as "almost" or "about" only
  to make plain words technically exact. The cause behind a failure or a wait stays out of it too
  when the cause is the system's own: a version, an update or release, a deployment or rollback, a
  migration or maintenance, a rate limit, a lock, a queue, a service or component name, an internal
  state or an error code. A booking that cannot be saved while a service restarts reads "We couldn't
  save your booking right now. Please try again in a few minutes.", never "The booking service is
  restarting" or "Error 503 from the calendar API". It holds wherever end-user text is written, as
  the refusal bullet above lists, and in a status label, a toast or an empty state; the full cause
  goes to the log and to text only the product's team reads.
- **Text only the product's own team reads states the observed condition and its values, and
  nothing more.** On an internal panel, an operator or support tool, or an internal API, a refusal
  or a report names what was found and lists the values it concerns, such as "Unrecognized shelf
  codes: B7, Q2". It assumes no cause, such as "the shelf list is out of date", and asks nothing of
  anyone, such as "Please ask the catalog team to correct the shelf list": its reader is the one
  who investigates, and a guessed cause or errand sends them the wrong way. It uses plain terms, such
  as player, account or item, never the product's in-world words for them, apart from a proper name
  such as its currency.
