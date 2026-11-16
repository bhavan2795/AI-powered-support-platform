import { useState, type FormEvent } from "react";
import "./App.css";

type ChatMessage = {
  id: string;
  role: "assistant" | "user";
  text: string;
};

function App() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: "welcome",
      role: "assistant",
      text: "Hi! I’m your support assistant. How can I help today?",
    },
  ]);
  const [draft, setDraft] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState("");

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
  event.preventDefault();
  setError("");
  setIsSending(true);

  try {
    const response = await fetch("http://127.0.0.1:8000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed. Check your email and password.");
    }

    setToken(data.access_token);
  } catch (error) {
    setError(error instanceof Error ? error.message : "Login failed.");
  } finally {
    setIsSending(false);
  }
}

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const text = draft.trim();
    if (!text || isSending) return;

    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: "user", text },
    ]);
    setDraft("");
    setError("");
    setIsSending(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/chat", {
        method: "POST",
        headers: {
  "Content-Type": "application/json",
  "Authorization": `Bearer ${token}`,
},

        body: JSON.stringify({ message: text }),
      });

      if (!response.ok) {
        throw new Error("The server returned an error.");
      }

      const data: { reply: string } = await response.json();

      setMessages((current) => [
        ...current,
        { id: crypto.randomUUID(), role: "assistant", text: data.reply },
      ]);
    } catch {
      setError("Could not reach the support server. Check that it is running.");
    } finally {
      setIsSending(false);
    }
  }

  return (
    <main className="chat">
      <header className="chat-header">
        <h1>Support Desk</h1>
        <p>We’re here to help</p>
      </header>

      <section className="messages" aria-live="polite">
        {messages.map((message) => (
          <div className={`message ${message.role}`} key={message.id}>
            {message.text}
          </div>
        ))}
      </section>

      {error && <p className="error-message" role="alert">{error}</p>}

      <form className="message-form" onSubmit={handleSubmit}>
        <input
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Type your message..."
          aria-label="Type your message"
          disabled={isSending}
        />
        <button type="submit" disabled={isSending}>
          {isSending ? "Sending..." : "Send"}
        </button>
      </form>
    </main>
  );
}

export default App;