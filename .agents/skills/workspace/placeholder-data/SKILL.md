---
name: placeholder-data
description: >-
  Replace a pasted API payload with obviously fake placeholders that keep
  its shape. Thin a repeated list to the items a reader still needs in order to
  read it the same way. Use when the user pastes an API response or payload and
  asks to sanitize, placeholder, or anonymize it for copy-paste.
short_description: 'Turn a pasted API payload into the same shape with obviously fake values.'
disable-model-invocation: true
---

# Placeholder Data

The user pastes a payload. The skill answers with the same shape filled with obvious placeholders.

## Workflow

1. If the paste is an HTTP message, keep its JSON body and discard the status line and headers.
2. Parse that body as JSON without writing the paste to a file or a log. When it does not parse, use the fallback in **Output**.
3. Rewrite the payload by judgment, using the rules below.
4. Pretty-print the result with a two-space indent and fill **Output**.

## Values

Keep every key, the nesting, and each value's kind. Do not add fields.

Keep `null`, booleans, and a short categorical token that does not identify anyone: one word or code, with no digits, that names a status, type, role, or unit, such as `active`, `usd`, or `admin`. Replace every other scalar. When a value might be sensitive, replace it.

A placeholder is an obvious stand-in a person still reads the way they read the original. Match its kind, its visible format, and the distinctions inside it: how many parts it has, how those parts differ, their order, their case, and the scale a reader would guess. Values that stay next to each other keep the same relationships. No identifying character from the original value survives in its stand-in, beyond the format's separators. Decide from the value in front of you, not from its key, and not from a list of formats.

Prefer a stand-in the reader already recognizes as a placeholder. A realistic substitute carries the same reading and can be mistaken for a real record, so it loses. A conventional placeholder — a stock placeholder name, place, or number, or a host reserved for examples — beats a generic test label too, when both carry that reading. Use a generic test label only when no conventional placeholder carries it, as with a sentence. A blank, all zeros, or a type label fails, because it drops the reading. Distinctions still show: an extra name part stays an extra part, a decimal stays a decimal, and a range's ends still differ. A value whose reading is none, such as zero, stays none.

When an object's keys are themselves data, such as emails or ids, replace those keys and thin the entries as **Repetition** says.

## Repetition

Keep enough items that a person still reads the list the way they read the original. Use judgment on this payload. One item is enough when the others only repeat it. When the list itself carries a reading — an order, a progression, a mix, or that each item is a span — keep a few, two or three, that still show that reading, in the same order, and no more. The same shape is only a clue: items can share a shape and still say different things. Nested lists are judged the same way.

## Output

The entire reply is this block, filled with the rewritten payload. No heading, no prose, and no second block.

````
```json
<pretty-printed payload>
```
````

A payload that does not parse gets this line and nothing else:

```text
Paste the body as JSON.
```

This input:

```json
{
  "full_name": "maria l lopez",
  "ssn": "234-56-7890",
  "email": "maria.lopez@example.com",
  "status": "active",
  "amount": 5.0,
  "note": "Left the package by the side door.",
  "window": "2024-03-01/2024-06-15",
  "stops": [
    "2024-06-01/2024-06-20",
    "2024-03-01/2024-03-14",
    "2024-01-02/2024-01-09",
    "2023-11-01/2023-11-12"
  ],
  "addresses": [
    {"line1": "458 Pine Road", "city": "Austin", "postal_code": "78609"},
    {"line1": "458 Pine Rd", "city": "Austin", "postal_code": "78609"}
  ]
}
```

is answered with exactly:

```json
{
  "full_name": "john a smith",
  "ssn": "111-11-1111",
  "email": "john.smith@example.com",
  "status": "active",
  "amount": 11.1,
  "note": "This is a test note.",
  "window": "2000-02-03/2000-07-08",
  "stops": [
    "2001-04-05/2001-04-18",
    "2001-03-06/2001-03-19",
    "2001-02-07/2001-02-14"
  ],
  "addresses": [
    {
      "line1": "123 Main Street",
      "city": "Anytown",
      "postal_code": "12345"
    }
  ]
}
```
