import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import './index.css';
import Sidebar from './components/SideCarOwner';
import SidebarParking from './components/SidebarParkingOwner';
import Home from './pages/Home';
import ManageCapacity from './components/ManageCapacity';
import LoginPage from './pages/LoginPage';
import SignupPage from './pages/SignupPage';
import UserPannel from './pages/UserPannel';
import RegisterCar from './pages/RegisterCar';
import RegisterParking from './pages/RegisterParking';
import HomaPO from './pages/HomePO';

import EditInfoPage2 from './pages/EditInfoPage2';
import EditCar from './pages/EditCar';
import EditParking from './pages/EditParking';
import ParkingPage from './pages/ParkingPage';
import Panel from './pages/Panel';
import PanelCarOwner from './pages/PanelCarOwner';
import Validation2 from './pages/ValidationPage2';

import Comments from './components/Comments';
import AppHeader from './components/AppHeader';
import { ThemeProvider } from '@mui/material';

import CustomTheme from './assets/CustomTheme';
import PrkingReserve from './pages/ParkingReserve';
import AppHeaderParkingOwner from './components/AppHeaderParkingOwner';
// import PanelCarOwner from './pages/PanelCarOwner';
import ReserveTableCarOwner from './pages/CarOwnerReserves';

import { create } from 'jss';
import rtl from 'jss-rtl';
import { StylesProvider, jssPreset } from '@mui/styles';
import Reservation from './pages/Reservation';

// Configure JSS
const jss = create({
  plugins: [...jssPreset().plugins, rtl()],
});

function App() {
  return (
    <ThemeProvider theme={CustomTheme}>
      <StylesProvider jss={jss}>
        <Router>
          <div className="App">
            <Switch>
              <Route exact path="/">
                <LoginPage />
              </Route>
              <Route exact path="/Signup">
                <SignupPage />
              </Route>
              ///////////////////////////////////ParkingOwner
              side:////////////////////////////////////////////////////
              <Route exact path="/HomeParkingOwner">
                <AppHeaderParkingOwner />
                <HomaPO />
              </Route>
              <Route exact path="/EditParking">
                <AppHeaderParkingOwner />
                <EditParking />
              </Route>
              <Route exact path="/Panel">
                <AppHeaderParkingOwner />
                <Panel />
              </Route>
              <Route exact path="/ValidationPage">
                <AppHeaderParkingOwner />
                <Validation2 />
              </Route>
              <Route exact path="/RegisterParking">
                <AppHeaderParkingOwner />
                <RegisterParking />
              </Route>
              <Route exact path="/PrkingReserve">
                <AppHeaderParkingOwner />
                {/* <ManageCapacity /> */}
                <PrkingReserve />
              </Route>
              <Route exact path="/EditInfo">
                <AppHeader />
                <EditInfoPage2 />
              </Route>
              ///////////////////////////////////CarOwner
              side:////////////////////////////////////////////////////////
              <Route exact path="/UserPannel">
                <AppHeader />
                <UserPannel />
              </Route>
              <Route exact path="/PanelCarOwner">
                <AppHeader />
                <PanelCarOwner />
              </Route>
              <Route exact path="/EditCar">
                <AppHeader />
                <EditCar />
              </Route>
              <Route exact path="/RegisterCar">
                <AppHeader />
                <RegisterCar />
              </Route>
              <Route exact path="/ParkingPage">
                <Reservation />
                {/* <AppHeader />
                <Comments /> */}
              </Route>
              <Route exact path="/CarOwnerReserves">
                <AppHeader />
                <ReserveTableCarOwner />
              </Route>
            </Switch>

            <Route exact path="/AppHeader">
              <AppHeader />
            </Route>
          </div>
        </Router>
      </StylesProvider>
    </ThemeProvider>
  );
}

export default App;
