import React from 'react'
import classNames from 'classnames'
import styles from './Sunflower.module.css'

export const Sunflower = (props) => {
    const {moisture} = props

    const moistureHue = !!moisture ? ({filter: `hue-rotate(${moisture-10}deg)`}) : ({})
    const petalGrayscale = !!moisture ? ({filter: `grayscale(${(70-moisture)}%)`}) : ({})

    const petals = (
        <React.Fragment>
            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(i => <div key={i} className={classNames(styles.petal, styles[`p${i}`])}/>)}
        </React.Fragment>
    )

    return (
        <div className={styles.padding}>
            <div className={classNames(props.className, styles.card)}>
            <div className={styles.center} style={moistureHue}>
                {props.children}
            </div>
            <div className={styles.petalsBack}>
                <div className={styles.petals} style={petalGrayscale}>
                    {petals}
                </div>
            </div>
            <div className={styles.petals} style={petalGrayscale}>
                {petals}
            </div>
        </div>
        </div>
    )
}

