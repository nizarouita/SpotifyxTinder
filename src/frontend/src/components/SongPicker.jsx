import { useEffect, useMemo, useState } from 'react';
import { searchSongs, addLikedSong } from '../api';
import { useDebounce } from '../hooks/useDebounce';
import './SongPicker.css';

const MIN_SONGS = 3;
const MAX_SONGS = 3;

// Your dataset's exact key names might differ from these — adjust if needed.
const getId = (song) => song.trackId ?? song.track_id;
const getName = (song) => song.trackName ?? song.track_name ?? 'Unknown title';
const getArtist = (song) => {
  const raw = song.artists ?? song.artist ?? 'Unknown artist';
  return formatArtists(raw);
};

function formatArtists(raw) {
  if (!raw) return 'Unknown artist';
  const str = String(raw).trim();

  // Detect a Python-list-looking string: starts with [ and ends with ]
  if (str.startsWith('[') && str.endsWith(']')) {
    const names = str
      .slice(1, -1) // strip [ and ]
      .split(',')
      .map((n) => n.trim().replace(/^['"]|['"]$/g, '')) // strip quotes
      .filter(Boolean);
    return names.join(' & ');
  }

  // Otherwise assume semicolon-separated
  const names = str
    .split(';')
    .map((n) => n.trim())
    .filter(Boolean);
  return names.join(' & ');
}

export default function SongPicker({ likedIds, setLikedIds, onDone }) {
//   const [allSongs, setAllSongs] = useState([]);
//   const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  const debouncedQuery = useDebounce(query, 250);
  const [addingId, setAddingId] = useState(null);
  const [results, setResults] = useState([]);

  useEffect(() => {
    const q = debouncedQuery.trim();
    if (!q) {
      setResults([]);
      return;
    }
    searchSongs(q)
      .then((data) => setResults(Array.isArray(data) ? data : []))
      .catch(() => setError('Search failed. Try again.'));
  }, [debouncedQuery]);


  const [likedSongObjects, setLikedSongObjects] = useState([]);
  const handleSelect = async (song) => {
    const id = getId(song);
    if (likedIds.includes(id) || likedIds.length >= MAX_SONGS) return;
    setAddingId(id);
    try {
      await addLikedSong(id);
      setLikedIds((prev) => [...prev, id]);
      setLikedSongObjects((prev) => [...prev, song]);
      setQuery('');
    } catch {
      setError('Could not save that song. Try again.');
    } finally {
      setAddingId(null);
    }
  };

  const likedSongs = likedSongObjects;
  const canProceed = likedIds.length >= MIN_SONGS;

  return (
    <div className="picker">
      {/* <p className="picker-eyebrow">Step 1 of 2</p> */}
      <h1 className="picker-title">Pick 3 songs that you like</h1>
      <p className="picker-subtitle">
        The more you swipe the more the algorithm knows about your taste
      </p>

      <input
        className="picker-search"
        type="text"
        placeholder="Search for a song or artist..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        disabled={likedIds.length >= MAX_SONGS}
      />

      {error && <p className="picker-error">{error}</p>}

      {debouncedQuery && (
        <ul className="picker-results">
          {results.length === 0 && (
            <li className="picker-empty">No matches yet — try another spelling.</li>
          )}
          {results.map((song) => {
            const id = getId(song);
            return (
              <li key={id} className="picker-result-row">
                <div>
                  <span className="picker-result-name">{getName(song)}</span>
                  <span className="picker-result-artist">{getArtist(song)}</span>
                </div>
                <button
                  className="picker-add-btn"
                  onClick={() => handleSelect(song)}
                  disabled={addingId === id}
                >
                  {addingId === id ? '···' : 'Add'}
                </button>
              </li>
            );
          })}
        </ul>
      )}

      <div className="picker-crate">
        {Array.from({ length: MAX_SONGS }).map((_, i) => {
          const song = likedSongs[i];
          return (
            <div key={i} className={`picker-chip ${song ? 'filled' : ''}`}>
              {song ? getName(song) : `${i + 1}`}
            </div>
          );
        })}
      </div>

      <button className="picker-next-btn" disabled={!canProceed} onClick={onDone}>
        {canProceed ? 'Start swiping →' : `Pick ${MIN_SONGS - likedIds.length} more`}
      </button>
    </div>
  );
}