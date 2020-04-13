import React from 'react';
import Button from 'react-bootstrap/Button';
import './App.css';

function App() {
  const openMap = () => {
    window.open("https://www.google.be/maps/dir/51.3867197,28.722/53.296,29.1225/data=!3m1!4b1!4m2!4m1!3e2");
  }

  const openAbout = () => {
    window.open("https://github.com/franpog859/top-of-the-world/blob/Add-frontend-boilerplate/README.md");
  }

  return (
    <div className="App">
      <header className="App-header">
        <Button variant="success" onClick={openMap} size="lg">Take me to the top!</Button><br></br>
        <Button variant="outline-secondary" onClick={openAbout} size="lg">Wait, what?</Button>
      </header>
    </div>
  );
}

export default App;
