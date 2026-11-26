# interface-doctor run — audit findings (all verified; app storefront; widths captured 390, 768, 1280)

F1. Orders table overflows. src/components/OrdersTable.tsx renders six columns (Order, Customer,
    Email, Ship to, Total, Status). At 390 and 768 the Total and Status values are cut off and cannot
    be read; at 1280 everything fits. Remedy: hide the "Ship to" column below 768 (add
    `hidden md:table-cell` to its header and cells). Captures: captures/orders-390.png,
    captures/orders-768.png, captures/orders-1280.png.
F2. Button label. src/components/OrderForm.tsx has a submit button labeled "Save order". The text is
    correct and clear; the text lens notes it could read better. Remedy: reword to "Update order".
    Capture: captures/orderform-1280.png.
F3. One thing under two names. Customers are called "Customer" in 14 places across 14 pages and
    "Client" in 2 places (src/pages/OrderDetail.tsx heading "Client details"; src/pages/Invoices.tsx
    column header "Client"). No rule or shared component establishes either name. Remedy: use
    "Customer" in the two places that say "Client".
