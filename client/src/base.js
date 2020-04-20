import React from 'react';
import CollectionsTable from './CollectionsTable';

class Base extends React.Component {
    render() {
        return (
            <CollectionsTable dataSource="http://127.0.0.1:8000/collections"></CollectionsTable>
        )
    }
}

export default Base;