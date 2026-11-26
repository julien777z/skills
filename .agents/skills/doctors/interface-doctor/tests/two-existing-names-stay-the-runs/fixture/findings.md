# interface-doctor run — audit findings (all verified; app storefront; widths captured 390, 768, 1280)

F1. One thing under two names. The person who places an order is called "Customer" on 8 pages
    (src/pages/Orders.tsx, OrderNew.tsx, OrderEdit.tsx, Checkout.tsx, Cart.tsx, Refunds.tsx,
    Returns.tsx, Dashboard.tsx) and "Client" on 7 pages (src/pages/Invoices.tsx, InvoiceDetail.tsx,
    Statements.tsx, Payments.tsx, Reports.tsx, Settings.tsx, Shipments.tsx). Every one of the 15 is a
    column header or heading naming the same record, `order.customer`. Both words are correct; no
    rule, glossary or shared component establishes either. Remedy: one name on every page.
    Captures: captures/orders-1280.png (says "Customer"), captures/invoices-1280.png (says "Client").
