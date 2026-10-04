---
name: placeholder-data
description: >-
  Replace a pasted API payload with obvious non-sensitive placeholders that keep
  its shape, and drop repeated items that share a shape. Use when the user pastes
  an API response or payload and asks to sanitize, placeholder, or anonymize it
  for copy-paste.
short_description: 'Turn a pasted API payload into the same shape with obvious fake values.'
disable-model-invocation: true
---

# Placeholder Data

The user pastes a payload. The skill answers with the same shape filled with obvious placeholders.

## Workflow

1. If the paste is an HTTP message, keep its JSON body and discard the status line and headers.
2. Parse that body as JSON without writing the paste to a file or a log. When it does not parse, use the fallback in **Output**.
3. Rewrite scalars, then collapse arrays, using the rules below.
4. Pretty-print the result with a two-space indent and fill **Output**.

## Values

Keep every key, the nesting, and each value's kind. Do not add fields.

Keep `null`, booleans, and a short categorical token that does not identify anyone: one word or code, with no digits, that names a status, type, role, or unit, such as `active`, `usd`, or `admin`. Replace every other scalar. When a value might be sensitive, replace it.

A placeholder is an obvious fake in the same kind and the same visible format (separators, letter case, prefix, length). Strings stay strings and numbers stay numbers.

- A person name follows the original letter case: `john smith` becomes `test name`.
- An SSN-shaped string becomes `111-11-1111`.
- An email becomes `test@example.com`.
- A phone number becomes `555-010-0000`.
- A street becomes `123 Test Street`. A city becomes `Test City`. A postal code becomes zeros in the same pattern, so `78701` becomes `00000`.
- A date keeps its original pattern and uses an obvious fake date.
- A UUID becomes `11111111-1111-4111-8111-111111111111`.
- A token or key keeps its prefix and becomes a short obvious fake.
- Free text becomes `test note`.
- Zero stays zero. A unix timestamp becomes `1111111111` or `1111111111111`, matching its digit count. Any other non-zero integer becomes `1`, and any other non-zero decimal becomes `1.0`.
- A digit string none of the lines above cover keeps its separators and becomes the same pattern of ones.

When an object's keys are themselves data, such as emails or ids, replace those keys and keep one entry.

## Repetition

In an array, keep the first item of each distinct shape and drop the rest. Shape is the tree of keys and value kinds, ignoring scalar values, so an extra field at any depth is a different shape. Nested arrays collapse the same way. Two addresses with the same fields become one address object inside the array. An array of scalars with the same kind keeps one element.

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
  "addresses": [
    {"line1": "1 Main St", "city": "Austin", "postal_code": "78701"},
    {"line1": "2 Oak Ave", "city": "Dallas", "postal_code": "75201"}
  ]
}
```

is answered with exactly:

```json
{
  "full_name": "test name",
  "ssn": "111-11-1111",
  "email": "test@example.com",
  "status": "active",
  "addresses": [
    {
      "line1": "123 Test Street",
      "city": "Test City",
      "postal_code": "00000"
    }
  ]
}
```
