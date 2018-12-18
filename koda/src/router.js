import React from 'react';
import {
  BrowserRouter,
  Route,
} from 'react-router-dom';
import Search from './Search/Search';
import Records from './Records';

import './router.css';

class KodaRouter extends React.Component {
  render() {
    return (
      <BrowserRouter>
        <div className="main-container">
          <Route exact path="/" component={Search} />
          <Route path="/records" component={Records} />
        </div>
      </BrowserRouter>
    );
  }
}

export default KodaRouter;
