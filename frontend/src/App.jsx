import React, {Component} from 'react';

import Navagtion from "./component/Navagtion"
import Content from "./component/Content"
import This from "./index.module.css"

class App extends Component {
    render() {
        return (
            <div className={This.wrapper}>
                <div className={This['nav-wrapper']}>
                    <Navagtion/>
                </div>
                <div className={This['content-wrapper']}>
                    <Content/>
                </div>
            </div>
        );
    }
}

export default App;