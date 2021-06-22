import React, { useState } from "react";
import axios from 'axios';
import { Card, Divider, List, Button } from "antd";
import { Tag } from './tag';

export function Article(props) {
    const [tags, setTags] = useState([]);
    const [showButton, setShowButton] = useState(false);
    const [articleTags, setArticleTags] = useState(props.article.Tags);

    const onSelect = value => {
        console.log(value);
        setTags([...tags, value]);
        setShowButton(true);
    }

    const onDeselect = value => {
        console.log(value);
        let temp = [...tags];
        temp = temp.filter((val, index, arr) => {
            return val !== value;
        });
        setTags(temp);
        if(tags.length <= 0)
            setShowButton(false);
    }

    const saveTags = () => {
        console.log(tags);
        axios.post("http://localhost:8080/saveTags", {
            pmid: props.article.PMID,
            tags: tags
        }).then(res => {
            setShowButton(false);
            setArticleTags(res.data);
        }).catch((error) => {
            console.log(error)
        });
    }


    const { article } = props;
    const pmid = "https://pubmed.ncbi.nlm.nih.gov/" + article.PMID;
    return(
        <div>
            <Card title={article.Title} extra={<p>PMID:<a href={pmid}>{article.PMID}</a></p>}>
                <Divider orientation="left">Abstract</Divider>
                <p>{article.Abstract}</p>
                <Divider orientation="left">Authors</Divider>
                <p>{article.Authors.join(", ")}</p>
                <Divider orientation="left">Keywords</Divider>
                <p>{article.Keywords.join(", ")}</p>
                <Divider />
                <Tag onSelect={onSelect} onDeselect={onDeselect}/>
                {articleTags && articleTags.length > 0 && 
                    <List
                        size="small"
                        bordered
                        dataSource={articleTags}
                        renderItem={item => <List.Item>{item}</List.Item>}
                    />}
                {showButton && 
                    <Button type="primary" onClick={saveTags} >
                        Save Tags
                    </Button>   
                }
            </Card>
            <Divider dashed />
        </div>
    );
}