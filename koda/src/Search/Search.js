import React, { Component } from 'react';
import {
  Input,
} from 'antd';
// import { withRouter } from 'react-router';
import './Search.css';
import RecordStore from './stores';

const InputSearch = Input.Search;


class Search extends Component {
  handlerSearch = async (value) => {
    await RecordStore.getRecords(value);
    const { history } = this.props;
    history.push('/records');
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
