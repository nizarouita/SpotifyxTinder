const BASE_URL = '/api'; // adjust to match your Flask server's host/port

async function request(path, options = {}) {
  const res = await fetch(`${BASE_URL}${path}`, {
    credentials: 'include', // required so Flask's session cookie is sent
    ...options,
  });
  if (!res.ok) {
    const error = new Error(`Request to ${path} failed with status ${res.status}`);
    error.status = res.status;
    throw error;
  }
  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

export function searchSongs(query) {
  return request(`/search_songs?q=${encodeURIComponent(query)}`);
}

export function getNextSong() {
  return request('/get_next_song');
}

export function addLikedSong(trackId, score = 1) {
  return request(`/add_liked_song/${encodeURIComponent(trackId)}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ score }),
  });
}