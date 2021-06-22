import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.css';
import { HomePage } from './pages/home';
import { CheckData } from "./pages/checkData";
import { Layout, Menu, Breadcrumb } from 'antd';
const { Header, Content, Footer } = Layout;

function App() {
  return (
    <Router>
      <Layout className="layout">
        <Header>
          <div className="logo" />
          <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
            <Menu.Item key="1">Search</Menu.Item>
          </Menu>
        </Header>
          <Content style={{ padding: '0 50px' }}>
            <Breadcrumb style={{ margin: '16px 0' }}>
              <Breadcrumb.Item>Search</Breadcrumb.Item>
            </Breadcrumb>
            <div className="site-layout-content">
              <Switch>
                <Route path="/checkdata">
                  <CheckData></CheckData>
                </Route>

                <Route path="/">
                  <HomePage></HomePage>
                </Route>
              </Switch>
            </div>
          </Content>
        <Footer style={{ textAlign: 'center' }}>This is a footer.</Footer>
      </Layout>
    </Router>
  );
}

export default App;
