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
  const backendURL = process.env.REACT_APP_BACKEND_URL!
  const authToken = process.env.REACT_APP_AUTH_TOKEN!

  const setAsyncPosition = async () => {
    navigator.geolocation.getCurrentPosition(
      position => setCurrentPosition(position),
      error => console.error('Failed to get current position: ', error)
    )
  }
  const buildHealthzBackendPath = () => `${backendURL}/healthz`
  const warmUpBackend = async () => {
    console.log('Warming the backend up...')
    fetch(buildHealthzBackendPath(), {headers: {'token': authToken}})
      .then(response => response.json())
      .then(response => console.debug(response))
      .catch(error => console.error('Failed to warm up the backend: ', error))
  }
  useEffect(() => {
    setAsyncPosition()
    warmUpBackend()
  }, [])

  const buildClosestTopBackendPath = (position: Position) => {
    return `${backendURL}/closestTop/${position.coords.latitude}/${position.coords.longitude}`
  }
  const fetchClosestTopPosition = async () => {
    console.log('Fetching closest top position...')
    fetch(buildClosestTopBackendPath(currentPosition!), {headers: {'token': authToken}})
      .then(response => response.json())
      .then(response => {console.debug(response); return response})
      .then(response => setTopPosition({
        latitude: response.latitude,
        longitude: response.longitude
      }))
      .catch(error => console.error('Failed to get closest top: ', error))
  }
  useEffect(() => {
    if (currentPosition) fetchClosestTopPosition()
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
    window.open('https://github.com/franpog859/top-of-the-world/blob/master/README.md')
  }

  const shouldMapButtonBeEnabled = (): boolean => {
    return currentPosition !== undefined && topPosition !== undefined
  }

  return (
    <div className='App'>
      <header className='App-header'>
        <Button
          variant='success'
          onClick={openMap}
          size='lg'
          disabled={!shouldMapButtonBeEnabled()}>
            Take me to the top!
        </Button>
        <br></br>
        <Button
          variant='outline-secondary'
          onClick={openAbout}
          size='lg'>
            Wait, what?
        </Button>
      </header>
    </div>
  );
}

export default App
