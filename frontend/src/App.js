import React, { useState } from 'react';

function App() {
  const [link, setLink] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setAudioUrl("");
    try {
      const formData = new FormData();
      formData.append('link', link);
      const res = await fetch("http://localhost:8000/link-to-audio/", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      if (res.ok && data.audio_file) {
        setAudioUrl(`http://localhost:8000/audio/${data.audio_file}`);
      } else {
        setError(data.error || "Failed to generate audio.");
      }
    } catch (err) {
      setError("Error: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>PDF to Audio Converter</h1>
      <p>Welcome! The backend is running on FastAPI.</p>
      <form onSubmit={handleSubmit} style={{ margin: '2em 0' }}>
        <label>
          Enter a link to convert webpage text to audio:<br />
          <input
            type="text"
            value={link}
            onChange={e => setLink(e.target.value)}
            style={{ width: '400px', marginRight: '1em' }}
            placeholder="https://example.com"
            required
          />
        </label>
        <button type="submit" disabled={loading || !link}>Convert</button>
      </form>
      {loading && <p>Processing...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {audioUrl && (
        <div>
          <h3>Audio Result:</h3>
          <audio controls src={audioUrl} />
          <p><a href={audioUrl} download>Download Audio</a></p>
        </div>
      )}
    </div>
  );
}

export default App;
