import React, { useEffect, useState } from "react";
import axios from 'axios';
import { Select } from "antd";
import WBK from 'wikibase-sdk'

const { Option } = Select;

const wbk = WBK({
  instance: 'https://www.wikidata.org',
  sparqlEndpoint: 'https://query.wikidata.org/sparql' // Required to use `sparqlQuery` and `getReverseClaims` functions, optional otherwise
})

const initialState = [];

export function HomePage() {
  const [wikis, setWikis] = useState(initialState);

  let searchValues = [];

  const onSearch = value => {
    console.log(value);
    if(!value && value === "") return;
    let url = wbk.searchEntities({
      search: value,
      format: 'json',
      limit: 10,
      language: 'en'
    });
    console.log("url: " + url)
    let options = []
    setWikis(initialState)
    axios.get(url)
        .then(res => {
          console.log(res.data.search[0]);
          res.data.search.map(item => options.push({id: item.id, description: item.description}))
          // <Option key={item.id}>{item.description}</Option>
          setWikis(options)
        })
        .catch((error) => {
          console.log(error)
        });
  }

  useEffect(() => {
    console.log("wikis:")
    console.log(wikis);
  }, [wikis]);

  return (
    <div>
      <Select
        mode="multiple"
        allowClear={true}
        autoFocus={true}
        autoClearSearchValue={false}
        style={{ width: '100%' }}
        placeholder="Please select"
        defaultValue={searchValues}
        onSearch={onSearch}
      >
        {wikis.map(item => 
          <Option key={item.id}>{item.description}</Option>)}
      </Select>
    </div>
  );
}
