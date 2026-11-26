def export_invoices(rows):
    """Yield invoice lines."""
    # TODO: remove after launch
    for row in rows:
        yield row.total
