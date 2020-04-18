import React, { useState, useEffect } from 'react'
import Button from 'react-bootstrap/Button'
import './App.css'

interface simplePosition {
  latitude: number
  longitude: number
}

function App() {
  const [currentPosition, setCurrentPosition] = useState<Position | undefined>(undefined)
  const [topPosition, setTopPosition] = useState<simplePosition | undefined>(undefined)
  const [shouldWarmUpBackend, setShouldWarmUpBackend] = useState<boolean>(true)
  const backendURL = process.env.REACT_APP_BACKEND_URL!
  const authToken = process.env.REACT_APP_AUTH_TOKEN!

  const setAsyncPosition = async () => { navigator.geolocation.getCurrentPosition(
    position => setCurrentPosition(position),
    err => console.log('Failed to get current position', err)
  )}
  setAsyncPosition()

  const buildClosestTopBackendPath = (position: Position) => {
    return `${backendURL}/closestTop/${position.coords.latitude}/${position.coords.longitude}`
  }
  const buildHealthzBackendPath = () => {
    return `${backendURL}/healthz`
  }
  const warmUpBackend = async () => {
    console.log("warming up")
    console.log(buildHealthzBackendPath())
    fetch(buildHealthzBackendPath(), {headers: {'token': authToken}})
      .then(response => response.json())
      .then(response => console.log(response))
      .catch(error => console.log('Failed to warm up the backend: ', error))
  }
  useEffect(() => {
    if (shouldWarmUpBackend) {
      warmUpBackend()
      setShouldWarmUpBackend(false)
    }
  }, [shouldWarmUpBackend])

  useEffect(() => {
    if (currentPosition) {
      fetch(buildClosestTopBackendPath(currentPosition!), {headers: {'token': authToken}})
        .then(response => response.json())
        .then(response => setTopPosition({latitude: response.latitude, longitude: response.longitude}))
        .catch(error => console.log('Failed to get closest top: ', error))
    }
  }, [currentPosition])

  const openMap = () => {
    const currentLatitude = currentPosition!.coords.latitude.toString()
    const currentLongitude = currentPosition!.coords.longitude.toString()
    const topLatitude = topPosition!.latitude.toString()
    const topLongitude = topPosition!.longitude.toString()
    window.open(`https://www.google.be/maps/dir/${currentLatitude},${currentLongitude}`+
      `/${topLatitude},${topLongitude}/data=!3m1!4b1!4m2!4m1!3e2`)
  }
  const openAbout = () => {
    window.open("https://github.com/franpog859/top-of-the-world/blob/master/README.md")
  }

  const enableMapButton = (): boolean => {
    return currentPosition !== undefined && topPosition !== undefined
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

export default App
