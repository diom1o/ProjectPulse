import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import axios from 'axios';
import App from './App';
import LoginPage from './pages/LoginPage';
import NotFoundPage from './pages/NotFoundPage';
axios.defaults.baseURL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:5000';
const Main = () => {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={App} />
        <Route path="/login" component={LoginPage} />
        <Route component={NotFoundPage} />
      </Switch>
    </Router>
  );
};
ReactDOM.render(<Main />, document.getElementById('root'));