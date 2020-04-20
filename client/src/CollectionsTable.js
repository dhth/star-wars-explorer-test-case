import React from 'react';
import Table from './Table';
import { Link } from "react-router-dom";


class CollectionsTable extends React.Component{
    constructor(props) {
    super(props);
    this.state = {
        isLoading: true,
        data: [],
      newFetchInProcess: false
    };
      this.onFetchAction = this.onFetchAction.bind(this);
  }
  componentDidMount() {
    fetch(this.props.dataSource)
      .then(response => response.json())
      .then(data => {
        this.setState({
          isLoading: false,
          data: data["collections"],
        });
      });
  }

  onFetchAction(){
    this.setState({
      newFetchInProcess: true,
      newFetchFailed: false
    })
    fetch(`http://127.0.0.1:8000/fetch-collection`)
      .then(response => {
        if (response.status !== 200) {
          throw new Error("Not 200 response")
        } else return (response.json());
      })
      .then(data => {
        if (data["success"] === true) {
          const newData = this.state.data.slice()
          newData.unshift(data["collection"]["metadata"])
          this.setState({
            newFetchInProcess: false,
            data: newData,
            newFetchFailed: false
          });
        }
        else {
          this.setState({
            newFetchInProcess: false,
            newFetchFailed: true
          })
        }
      }).catch(error => {
        this.setState({
          newFetchInProcess: false,
          newFetchFailed: true
        })
      });
  }
  render(){

      const columns = [
              {
                  Header: 'ID',
                  accessor: 'id',
                  Cell: e => <Link className="nav-link" to={`/collections/${e.value}`}>
                      {e.value}
                </Link>
              },
              {
                  Header: 'File Name',
                  accessor: 'file_name',
              },
              {
                  Header: 'Date',
                  accessor: 'date',
              },
              {
                  Header: 'Data',
                  accessor: 'data',
                  Cell: (tableInfo) => (
                      <Link to={`/collections/${tableInfo.data[tableInfo.row.index].id}`}>
                          <button type="button" className="btn btn-primary btn-sm">
                              See Data</button>
                      </Link>
                  )
              },
          ]
    const fetchButton = this.state.newFetchInProcess === false ? <div><button type="button" onClick={this.onFetchAction} className="btn btn-success actionButton">
      Fetch
    </button>{this.state.newFetchFailed === true ? <p>Data Fetch failed</p> : null}</div> : <div><button type="button" className="btn btn-secondary actionButton" disabled>
        Fetch in progress
    </button>      
          <div className="spinner-border spinner" role="status">
            <span className="sr-only">Loading...</span>
          </div>
        </div>
    
    let table = null;
      if (this.state.isLoading){
          table = <div>
              <p>Fetching data...</p>
              </div>
      }
      else{
        table = 
          <div>
              <Table columns={columns} data={this.state.data} />
              </div>
      }
    const noDataAvailable = <p className="lead">No data available. Click button to fetch.</p>
    return (
      <div className="container mainContainer">
        <h3>Collections</h3>
        {fetchButton}
        {this.state.data.length > 0 ? table : noDataAvailable}
      </div>
    )
  }
}

export default CollectionsTable;