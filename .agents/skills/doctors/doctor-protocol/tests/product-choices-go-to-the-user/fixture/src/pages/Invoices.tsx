export default function Invoices({ invoices }: { invoices: Invoice[] }) {
  return (
    <table>
      <thead>
        <tr><th>Invoice</th><th>Client</th><th>Amount</th></tr>
      </thead>
      <tbody>
        {invoices.map((i) => (
          <tr key={i.id}><td>{i.id}</td><td>{i.customer}</td><td>{i.amount}</td></tr>
        ))}
      </tbody>
    </table>
  );
}
