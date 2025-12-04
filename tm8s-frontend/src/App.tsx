import { useState } from 'react'
import './App.css'

function App() {
  const [player1, setPlayer1] = useState("")
  const [player2, setPlayer2] = useState("")
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault(); // Prevents the browser from reloading the page

    if (!player1 || !player2) {
      alert("Please enter both player names.");
      return;
    }

    setLoading(true)
    setResults(null)

    try {
      const response = await fetch(`http://127.0.0.1:8000/api/connections?p1=${player1}&p2=${player2}`)

      if (response.status === 404) {
        setResults({ count: 0, connections: [] });
        return;
      }

      const data = await response.json()
      setResults(data)

    } catch (error) {
      console.error("Error connecting to server:", error)
      alert("Could not connect to the Python Backend. Is it running?")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container">
      <h1>⚽ tm8s</h1>
      <p>Find teammates who played together.</p>

      <form onSubmit={handleSearch} className="search-box-form">
        <div className="search-box">
          <div className="player-input">
            <label>Player 1</label>
            <input
              type="text"
              placeholder="Enter first player name"
              value={player1}
              onChange={(e) => setPlayer1(e.target.value)}
            />
          </div>

          <div className="player-input">
            <label>Player 2</label>
            <input
              type="text"
              placeholder="Enter second player name"
              value={player2}
              onChange={(e) => setPlayer2(e.target.value)}
            />
          </div>
        </div>

        <button type="submit" disabled={loading || !player1 || !player2}>
          {loading ? "Scouting..." : "Find Connection"}
        </button>
      </form>


      {/* Results Section - START */}

      {results && (
        <div className="results-area">
          {results.count > 0 ? (
            // SUCCESS STATE: Green Cards
            <>
              <h3 style={{ color: 'green' }}>✅ {results.count} {results.count === 1 ? 'connection': 'connections'} found!</h3>
              {results.connections.map((conn: any, index: number) => (
                  <div key={index} className="card success-card">
                      {/* 👇 Add the image directly here */}
                      {conn.crest_url && (
                          <img src={conn.crest_url} alt="Club Crest" className="card-bg-crest" 
                          onError={(e) => e.currentTarget.style.display = 'none'}
                          />
                      )}
                      
                      {/* Wrap text in a relative div to keep it on top */}
                      <div className="card-content">
                          <h4>{conn.club_name}</h4>
                          <p>Played together: {conn.overlap_start} - {conn.overlap_end}</p>
                      </div>
                  </div>
              ))}
            </>
          ) : (
            // FAILURE STATE: Red Message
            <h3 style={{ color: 'red' }}>❌ Never played together.</h3>
          )}
        </div>
      )} {/* Results Section - END */}

    </div>
  );
}

export default App