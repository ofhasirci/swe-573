import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.css';
import { HomePage } from './pages/home';
import { CheckData } from "./pages/checkData";
import { Layout, Menu, Breadcrumb } from 'antd';
const { Header, Content, Footer } = Layout;

function App() {
  return (
    <Layout className="layout">
      <Header>
        <div className="logo" />
        <Menu theme="dark" mode="horizontal" defaultSelectedKeys={['1']}>
          <Menu.Item key="1">Search</Menu.Item>
          <Menu.Item key="2">nav 2</Menu.Item>
          <Menu.Item key="3">nav 3</Menu.Item>
        </Menu>
      </Header>
      <Content style={{ padding: '0 50px' }}>
        <Breadcrumb style={{ margin: '16px 0' }}>
          <Breadcrumb.Item>Search</Breadcrumb.Item>
        </Breadcrumb>
        <div className="site-layout-content">
          <Router>
            <Switch>
              <Route path="/checkdata">
                <CheckData></CheckData>
              </Route>

              <Route path="/">
                <HomePage></HomePage>
              </Route>
            </Switch>
          </Router>
        </div>
      </Content>
      <Footer style={{ textAlign: 'center' }}>This is a footer.</Footer>
  </Layout>
  );
}

export default App;
