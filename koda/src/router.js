import React from 'react';
import {
  BrowserRouter,
  Route,
} from 'react-router-dom';
import Search from './Search/Search';

import './router.css';

class KodaRouter extends React.Component{
  render() {
    return (
      <BrowserRouter>
        <div className="main-container">
          <Route exact path="/" component={Search} />
        </div>
      </BrowserRouter>
    )
  }
}

export default KodaRouter;
