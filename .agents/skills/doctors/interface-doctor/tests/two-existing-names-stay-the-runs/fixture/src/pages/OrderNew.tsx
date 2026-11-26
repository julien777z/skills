export default function OrderNew({ order }: { order: Order }) {
  return (
    <section>
      <h3>Customer</h3>
      <p>{order.customer}</p>
    </section>
  );
}
