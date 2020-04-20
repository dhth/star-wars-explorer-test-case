import React from 'react';
import { Route, Link, Router } from "react-router-dom";
import { appInfo } from './appInfo';
// import AboutPage from "./AboutPage";
import Base from './base';
import CollectionTable from './CollectionTable';
import CollectionValueCountsTable from './CollectionValueCountsTable';

class Nav extends React.Component {
    render() {
        // const urlsJSX = urls["US"].map(x => <Link className="dropdown-item" to=x.url>
        //     x.title</Link>);
        return (
            <Router history={this.props.history}>
                <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
                    <Link className="navbar-brand" to="/">
                        {appInfo.appName}
                    </Link>

                    <button
                        className="navbar-toggler"
                        type="button"
                        data-toggle="collapse"
                        data-target="#navbarNavDropdown"
                        aria-controls="navbarNavDropdown"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon" />
                    </button>
                    <div className="collapse navbar-collapse" id="navbarNavDropdown">
                        <ul className="navbar-nav">

                        <li className="nav-item">
                        <Link className="nav-link" to="/">
                        Collections
                        </Link>
                        </li>
                        </ul>
                    </div>
                    <div className="collapse navbar-collapse justify-content-end" id="navbarCollapse">
                        <ul className="navbar-nav">
                            <li className="nav-item">
                                <small>by dhruv</small>
                            </li>
                        </ul>
                    </div>

                </nav>
                {/* routes */}
                <Route exact path="/" render={props => <Base />} />
                <Route path='/collections/:collectionId/value-counts/' component={CollectionValueCountsTable} ></Route>
                <Route exact path='/collections/:collectionId/' component={CollectionTable} />
                {/* <Route path="/about" render={props => <AboutPage />} /> */}
            </Router>
        );
    }
}

export default Nav;