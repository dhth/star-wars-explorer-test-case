import React from 'react';
import Table from './Table';
import { Link } from "react-router-dom";

class CollectionValueCountsTable extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoading: true,
            data: [],
            tableFields: [],
            allFields: ["name",
                "height",
                "mass",
                "hair_color",
                "skin_color",
                "eye_color",
                "birth_year",
                "gender",
                "homeworld",
                "date"],
            chosenFields: ['birth_year', 'homeworld']
        };
        this.handleButtonClick = this.handleButtonClick.bind(this);
        this.onClickAction = this.onClickAction.bind(this);
    }

    componentDidMount() {
        const { collectionId } = this.props.match.params
        this.setState({
            collectionId: collectionId
        })
        this.loadData(this.state.chosenFields);
    }

    handleButtonClick() {
        // this.loadData(this.state.currentPage + 1);
    }

    onClickAction(event) {
        let indexOf = this.state.chosenFields.indexOf(event.target.value)
        let selectedTagsCloned = this.state.chosenFields.slice();
        if (indexOf === -1) {
            selectedTagsCloned.push(event.target.value);
        }
        else {
            selectedTagsCloned.splice(indexOf, 1);
        }
        if (selectedTagsCloned.length > 0){
            this.loadData(selectedTagsCloned);
        }

    }

    loadData(chosenFields) {
        this.setState({
            isLoading: true,
            fetchFailed: false})
        const { collectionId } = this.props.match.params
        fetch(`http://127.0.0.1:8000/collections/value_counts/${collectionId}?fields=${chosenFields.join(',')}`)
            .then(response => response.json())
            .then(data => {
                if (data["success"] === true) {
                    this.setState({
                        collectionId: collectionId,
                        isLoading: false,
                        data: data["value_counts"]["data"],
                        tableFields: data["value_counts"]["fields"],
                        metadata: data["value_counts"]["metadata"],
                        chosenFields: chosenFields
                    });
                }
                else {
                    this.setState({
                        fetchFailed: true
                    })
                }
            });
    }
    
    render() {
        const buttons = <div className="tagsFilter">
        <p className="h5">Filter by Fields:</p>
        {
            this.state.allFields.map((tag, k) => {
                if (this.state.chosenFields.includes(tag)) {
                    return <button key={`tagFilterButton-${k}`} type="button" onClick={this.onClickAction} className="btn btn-dark filterButton" value={tag}>
                        {tag}
                    </button>
                }
                else {
                    return <button key={`tagFilterButton-${k}`} type="button" onClick={this.onClickAction} className="btn btn-light filterButton" value={tag}>
                        {tag}
                    </button>
                }
            })
        }
        </div>
        let table = null;
        
        if (!this.state.isLoading) {
            const columns = this.state.tableFields.map(x => { return { Header: x, accessor: x } });
            table = (
                <div>
                    <h3>{`Value Counts: ${this.state.metadata["file_name"]}`}</h3>
                    <Table columns={columns} data={this.state.data} />
                </div>
            )
        }
        return (
            <div className="container mainContainer">
                
                {buttons}
                <hr></hr>
                <Link to={`/collections/${this.state.collectionId}/`}>
                    <button type="button" className="btn btn-primary actionButton">
                        See Data
                              </button>
                </Link>
                {table}
            </div>
        )
        
    }
}

export default CollectionValueCountsTable;