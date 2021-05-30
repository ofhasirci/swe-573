import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import './App.css';
import { HomePage } from './pages/home';
import { CheckData } from "./pages/checkData";

function App() {
  return (
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
  );
}

export default App;
