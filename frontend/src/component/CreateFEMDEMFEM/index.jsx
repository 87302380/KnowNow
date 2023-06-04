import React, {Component} from 'react';
import {Button, Form, Input} from "antd";

import 'antd/dist/antd.css';

class Index extends Component {
    render() {
        return (
            <div>
                <Form onFinish={this.onFinish}>
                <Form.Item label="BT-Design-Parameter eingeben" name="keyWord">
                        <Input />
                    </Form.Item>
                    <Form.Item style={{ textAlign: 'right' }}>
                        <Button type="primary" htmlType="submit" >
                        Bestätigt
                        </Button>
                    </Form.Item>
                </Form>
            </div>
        )
            ;
    }

    onFinish() {
        console.log("finish")
    }
}
export default Index;