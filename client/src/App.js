import React from 'react';
import './styles.scss';
import { createBrowserHistory } from 'history';
import Nav from './Nav';
import 'bootstrap/dist/css/bootstrap.css';

var history = createBrowserHistory();

function App() {
  return (
    <div  >
      {/* <Base/> */}
      <Nav history={history} />
    </div>

  );
}

export default App;