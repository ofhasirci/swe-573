import 'antd/dist/antd.css';
import React from "react";
import {Input} from "antd";
const { Search } = Input;

const onSearch = value => console.log(value);

export function CheckData() {
  return (
    <div>
        <Search
            placeholder="Search"
            allowClear
            enterButton="Search"
            size="large"
            onSearch={onSearch}
        />
    </div>
  );
}
