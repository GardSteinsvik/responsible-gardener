import React, {Component} from 'react'
import DataApi from "../api/DataApi"
import styles from './App.module.css'
import {Sunflower} from '../components/Sunflower/Sunflower'
import Button from '../components/Button/Button';

class App extends Component {

  constructor(props) {
    super(props)

    this.state = {
      moisture: ''
    }

    DataApi.getMoisture()
      .then(result => {
        this.setState({
          moisture: result.moisture.toFixed(1)
        })
      })
      .catch(error => console.log(error))
  }

  render() {
    const moistureInfo = this.state.moisture ? `${this.state.moisture}%` : 'Loading...'
    return (
      <div className={styles.app}>
        <h1>Responsible Gardener</h1>
        <Sunflower moisture={this.state.moisture}>
          <p>MOISTURE</p>
          <p>{moistureInfo}</p>
        </Sunflower>
        <Button disabled>TURN ON AUTO WATERING</Button>
        <Button>WATER ONCE</Button>
        <Button>ADJUST WATERING AMOUNT</Button>
        <Button inProgress>WATERING...</Button>
        {[1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100].map(n => <Sunflower key={n} moisture={n}>{n}%</Sunflower>)}
      </div>
    )
  }
}

export default App;
