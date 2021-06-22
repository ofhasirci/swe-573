import React, { useState } from "react";
import axios from 'axios';
import Iframe from 'react-iframe'
import { Row, Col, Button, Divider, Pagination } from "antd";
import { Tag } from "../component/tag";
import { Article } from "../component/article";


export function HomePage() {
  const [articles, setArticles] = useState([]);
  const [ldaUrl, setLdaurl] = useState(null);
  const [numOfArticle, setNumOfArticle] = useState(null);
  const [classNumber, setClassNumber] = useState(null);

  let searchValues = [];

  const onSelect = value => {
    console.log(value);
    let res = value.split(':');
    searchValues.push(res[0]);
  }

  const onDeselect = value => {
    console.log(value);
    let res = value.split(':');
    searchValues = searchValues.filter((value, index, arr) => {
      return value !== res[0];
    });
  }

  const getArticles = () => {
    if (searchValues.length === 0) return;
    axios.post("http://207.154.210.239:8080/search", {
      terms: searchValues,
      offset: 0,
      count: 10
    }).then(res => {
      console.log(res.data.articles[9].Tags);
      setArticles(res.data.articles);
      setLdaurl(res.data.ldaUrl);
      setNumOfArticle(res.data.numOfArticle);
      setClassNumber(res.data.classNumber);
    }).catch((error) => {
        console.log(error)
    });
  }

  const clearPage = () => {
    setArticles([]);
    setLdaurl(null);
    setNumOfArticle(null);
    setClassNumber(null)
    searchValues = [];
  }

  const changePage = (page, pageSize) => {
    console.log(page);
    axios.post("http://207.154.210.239:8080/pagination", {
      offset: page-1,
      count: 10,
      class_no: classNumber
    }).then(res => {
      setArticles(res.data);
    }).catch((error) => {
      console.log(error)
    });
  }

  return (
    <div>
      <Tag onSelect={onSelect} onDeselect={onDeselect}/>
      <Row>
        <Col span={8}/>
        <Col span={8}>
          <Button type="primary" onClick={getArticles}>Bring Articles</Button>
          <Divider type="vertical"/>
          <Button type="primary" onClick={clearPage}>Clear</Button>
        </Col>
      </Row>
      <Divider />
      <Row>
        <Col span={2}></Col>
        <Col span={8}>
          {ldaUrl && 
          <Iframe url={ldaUrl} width="900px" height="1000px" />
          }
        </Col>
      </Row>
      <Divider />
      <Row>
        {numOfArticle && 
          <div>
            <p>Number of articles on this topics: {numOfArticle}</p>
            <br/>
            {classNumber && <p>Class number of articles: {classNumber + 1}</p>}
          </div>}
      </Row>
      <Divider />
      <Row>
        <Col span={24}>
          {articles.length > 0 &&
            articles.map((value, index, arr) => {
              return <Article key={value.PMID} article={value} />
            }) 
          }
        </Col>
      </Row>
      <Row>
        <Col span={24}>
          {numOfArticle && 
            <Pagination total={numOfArticle} onChange={changePage}/>
          }
        </Col>
      </Row>
    </div>
  );
}
