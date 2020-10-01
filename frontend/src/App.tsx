import React, { useState, useEffect } from 'react'
import './App.css'
import Lead from './Lead/Lead'
import Buttons from './Buttons/Buttons'
import Footer from './Footer/Footer'

interface simplePosition {
  latitude: number
  longitude: number
}

function App() {
  const [currentPosition, setCurrentPosition] = useState<Position | undefined>(undefined)
  const [topPosition, setTopPosition] = useState<simplePosition | undefined>(undefined)
  const [isMapButtonClicked, setIsMapButtonClicked] = useState<boolean>(false)
  const [didFetchingFail, setDidFetchingFail] = useState<boolean>(false)
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
      .catch(error => {
        console.error('Failed to get closest top: ', error)
        setDidFetchingFail(true)
        setIsMapButtonClicked(false)
      })
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
  useEffect(() => {
    if (currentPosition !== undefined &&
        topPosition !== undefined &&
        isMapButtonClicked === true) {

          setIsMapButtonClicked(false)
          openMap()
        }
  }, [currentPosition, topPosition, isMapButtonClicked])

  const clickMapButton = () => {
    setIsMapButtonClicked(true)
  }
  const openAbout = () => {
    window.open('https://github.com/franpog859/top-of-the-world/blob/master/README.md')
  }

  return (
    <div className='App'>
      <header className='App-header App-animation'>
        <Lead 
          didFetchingFail={didFetchingFail}
          isLocationAvailable={currentPosition !== undefined}/>
        <Buttons
          clickMapButton={clickMapButton}
          clickAboutButton={openAbout}
          isMapButtonClicked={isMapButtonClicked}/>
        <Footer />
      </header>
    </div>
  )
}

export default App
