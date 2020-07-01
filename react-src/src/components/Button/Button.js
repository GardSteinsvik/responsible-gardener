import React from 'react'
import styles from './Button.module.css'
import classNames from 'classnames'

const Button = ({className, inProgress, onClick, disabled, children}) => {

    return (
        <button
            className={classNames(
                className,
                styles.button,
                inProgress && styles.inProgress,
            )}
            onClick={onClick}
            disabled={disabled || inProgress}
        >
            {children}
        </button>
    )
}

export default Button