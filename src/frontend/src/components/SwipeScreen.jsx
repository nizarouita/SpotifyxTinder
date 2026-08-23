import { useEffect, useRef, useState } from 'react';
import { getNextSong, addLikedSong } from '../api';
import './SwipeScreen.css';

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
const getAlbum = (song) => song.albumName ?? song.album_name ?? null;
const getArtwork = (song) => song.artworkUrl ?? null;

export default function SwipeScreen() {
  const [song, setSong] = useState(null);
  const [loading, setLoading] = useState(true);
  const [finished, setFinished] = useState(false);
  const [error, setError] = useState(null);
  const [dragX, setDragX] = useState(0);
  const dragging = useRef(false);
  const startX = useRef(0);

  const loadNext = () => {
    setLoading(true);
    setDragX(0);
    getNextSong()
      .then((data) => {
        setSong(data);
        setFinished(false);
      })
      .catch((err) => {
        if (err.status === 404) {
          setFinished(true);
          setSong(null);
        } else {
          setError('Could not load the next song.');
        }
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    loadNext();
  }, []);

  const commitSwipe = async (direction) => {
    if (!song) return;
    if (direction === 'right') {
      try {
        await addLikedSong(getId(song));
      } catch {
        setError('Could not save that song, moving on anyway.');
      }
    }
    if (direction === 'left') {
      try {
        await addLikedSong(getId(song), -1);
      } catch {
        setError('Could not save that song, moving on anyway.');
      }
    }
    loadNext();
  };

  const onPointerDown = (e) => {
    dragging.current = true;
    startX.current = e.clientX;
  };
  const onPointerMove = (e) => {
    if (!dragging.current) return;
    setDragX(e.clientX - startX.current);
  };
  const onPointerUp = () => {
    if (!dragging.current) return;
    dragging.current = false;
    if (dragX > 120) commitSwipe('right');
    else if (dragX < -120) commitSwipe('left');
    else setDragX(0);
  };

  if (loading && !song) {
    return <div className="swipe-status">Loading the next song...</div>;
  }

  if (finished) {
    return (
      <div className="swipe-status">
        <h2>That's every song we've got</h2>
        <p>Come back later for more.</p>
      </div>
    );
  }

  const rotation = dragX / 18;

  return (
    <div className="swipe-screen">
      {/* <p className="swipe-eyebrow">Step 2 of 2</p> */}

      {song && (
        <div
            className="swipe-card"
            style={{ transform: `translateX(${dragX}px) rotate(${rotation}deg)` }}
            onPointerDown={onPointerDown}
            onPointerMove={onPointerMove}
            onPointerUp={onPointerUp}
            onPointerLeave={onPointerUp}
        >
            {/* <span className="swipe-card-label">now playing</span> */}

            <div className="swipe-card-art">
            {getArtwork(song) ? (
                <img src={getArtwork(song)} alt="" draggable={false} />
            ) : (
                <div className="swipe-card-art-fallback">♪</div>
            )}
            </div>

            <h2 className="swipe-card-title">{getName(song)}</h2>
            <p className="swipe-card-artist">{getArtist(song)}</p>
            <div className="swipe-card-meta">
            {getAlbum(song) && <span>{getAlbum(song)}</span>}
            {/* {getTempo(song) && <span>{getTempo(song)}</span>} */}
            </div>
        </div>
        )}

      <div className="swipe-actions">
        <button className="swipe-btn dislike" onClick={() => commitSwipe('left')} aria-label="Skip">
          ✕
        </button>
        <button className="swipe-btn like" onClick={() => commitSwipe('right')} aria-label="Like">
          ♥
        </button>
      </div>

      {error && <p className="picker-error">{error}</p>}
    </div>
  );
}