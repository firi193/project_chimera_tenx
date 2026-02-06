import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import ReviewQueuePage from "./pages/review";

export default function App() {
  return (
    <BrowserRouter>
      <div style={{ fontFamily: "system-ui, sans-serif", maxWidth: 960, margin: "0 auto", padding: 24 }}>
        <header style={{ borderBottom: "1px solid #eee", paddingBottom: 16, marginBottom: 24 }}>
          <h1 style={{ margin: 0, fontSize: "1.5rem" }}>Chimera HITL Review Dashboard</h1>
          <p style={{ margin: "8px 0 0", color: "#666" }}>Review queue and approve / reject / edit content.</p>
          <nav style={{ marginTop: 16 }}>
            <Link to="/" style={{ marginRight: 16 }}>Home</Link>
            <Link to="/review">Review Queue</Link>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/review" element={<ReviewQueuePage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

function HomePage() {
  return (
    <div>
      <h2>Home</h2>
      <p>Use the <strong>Review Queue</strong> to see items that need human review (medium-confidence or sensitive-topic content).</p>
      <p>From each item you can approve, reject, or edit before content is published.</p>
    </div>
  );
}
