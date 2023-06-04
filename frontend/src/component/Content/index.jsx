import React, { Component } from 'react';
import PubSub from 'pubsub-js';
import Search from '../Search';
import Upload from '../UploadFile';
import CreateFEMDEMFEM from '../CreateFEMDEMFEM';
import CreateLaminierSimulation from '../CreateLaminierSimulation';
import styles from './index.module.css';

class Content extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeKey: 0,
    };
    this.onGetActive = this.onGetActive.bind(this); // 绑定 this
  }

  componentDidMount() {
    const { state } = this;
    state.pubsub = PubSub.subscribe('getKey', (_, key) => this.onGetActive(key)); // 绑定 PubSub 事件
    this.setState(state);
    PubSub.subscribe('getKey', (_, key) => this.onGetActive(key)); // 绑定 PubSub 事件
  }

  onGetActive(key) {
    const { state } = this;
    state.activeKey = key;
    this.setState(state);
  }

  render() {
    const { activeKey } = this.state; // 解构出 state 中的 activeKey
    const titleMap = ['SparqlQuery', 'Hochladen', 'FEM-DEM-FEM Simulation', 'Laminiersimulation']; // 标题数组
    const Title = titleMap[activeKey]; // 通过索引获取标题文本
    const ContentComponent = [Search, Upload, CreateFEMDEMFEM, CreateLaminierSimulation][activeKey]; // 通过索引获取渲染的组件
    return (
      <div className={styles.wrapper}>
        <div className={styles.container}>
          <h2 className={styles.title}>
            <span>{Title}</span>
          </h2>
          <ContentComponent />
        </div>
      </div>
    );
  }
}

export default Content;
