import React, {Component} from 'react';

import styles from "./index.module.css"
import PubSub from "pubsub-js";

class Nav extends Component {

    constructor(props) {
        super(props);
        this.state = {activeKey: 0}
        this.$refs = {}

        this.onChange = this.onChange.bind(this)
    }


    render() {
        return (
            <ul className={styles.nav} ref={c => this.$refs.navList = c}>
                <li className={`${styles.item} ${styles.active}`} onClick={() => this.onChange(0)}>
                    <a href="#">Abfragen</a>
                </li>
                <li className={styles.item} onClick={() => this.onChange(1)}>
                    <a href="#">Hochladen</a>
                </li>
                <li className={styles.item} onClick={() => this.onChange(2)}>
                    <a href="#">FEM-DEM-FEM Simulation</a>
                </li>
                <li className={styles.item} onClick={() => this.onChange(3)}>
                    <a href="#">Laminiersimulation</a>
                </li>
            </ul>
        )
            ;
    }

    onChange(key) {
        const navList = this.$refs.navList.children
        for (let element of navList) {
            element.className = `${styles.item}`
        }
        navList[key].className += ` ${styles.active}`
        PubSub.publish("getKey",key)
    }
}

export default Nav;