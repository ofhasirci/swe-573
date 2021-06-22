import React, { useState } from "react";
import axios from 'axios';
import { Select, Input, Row, Col } from "antd";
import WBK from 'wikibase-sdk'

const { Option } = Select;
const { Search } = Input;

const wbk = WBK({
    instance: 'https://www.wikidata.org',
    sparqlEndpoint: 'https://query.wikidata.org/sparql' // Required to use `sparqlQuery` and `getReverseClaims` functions, optional otherwise
});


export function Tag(props) {
    const [wikis, setWikis] = useState([]);

    const onSearch = value => {
        if (!value && value === "") return;
        let url = wbk.searchEntities({
            search: value,
            format: 'json',
            limit: 10,
            language: 'en'
        });
        let options = []
        setWikis([])
        axios.get(url)
            .then(res => {
                res.data.search.map(item => options.push({ id: item.id, description: item.description }))
                setWikis(options)
            })
            .catch((error) => {
                console.log(error)
            });
    }

    return (
        <Row>
            <Col span={24}>
                <Search
                    placeholder="Search Term"
                    allowClear
                    enterButton="Search"
                    onSearch={onSearch}
                />
                <Select
                    mode="multiple"
                    allowClear={true}
                    autoFocus={true}
                    autoClearSearchValue={false}
                    style={{ width: '100%' }}
                    placeholder="Please select wikis"
                    onSelect={props.onSelect}
                    onDeselect={props.onDeselect}
                >
                    {wikis.map(item =>
                        <Option key={item.id+ ":" +item.description}>{item.id + ":" +item.description}</Option>)}
                </Select>
            </Col>
        </Row>
    );
}