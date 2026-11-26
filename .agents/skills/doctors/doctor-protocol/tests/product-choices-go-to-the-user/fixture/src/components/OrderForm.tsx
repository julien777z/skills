export function OrderForm({ onSubmit }: { onSubmit: (data: FormData) => void }) {
  return (
    <form action={onSubmit}>
      <input name="reference" />
      <input name="notes" />
      <button type="submit">Save order</button>
    </form>
  );
}
