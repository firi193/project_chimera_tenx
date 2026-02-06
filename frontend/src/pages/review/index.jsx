import { useState } from "react";

export default function ReviewQueuePage() {
  const [filter, setFilter] = useState("pending");
  // Placeholder: will be replaced by GET /api/v1/review/queue when backend is ready
  const items = [];

  return (
    <div>
      <h2>Review Queue</h2>
      <p>Items that need human review (medium-confidence or sensitive-topic).</p>
      <div style={{ marginBottom: 16 }}>
        <label style={{ marginRight: 8 }}>Status:</label>
        <select value={filter} onChange={(e) => setFilter(e.target.value)}>
          <option value="pending">Pending</option>
          <option value="approved">Approved</option>
          <option value="rejected">Rejected</option>
          <option value="edited">Edited</option>
        </select>
      </div>
      {items.length === 0 ? (
        <p style={{ color: "#666" }}>No items in the review queue. Pending items will appear here when the backend Review API is connected.</p>
      ) : (
        <ul style={{ listStyle: "none", padding: 0 }}>
          {items.map((item) => (
            <li key={item.id} style={{ padding: 12, border: "1px solid #eee", marginBottom: 8 }}>
              <strong>{item.id}</strong> – {item.status}
            </li>
          ))}
        </ul>
      )}
      <section style={{ marginTop: 24, padding: 16, background: "#f9f9f9", borderRadius: 8 }}>
        <h3 style={{ marginTop: 0 }}>Actions</h3>
        <p>When you open an item you can:</p>
        <ul>
          <li><strong>Approve</strong> – content can proceed to publish</li>
          <li><strong>Reject</strong> – content is rejected; task can be retried</li>
          <li><strong>Edit</strong> – change the content then approve</li>
        </ul>
      </section>
    </div>
  );
}
