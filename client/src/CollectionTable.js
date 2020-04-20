import React from 'react';
import Table from './Table';
import { Link } from "react-router-dom";

class CollectionTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            data: [],
            fields: [],
            currentPage: 0,
            endReached: false
        };
        this.handleButtonClick = this.handleButtonClick.bind(this);    
    }
    componentDidMount() {
        const { collectionId } = this.props.match.params
        this.setState({
            collectionId: collectionId
        })
        this.loadData(this.state.currentPage+1);
    }
    handleButtonClick(){
        this.loadData(this.state.currentPage+1);
    }

    loadData(page_num){
        const { collectionId } = this.props.match.params
        fetch(`http://127.0.0.1:8000/collections/${collectionId}?page_num=${page_num}`)
            .then(response => response.json())
            .then(data => {
                if (data["success"] === true){
                    const fields = data["collection"]["fields"]
                    const index = fields.indexOf("person_collection");
                    if (index > -1) {
                        fields.splice(index, 1);
                    }
                    this.setState({
                        collectionId: collectionId,
                        isLoading: false,
                        data: this.state.data.concat(data["collection"]["data"]),
                        fields: fields,
                        metadata: data["collection"]["metadata"],
                        currentPage: this.state.currentPage+1
                    });
                }
                else if (data["detail"] === "page_num exceeded limit"){
                    this.setState({
                        endReached: true})
                }
            });
    }
    render() {

        const columns = this.state.fields.map(x => { return { Header: x, accessor: x } });
        let table = null;
        if (this.state.isLoading) {
            table = <div>
                <p>Fetching data...</p>
            </div>
        }
        else {
            table = (
                <div>
                    <h3>{`Collection: ${this.state.metadata["file_name"]}`}</h3>
                    <hr></hr>
                    <Link to={`/collections/${this.state.collectionId}/value-counts`}>
                        <button type="button" className="btn btn-primary actionButton">
                            Value Counts
                              </button>
                    </Link>
                    <Table columns={columns} data={this.state.data} />
                    { this.state.endReached === false ? 
                        <button type="button" className="btn btn-secondary btn-sm loadMoreButton" onClick={this.handleButtonClick}>
                            Load More
                              </button> : <button type="button" className="btn btn-warning btn-sm loadMoreButton" disabled>
                            Reached end
                              </button>}
                    
                </div>
            )
        }
        return (
            <div className="container mainContainer">
                {table}
            </div>
        )
    }
}

export default CollectionTable;