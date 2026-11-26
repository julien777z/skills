export default function OrderDetail({ order }: { order: Order }) {
  return (
    <section>
      <h2>Client details</h2>
      <p>{order.customer}</p>
      <p>{order.email}</p>
    </section>
  );
}
