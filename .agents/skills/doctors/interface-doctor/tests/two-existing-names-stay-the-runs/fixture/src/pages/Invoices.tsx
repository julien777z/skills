export default function Invoices({ order }: { order: Order }) {
  return (
    <section>
      <h3>Client</h3>
      <p>{order.customer}</p>
    </section>
  );
}
