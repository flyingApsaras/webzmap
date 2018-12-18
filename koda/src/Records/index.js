import React from 'react';
import {
  Card,
} from 'antd';
import RecordStore from '../Search/stores';

import './index.css';

class Records extends React.Component {
  renderResult = (result, resultComponents) => {
    for (const key in result) {
      if (typeof result[key] !== 'object') {
        resultComponents.push(
          <span key={key}>
            {key} 
            : 
            {result[key]}
          </span>,
        );
      } else {
        this.renderResult(result[key], resultComponents);
      }
    }
  }

  renderRecord = (record) => {
    const { _source: { ip, data } } = record;
    const protocol = Object.keys(data)[0];
    const resultComponents = [];
    const { timestamp, result } = data[protocol];  
    this.renderResult(result, resultComponents);
    console.log(resultComponents);
    return (
      <Card className="record" key={record._source.ip}>
        <div className="record-meta-info">
          <span>
            <a href={'http://'.concat(ip)}>{ip}</a>
          </span>
          <span> 
            扫描时间: 
            { timestamp }
          </span>
          <span>
            {protocol}
          </span>
        </div>
        
        <div className="record-result">
          { resultComponents }
        </div>
      </Card>
    );
  }

  render() {
    const records = RecordStore.records.map((item) => {
      return this.renderRecord(item);
    });
    return (
      <div className="records-container">
        {records.length !== 0
          ? records 
          : '记录空'
        }
      </div>
    );  
  }
}

export default Records;
