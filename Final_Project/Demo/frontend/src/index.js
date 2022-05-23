import React, {useState} from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import {BrowserRouter, Switch, Route, Redirect} from "react-router-dom"
import Register from './components/Register';
import ChangePassword from './components/ChangePassword';
import Login from './components/Login';
import CurriculumVitaes from './components/CurriculumVitaes';
import UnrolledCV from './components/UnrolledCV';

/**
 * 
 * get the access_token from localStorage
 * 
 * 
 * 
 */
function getToken(){
  const tokenString = localStorage.getItem("access_token");
  const userToken = JSON.parse(tokenString);
  return userToken
}

/**
 * 
 * get the refresh_token from localStorage
 * 
 * 
 * 
 */
function getRefreshToken(){
  const tokenString = localStorage.getItem("refresh_token");
  const userToken = JSON.parse(tokenString);
  return userToken
}

function App(){
  const [token,setToken] = useState(() =>getToken())
  const [refresh_token, setRefreshToken] = useState(() => getRefreshToken())
  return (
    <BrowserRouter>
      <Switch>

        <Route exact path="/">
          {!token ? <Redirect to="login"/>:<Redirect to="/CurriculumVitaes"/>}
        </Route>

        <Route path="/register">
          <Register setToken={setToken} setRefreshToken = {setRefreshToken}/>
        </Route>

        <Route path="/login">
          <Login setToken={setToken} setRefreshToken = {setRefreshToken}/>
        </Route>

        <Route path="/CurriculumVitaes">
          {!token ? <Redirect to="login"/>:<CurriculumVitaes token = {token} refresh_token={refresh_token} setToken={setToken} />}
        </Route>

        <Route path={"/change_password"}>
          <ChangePassword/>
        </Route>

        <Route path="/unfolded">
          <UnrolledCV/>
        </Route>
      </Switch>
    </BrowserRouter>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(

    <App />,

);



