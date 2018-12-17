import React, { Component } from 'react';
import {
  Input,
} from 'antd';
import './Search.css';

const InputSearch = Input.Search;

class Search extends Component {
  handlerSearch = (value) => {
    console.log(value)
  };
  render() {
    return (
      <div className="search-background">
        <div className="search-content">
          <div className="search-title">
            <span className="yehei-font search-main-title">工控态势感知</span>
            <span className="arial-font">Industrial Control Situational Awareness</span>
          </div>
          <div className="middle">
            <InputSearch 
              className="search-input"
              placeholder="输入设备型号: modbus,siemens"
              enterButton
              size="large"
              onSearch={this.handlerSearch}
            />
          </div>
        </div>
      </div>
    );
  }
}

export default Search;
