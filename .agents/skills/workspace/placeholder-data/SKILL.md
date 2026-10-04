---
name: placeholder-data
description: >-
  Replace a pasted API payload with plausible non-sensitive placeholders that keep
  its shape. Thin a repeated list to the items a reader still needs in order to
  read it the same way. Use when the user pastes an API response or payload and
  asks to sanitize, placeholder, or anonymize it for copy-paste.
short_description: 'Turn a pasted API payload into the same shape with plausible fake values.'
disable-model-invocation: true
---

# Placeholder Data

The user pastes a payload. The skill answers with the same shape filled with plausible placeholders.

## Workflow

1. If the paste is an HTTP message, keep its JSON body and discard the status line and headers.
2. Parse that body as JSON without writing the paste to a file or a log. When it does not parse, use the fallback in **Output**.
3. Rewrite the payload by judgment, using the rules below.
4. Pretty-print the result with a two-space indent and fill **Output**.

## Values

Keep every key, the nesting, and each value's kind. Do not add fields.

Keep `null`, booleans, and a short categorical token that does not identify anyone: one word or code, with no digits, that names a status, type, role, or unit, such as `active`, `usd`, or `admin`. Replace every other scalar. When a value might be sensitive, replace it.

A placeholder is a fictional value a person still reads the way they read the original. Match its kind, its visible format, and the distinctions inside it: how many parts it has, how those parts differ, their order, their case, and the scale a reader would guess. Values that stay next to each other keep the same relationships, so the record still reads as one plausible example. No identifying character from the original value survives in its stand-in, beyond the format's separators and a reserved fictional form. Decide from the value in front of you, not from its key, and not from a list of formats. A blank, a repeated character, a type label, or one stock word reused for every value of that kind fails this, whatever the value is. Where a format has a reserved fictional form, use it so the stand-in cannot be a real one. A value whose reading is none, such as zero, stays none.

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
  "full_name": "john smith",
  "ssn": "123-45-6789",
  "email": "john@example.com",
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
    {"line1": "1 Main St", "city": "Austin", "postal_code": "78701"},
    {"line1": "2 Oak Ave", "city": "Dallas", "postal_code": "75201"}
  ]
}
```

is answered with exactly:

```json
{
  "full_name": "alex morgan",
  "ssn": "901-23-4567",
  "email": "alex.morgan@example.com",
  "status": "active",
  "amount": 12.5,
  "note": "The crate arrived before noon.",
  "window": "2000-01-02/2000-06-15",
  "stops": [
    "2001-06-01/2001-06-20",
    "2001-03-01/2001-03-14",
    "2001-01-02/2001-01-09"
  ],
  "addresses": [
    {
      "line1": "18 Maple Street",
      "city": "Springfield",
      "postal_code": "12345"
    }
  ]
}
```
