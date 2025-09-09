import { useEffect, useState } from "react";

function App() {
  const [products, setProducts] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState(null);
  const [orderStatus, setOrderStatus] = useState(null);

  useEffect(() => {
    fetch(`${import.meta.env.VITE_INVENTORY_API}/products/`)
      .then((res) => res.json())
      .then(setProducts);
  }, []);

  const placeOrder = async () => {
    if (!selectedProduct) return alert("Select a product first");

    // Create order
    const res = await fetch(`${import.meta.env.VITE_ORDER_API}/orders/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ product_id: selectedProduct.id, quantity: 1, amount: 10 })
    });

    const data = await res.json();
    setOrderStatus({ id: data.order_id, status: data.status });

    // Poll for status
    const interval = setInterval(async () => {
      const statusRes = await fetch(`${import.meta.env.VITE_ORDER_API}/orders/${data.order_id}/`);
      const statusData = await statusRes.json();
      setOrderStatus(statusData);
      if (statusData.status !== "PENDING") clearInterval(interval);
    }, 2000);
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Place Order</h1>
      <h2>Products</h2>
      <ul>
        {products.map((p) => (
          <li key={p.id}>
            <label>
              <input
                type="radio"
                name="product"
                value={p.id}
                onChange={() => setSelectedProduct(p)}
              />
              {p.name} - Stock: {p.stock}
            </label>
          </li>
        ))}
      </ul>

      <button onClick={placeOrder} disabled={!selectedProduct}>
        Place Order
      </button>

      {orderStatus && (
        <div style={{ marginTop: 20 }}>
          <h3>Order Status:</h3>
          <p>ID: {orderStatus.id}</p>
          <p>Status: {orderStatus.status}</p>
        </div>
      )}
    </div>
  );
}

export default App;
