import React, { Component } from 'react';
import { Form, Input, Button, Table } from 'antd';
import 'antd/dist/antd.css';
import styles from './SparqlQuery.module.css';

class SparqlQuery extends Component {
  state = {
    data: [],
    columns: [],
    loading: false,
  };

  onFinish = (values) => {
    this.setState({ loading: true });
    fetch('/sparqlquery/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ sparql: values.query }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log('Success:', data);
        const columns = Object.keys(data[0] || {}).map((key) => ({
          title: key,
          dataIndex: key,
          key: key,
        }));
        this.setState({ data: data, columns: columns, loading: false });
      })
      .catch((error) => {
        console.error('Error:', error);
        this.setState({ loading: false });
      });
  };

  render() {
    const { data, columns, loading } = this.state;

    return (
      <div className={styles.container} >
        <Form onFinish={this.onFinish}>
          <Form.Item
            label="SPARQL Query"
            name="query"
            rules={[{ required: true, message: 'Please input your SPARQL Query!' }]}
          >
            <Input.TextArea autoSize={{ minRows: 3 }} />
          </Form.Item>
          <Form.Item style={{ textAlign: 'right' }}>
            <Button type="primary" htmlType="submit" disabled={loading}>
              {loading ? 'Loading' : 'Submit'}
            </Button>
          </Form.Item>
        </Form>
        <div className={styles.tableContainer}>
          <Table dataSource={data} columns={columns} key="table" scroll={{ y: 400 }} />
        </div>
      </div>
    );
  }
}

export default SparqlQuery;
