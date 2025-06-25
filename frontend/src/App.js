import React, { useState } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL;

function App() {
  const [mode, setMode] = useState("link"); // 'link', 'pdf', 'text'
  const [link, setLink] = useState("");
  const [pdfFile, setPdfFile] = useState(null);
  const [textInput, setTextInput] = useState("");
  const [audioUrl, setAudioUrl] = useState("");
  const [textUrl, setTextUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const resetOutputs = () => {
    setAudioUrl("");
    setTextUrl("");
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    resetOutputs();
    try {
      if (mode === "link") {
        try {
          const formData = new FormData();
          formData.append('link', link);
          const res = await fetch(`${API_BASE_URL}/link-to-audio/`, {
            method: "POST",
            body: formData
          });
          let data;
          try {
            data = await res.json();
          } catch {
            setError("Server error: could not parse response.");
            setLoading(false);
            return;
          }
          if (res.ok && data.audio_file) {
            setAudioUrl(`${API_BASE_URL}/audio/${data.audio_file}`);
          } else {
            setError(data?.error || `Error: ${res.status} ${res.statusText}`);
          }
        } catch (err) {
          setError("Error: " + err.message);
        }
      } else if (mode === "pdf") {
        if (!pdfFile) {
          setError("Please select a PDF file.");
          setLoading(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', pdfFile);
        const res = await fetch(`${API_BASE_URL}/pdf-to-text-audio/`, {
          method: "POST",
          body: formData
        });
        const data = await res.json();
        if (res.ok && data.text_file && data.audio_file) {
          setTextUrl(`${API_BASE_URL}/text/${data.text_file}`);
          setAudioUrl(`${API_BASE_URL}/audio/${data.audio_file}`);
        } else {
          setError(data.error || "Failed to process PDF.");
        }
      } else if (mode === "text") {
        if (!textInput.trim()) {
          setError("Please enter some text.");
          setLoading(false);
          return;
        }
        const formData = new FormData();
        formData.append('text', textInput);
        const res = await fetch(`${API_BASE_URL}/text-to-audio/`, {
          method: "POST",
          body: formData
        });
        const data = await res.json();
        if (res.ok && data.audio_file) {
          setAudioUrl(`${API_BASE_URL}/audio/${data.audio_file}`);
        } else {
          setError(data.error || "Failed to generate audio from text.");
        }
      }
    } catch (err) {
      setError("Error: " + err.message);
    }
    setLoading(false);
  };

  return (
    <div className="App" style={{ maxWidth: 600, margin: '0 auto', padding: '1em' }}>
      <h1 style={{ fontSize: '2em', textAlign: 'center' }}>PDF & Text to Audio Converter</h1>
      <div style={{ display: 'flex', justifyContent: 'center', gap: 8, marginBottom: 16, flexWrap: 'wrap' }}>
        <button onClick={() => { setMode('link'); resetOutputs(); }} style={{ padding: 8, borderRadius: 6, border: mode === 'link' ? '2px solid #1976d2' : '1px solid #ccc', background: mode === 'link' ? '#e3f2fd' : 'white', minWidth: 80 }}>Link</button>
        <button onClick={() => { setMode('pdf'); resetOutputs(); }} style={{ padding: 8, borderRadius: 6, border: mode === 'pdf' ? '2px solid #1976d2' : '1px solid #ccc', background: mode === 'pdf' ? '#e3f2fd' : 'white', minWidth: 80 }}>PDF</button>
        <button onClick={() => { setMode('text'); resetOutputs(); }} style={{ padding: 8, borderRadius: 6, border: mode === 'text' ? '2px solid #1976d2' : '1px solid #ccc', background: mode === 'text' ? '#e3f2fd' : 'white', minWidth: 80 }}>Text</button>
      </div>
      <form onSubmit={handleSubmit} style={{ margin: '2em 0', display: 'flex', flexDirection: 'column', gap: '1em' }}>
        {mode === "link" && (
          <label style={{ fontSize: '1em' }}>
            Enter a link to convert webpage text to audio:
            <input
              type="text"
              value={link}
              onChange={e => setLink(e.target.value)}
              style={{
                width: '100%',
                maxWidth: 400,
                margin: '0.5em 0',
                padding: '0.75em',
                fontSize: '1em',
                borderRadius: 6,
                border: '1px solid #ccc',
                boxSizing: 'border-box'
              }}
              placeholder="https://example.com"
              required
            />
          </label>
        )}
        {mode === "pdf" && (
          <label style={{ fontSize: '1em' }}>
            Upload a PDF to extract text and generate audio:
            <input
              type="file"
              accept="application/pdf"
              onChange={e => setPdfFile(e.target.files[0])}
              style={{
                width: '100%',
                maxWidth: 400,
                margin: '0.5em 0',
                padding: '0.75em',
                fontSize: '1em',
                borderRadius: 6,
                border: '1px solid #ccc',
                boxSizing: 'border-box'
              }}
              required
            />
          </label>
        )}
        {mode === "text" && (
          <label style={{ fontSize: '1em', width: '100%' }}>
            Paste text to generate audio:
            <textarea
              value={textInput}
              onChange={e => setTextInput(e.target.value)}
              rows={6}
              style={{
                width: '100%',
                maxWidth: 400,
                margin: '0.5em 0',
                padding: '0.75em',
                fontSize: '1em',
                borderRadius: 6,
                border: '1px solid #ccc',
                boxSizing: 'border-box',
                resize: 'vertical'
              }}
              placeholder="Paste or type your text here..."
              required
            />
          </label>
        )}
        <button
          type="submit"
          disabled={loading || (mode === 'link' && !link) || (mode === 'pdf' && !pdfFile) || (mode === 'text' && !textInput.trim())}
          style={{
            padding: '0.75em',
            fontSize: '1em',
            borderRadius: 6,
            background: '#1976d2',
            color: 'white',
            border: 'none',
            cursor: loading ? 'not-allowed' : 'pointer',
            width: '100%',
            maxWidth: 400,
            alignSelf: 'center'
          }}
        >
          Convert
        </button>
      </form>
      {loading && <p style={{ textAlign: 'center' }}>Processing...</p>}
      {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}
      {textUrl && (
        <div style={{ textAlign: 'center', marginBottom: 16 }}>
          <h3>Text Result:</h3>
          <a href={textUrl} download style={{ color: '#1976d2' }}>Download Extracted Text</a>
        </div>
      )}
      {audioUrl && (
        <div style={{ textAlign: 'center' }}>
          <h3>Audio Result:</h3>
          <audio controls src={audioUrl} style={{ width: '100%', maxWidth: 400 }} />
          <p><a href={audioUrl} download style={{ color: '#1976d2' }}>Download Audio</a></p>
        </div>
      )}
    </div>
  );
}

export default App;
