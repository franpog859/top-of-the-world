import React from 'react';
import logo from './logo.svg';
import './App.css';

function App() {
  const buttonClick = () => {
    window.open("https://www.google.be/maps/dir/51.3867197,28.722/53.296,29.1225/data=!3m1!4b1!4m2!4m1!3e2");
  }

  return (
    <div className="App">
      <header className="App-header">
        <button onClick={buttonClick}>Take me to the top!</button>
      </header>
    </div>
  );
}

export default App;
