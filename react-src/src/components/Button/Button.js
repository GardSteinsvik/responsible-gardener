import React from 'react'
import styles from './Button.module.css'
import classNames from 'classnames'

const Button = (props) => {

    return (
        <button
            className={classNames(
                props.className,
                styles.button,
                props.inProgress && styles.inProgress,
            )}
            onClick={props.onClick}
            disabled={props.disabled || props.inProgress}
        >
            {props.children}
        </button>
    )
}

export default Button