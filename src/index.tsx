import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';
import HomePage from './App';
import LoginPage from './pages/LoginPage';
import PageNotFound from './pages/NotFoundPage';

axios.defaults.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const MainRouter = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route path="/login" component={LoginPage} />
        <Route component={PageNotFound} />
      </Switch>
    </Router>
  );
};

ReactDOM.render(<MainRouter />, document.getElementById('root'));