import React, {useState} from 'react'
import {setWaterAmount} from '../api/api'
import Button from '../components/Button/Button'


const WaterAmount = ({waterAmount}) => {

    const [waterAmountInput, setWaterAmountInput] = useState(waterAmount)

    const [loadingSetWaterAmount, setLoadingSetWaterAmount] = useState(false)
    const [setWaterAmountSuccess, setSetWaterAmountSuccess] = useState(false)
    const [errorMessage, setErrorMessage] = useState(null)

    function handleSetWaterAmount(waterAmount) {
        setLoadingSetWaterAmount(true)
        setSetWaterAmountSuccess(false)
        setWaterAmount(waterAmount).then(
            data => {
                console.log(data)
                setLoadingSetWaterAmount(false)
                setSetWaterAmountSuccess(true)
            },
            error => {
                setLoadingSetWaterAmount(false)
                setErrorMessage(error.message)
            },
        )
    }

    return (
    <>
        <p>Water amount:</p>
        <input type="number" value={waterAmountInput} onChange={e => setWaterAmountInput(e.target.value)}/>
        <Button onClick={() => handleSetWaterAmount(waterAmountInput)} inProgress={loadingSetWaterAmount}>Set water amount</Button>
        {setWaterAmountSuccess && <p style={{color: 'green', fontSize: 12}}>SUCCESS!</p>}
        {errorMessage && <p style={{color: 'red', fontSize: 12}}>{errorMessage}</p>}
    </>
    )
}

export default WaterAmount