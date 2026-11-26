export function OrdersTable({ orders }: { orders: Order[] }) {
  return (
    <table className="w-full">
      <thead>
        <tr><th>Order</th><th>Customer</th><th>Email</th><th>Ship to</th><th>Total</th><th>Status</th></tr>
      </thead>
      <tbody>
        {orders.map((o) => (
          <tr key={o.id}><td>{o.id}</td><td>{o.customer}</td><td>{o.email}</td><td>{o.shipTo}</td><td>{o.total}</td><td>{o.status}</td></tr>
        ))}
      </tbody>
    </table>
  );
}
