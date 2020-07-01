import React, {useState, useEffect} from 'react'
import {getData, setLastWatered} from '../api/api'
import styles from './App.module.css'
import {Sunflower} from '../components/Sunflower/Sunflower'
import Button from '../components/Button/Button'
import WaterAmount from './WaterAmount'
import {format} from 'date-fns'

const App = () => {

    const [data, setData] = useState(null)
    const [errorMessage, setErrorMessage] = useState(null)

    const [loadingSetLastWatered, setLoadingSetLastWatered] = useState(false)
    const [setLastWateredSuccess, setSetLastWateredSucces] = useState(false)

    useEffect(() => {
        getData().then(
            data => {
                setData(data)                
            },
            error => {
                setErrorMessage(error.message)
            },
        )
    }, [])

    function handleSetLastWatered() {
        setLoadingSetLastWatered(true)
        setSetLastWateredSucces(false)
        setLastWatered().then(
            data => {
                console.log(data)
                setLoadingSetLastWatered(false)
                setSetLastWateredSucces(true)
            },
            error => {
                setErrorMessage(error.message)
            },
        )
    }

    if (errorMessage) {
        return (
        <div className={styles.app}>
            <p>The Responsible Gardener is off duty.</p>
            <p>{errorMessage}</p>
        </div>
        )
    }

    if (data) {
        const {moisture, lastWatered, waterAmount} = data
        const moistureInfo = moisture === null ? 'Loading...' : `${+moisture.toFixed(1)}%`
        return (
            <div className={styles.app}>
                <h1>Responsible Gardener</h1>
                <Sunflower moisture={moisture}>
                <p>MOISTURE</p>
                <p>{moistureInfo}</p>
                </Sunflower>
                <div style={{height: 24}}/>
                <p>Last watered:</p>
                <p>{format(new Date(lastWatered), 'dd.MM.yyyy HH:mm:ss')}</p>
                <Button onClick={() => handleSetLastWatered()} inProgress={loadingSetLastWatered}>Set last watered to now</Button>
                {setLastWateredSuccess && <p style={{color: 'green', fontSize: 12}}>SUCCESS!</p>}

                <div style={{height: 24}}/>

                <WaterAmount waterAmount={waterAmount}/>
                {/* {[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map(n => <Sunflower key={n} moisture={n}>{n}%</Sunflower>)} */}
            </div>
        ) 
    }
    
    return <p>This page was intentionally left blank.</p>
}

export default App;
