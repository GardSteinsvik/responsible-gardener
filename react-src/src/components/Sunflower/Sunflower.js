import React from 'react'
import classNames from 'classnames'
import styles from './Sunflower.module.css'

export const Sunflower = (props) => {

    console.log(props.moisture)

    const moistureHue = !!props.moisture ? ({filter: `hue-rotate(${props.moisture-10}deg)`}) : ({})
    console.log(moistureHue)

    const petalGrayscale = !!props.moisture ? ({filter: `grayscale(${(70-props.moisture)}%)`}) : ({})
    console.log(petalGrayscale)

    const petals = (
        <React.Fragment>
            <div className={classNames(styles.petal, styles.p1)}/>
                <div className={classNames(styles.petal, styles.p2)}/>
                <div className={classNames(styles.petal, styles.p3)}/>
                <div className={classNames(styles.petal, styles.p4)}/>
                <div className={classNames(styles.petal, styles.p5)}/>
                <div className={classNames(styles.petal, styles.p6)}/>
                <div className={classNames(styles.petal, styles.p7)}/>
                <div className={classNames(styles.petal, styles.p8)}/>
                <div className={classNames(styles.petal, styles.p9)}/>
                <div className={classNames(styles.petal, styles.p10)}/>
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

