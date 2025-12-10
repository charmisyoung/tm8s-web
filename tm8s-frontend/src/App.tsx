import React, { useState, useEffect } from 'react';
import './App.css'; 
import KoFiWidget from './KoFiWidget.tsx';

declare global {
    interface Window {
        gtag: (...args: any[]) => void;
    }
}

interface Connection {
    club_name: string;
    overlap_start: number;
    overlap_end: number;
    crest_url: string;
}

interface ResultsData {
    count: number;
    connections: Connection[];
}

function App() {
    const [player1, setPlayer1] = useState("");
    const [player2, setPlayer2] = useState("");
    const [results, setResults] = useState<ResultsData | null>(null);
    const [loading, setLoading] = useState(false);
    

    const trackPageView = (path: string, title: string) => {
        if (typeof window.gtag === 'function') {
            window.gtag('event', 'page_view', {
                page_title: title,
                page_path: path,
                send_to: 'G-NKL88L1XJK'
            });
        }
    };

    useEffect(() => {
        trackPageView('/', 'tm8s Home');
    }, []);
            
    async function handleSearch(e: React.FormEvent) {
        e.preventDefault();

        if (!player1 || !player2) {
            alert("Please enter both player names.");
            return;
        }

        setLoading(true);
        setResults(null);

        try {
            const response = await fetch(`/api/connections?p1=${player1}&p2=${player2}`);

            if (response.status === 404) {
                setResults({ count: 0, connections: [] });
                return;
            }

            const data = await response.json();
            setResults(data);

        } catch (error) {
            console.error("Error connecting to backend:", error);
            alert("Could not connect to the Python Backend. Is it running? Error: " + error);
        } finally {
            setLoading(false);
        }
    }
    
    return (
        <div className="container">
            <h1>⚽ tm8s</h1>
            <p><i>Uncovering shared history on the pitch</i></p>


            <form onSubmit={handleSearch} className="search-box-form">
                <div className="search-box">
                    {/* Player 1 Input */}
                    <div className="player-input">
                        <label><b>Player 1</b></label>
                        <input
                            type="text"
                            placeholder="Enter name e.g. Messi"
                            value={player1}
                            onChange={(e) => setPlayer1(e.target.value)}
                        />
                    </div>

                    {/* Player 2 Input */}
                    <div className="player-input">
                        <label><b>Player 2</b></label>
                        <input
                            type="text"
                            placeholder="Enter name e.g. Neymar"
                            value={player2}
                            onChange={(e) => setPlayer2(e.target.value)}
                        />
                    </div>
                </div>

                <button type="submit" disabled={loading || !player1 || !player2}>
                    {loading ? "Scouting..." : "Find Connection"}
                </button>
            <p style={{color: '#9A2A2A', fontSize: 12 }}>
                ⚠️ tm8s currently supports football (soccer) only.
            </p>
            </form>

            {/* Results Section - START */}
            {results && (
                <div className="results-area">
                    {results.count > 0 ? (
                        // SUCCESS STATE: Green Cards
                        <>
                            <h3 style={{ color: 'green' }}>
                                ✅ {results.count} {results.count === 1 ? 'Connection' : 'Connections'} found!
                            </h3>
                            {results.connections.map((conn: Connection, index: number) => (
                                <div key={index} className="card success-card">
                                    {conn.crest_url && (
                                        <img src={conn.crest_url} alt="" className="card-bg-crest" 
                                        onError={(e) => e.currentTarget.style.display = 'none'}
                                        />
                                    )}
                                    
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

        <div style={{ marginTop: '40px', fontSize: '0.8rem', display: 'flex', justifyContent: 'center', alignItems: 'center', gap: '8px' }}>
        <a 
            href="https://github.com/charmisyoung/tm8s-web" 
            target="_blank" 
            rel="noopener noreferrer"
            className="github-link"
        >
            <img 
                src="https://github.githubassets.com/assets/GitHub-Mark-ea2971cee799.png" 
                alt="GitHub" 
                style={{ width: '16px', height: '16px', opacity: 0.7, alignItems:'center' }} 
            />
            View Source Code on GitHub
        </a>

        <KoFiWidget />
    </div>
</div>
    );
}

export default App;