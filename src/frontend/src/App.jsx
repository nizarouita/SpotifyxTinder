import { useState } from 'react';
import SongPicker from './components/SongPicker';
import SwipeScreen from './components/SwipeScreen';
import './App.css';

function App() {
  const [step, setStep] = useState('pick'); // 'pick' | 'swipe'
  const [likedIds, setLikedIds] = useState([]);

  return (
    <div className="app-shell">
      {step === 'pick' ? (
        <SongPicker
          likedIds={likedIds}
          setLikedIds={setLikedIds}
          onDone={() => setStep('swipe')}
        />
      ) : (
        <SwipeScreen />
      )}
    </div>
  );
}

export default App;