import React, {useState} from 'react';
import './Display.css';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import useSWR from 'swr';
import axios from 'axios';
import { DropdownButton } from 'react-bootstrap';

const fetcher = (url) => axios.get(url).then(res => res.data);

export default function Display(props) {
    return (
        <div className="manager-view-display-frame">
            {props.view === 'inventory' ? (
                <Inventory />
            ) : props.view === 'x-report' ? (
                <XReport />
            ) : props.view === 'z-report' ? (
                <ZReport />
            ) : props.view === 'prices' ? (
                <Prices />
            ) : props.view === 'sales-report' ? (
                <SalesReport />
            ) : props.view === 'excess-report' ? (
                <ExcessReport />
            ) : props.view === 'restock-report' ? (
                <RestockReport />
            ) : props.view === 'what-sells' ? (
                <WhatSells />
            ) : (
                <h1>Welcome Manager, click a button to get started!</h1>
            )}
        </div>
    );
}

function Inventory() {
    const [selectedItem, setSelectedItem] = useState('');
    // fetch information from endpoint
    const { data, error, isLoading } = useSWR('http://localhost:5000/inventory', fetcher);
    if (error) {
        console.error(error);
    }

    if (isLoading || error || data === undefined) {
        return;
    }
    const processedData = JSON.parse(data);

    const restockAll = () => {
        axios.post('http://localhost:5000/inventory', {}
        ).then((res) => {
            console.log(res);
        })
    };

    const setQuantity = () => {
        axios.post('http://localhost:5000/inventory', {'InventoryItem': 'Cheese'}
        ).then((res) => {
            console.log(res);
        })
    };

    return (
        <div>
            <h1>Inventory</h1>
            <div className="inventory-frame">
                <div className='table-container'>
                    <Table className="striped bordered hover">
                        <thead>
                            <tr>
                                {Object.keys(processedData[0]).map((key) => (
                                    <th key={key}>{key}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {processedData.map((item, index) => (
                                <tr key={index}>
                                    {Object.keys(item).map((key) => (
                                        <td key={key}>{item[key]}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </Table>
                </div>
                <div>
                    <Button variant="outline-success" className="inventory-button" onClick={restockAll}>Restock All</Button>
                    <div>
                        <DropdownButton title="Select Item">
                        </DropdownButton>
                        <Button variant="outline-primary" className="inventory-button" onClick={setQuantity}>Set Quantity</Button>
                    </div>
                </div>
            </div>
        </div>
    )
}

function XReport() {
    return (
        <h1>X Report</h1>
    )
}

function ZReport() {
    return (
        <h1>Z Report</h1>
    )
}

function Prices() {
    return (
        <h1>Prices</h1>
    )
}

function SalesReport() {
    return (
        <h1>Sales Report</h1>
    )
}

function ExcessReport() {
    return (
        <h1>Excess Report</h1>
    )
}

function RestockReport() {
    return (
        <h1>Restock Report</h1>
    )
}

function WhatSells() {
    return (
        <h1>What Sells</h1>
    )
}