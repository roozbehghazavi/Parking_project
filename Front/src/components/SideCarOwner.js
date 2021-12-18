import React, { useState, useEffect } from 'react';

//All the svg files
import logo from '../assets/logo.svg';
import Home from '../assets/home-solid.svg';
import setting from '../assets/settings.svg';
import PowerOff from '../assets/power-off-solid.svg';
import styled from 'styled-components';
import car from '../assets/car.svg';
import parking from '../assets/parking.svg';
import { NavLink, useHistory } from 'react-router-dom';
import * as RiIcons from 'react-icons/ri';
import '../css/side.css';
//import { useHistory } from 'react-router';
// import CarsList from './userpannel/CarsList';
import axios from 'axios';

// const Container = styled.div`
//   position: fixed;

//   .active {
//     border-right: 4px solid var(--white);

//     img {
//       filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(93deg)
//         brightness(103%) contrast(103%);
//     }
//   }
// `;

const Button = styled.button`
  background-color: var(--grey);
  border: none;
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  margin: 0.5rem 7px 0 0.5rem;
  cursor: pointer;

  display: flex;
  justify-content: center;
  align-items: center;

  position: relative;

  &::before,
  &::after {
    content: '';
    background-color: var(--white);
    height: 2px;
    width: 1rem;
    position: absolute;
    transition: all 0.3s ease;
  }

  &::before {
    top: ${(props) => (props.clicked ? '1.5' : '1rem')};
    transform: ${(props) => (props.clicked ? 'rotate(135deg)' : 'rotate(0)')};
  }

  &::after {
    top: ${(props) => (props.clicked ? '1.2' : '1.5rem')};
    transform: ${(props) => (props.clicked ? 'rotate(-135deg)' : 'rotate(0)')};
  }
`;

// const SidebarContainer = styled.div`
//   background-color: var(--black);
//   width: 3.5rem;
//   height: 80vh;
//   margin-top: 1rem;
//   border-radius: 30px 0 0 30px;
//   padding: 1rem 0;

//   display: flex;
//   flex-direction: column;
//   align-items: center;
//   justify-content: space-between;

//   position: absolute;
//   right: 0;
// `;

// const Logo = styled.div`
//   width: 2rem;

//   img {
//     width: 100%;
//     height: auto;
//   }
// `;

const SlickBar = styled.ul`
  color: var(--white);
  list-style: none;
  display: flex;
  flex-direction: column;

  justify-content: center;
  background-color: #5d6d7e;
  // direction: rtl;

  padding: 2rem 0;

  position: absolute;
  top: 6rem;
  right: 0;

  width: ${(props) => (props.clicked ? '12rem' : '3.5rem')};
  // right: ${(props) => (props.clicked ? '0' : '-100%')};
  transition: all 0.5s ease;
  border-radius: 30px 0 0 30px;
`;

const Item = styled(NavLink)`
  text-decoration: none;
  color: var(--white);
  width: 100%;
  padding: 1.05rem 0;
  padding-right: 1rem;
  cursor: pointer;

  display: flex;
  padding-left: 1rem;

  &:hover {
    border-right: 4px solid var(--white);

    img {
      filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(93deg)
        brightness(103%) contrast(103%);
    }
  }

  img {
    width: 1.2rem;
    height: auto;
    filter: invert(92%) sepia(4%) saturate(1033%) hue-rotate(169deg)
      brightness(78%) contrast(85%);
  }
`;

const Text = styled.span`
  direction: rtl;
  // width: ${(props) => (props.clicked ? '100%' : '0')};
  width: 200px;
  overflow: hidden;
  margin-right: ${(props) => (props.clicked ? '1.5rem' : '0')};
  transition: all 0.3s ease;
`;

const Profile = styled.div`
  width: ${(props) => (props.clicked ? '-14rem' : '3rem')};
  height: 3rem;

  padding: 0.5rem 1rem;
  /* border: 2px solid var(--white); */
  border-radius: 20px;
  margin: 0 7px 0 0.7rem;

  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: ${(props) => (props.clicked ? '9rem' : '0')};

  color: var(--white);

  transition: all 0.3s ease;

  img {
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 50%;
    cursor: pointer;

    &:hover {
      border: 2px solid var(--grey);
      padding: 2px;
    }
  }
`;

const Details = styled.div`
  display: ${(props) => (props.clicked ? 'flex' : 'none')};
  justify-content: space-between;
  align-items: center;
`;

const Name = styled.div`
  padding: 0 1.5rem;

  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;

  h4 {
    display: inline-block;
  }

  a {
    font-size: 0.8rem;
    text-decoration: none;
    color: var(--grey);

    &:hover {
      text-decoration: underline;
    }
  }
`;

// const Logout = styled.button`
//   border: none;
//   width: 2rem;
//   height: 2rem;
//   background-color: transparent;
//   // padding-left: 3 px;
//   margin: 0 7px 0 0.7rem;
//   img {
//     width: 100%;
//     height: auto;
//     filter: invert(15%) sepia(70%) saturate(6573%) hue-rotate(2deg)
//       brightness(100%) contrast(126%);
//     transition: all 0.3s ease;
//     &:hover {
//       border: none;
//       padding: 0;
//       opacity: 0.5;
//     }
//   }
// `;

const Sidebar = () => {
  const [click, setClick] = useState(false);
  const handleClick = () => setClick(!click);

  const history = useHistory();

  const [CarDropdown, setCarDropdown] = useState(false);
  const handleCarDropDown = (e) => {
    if (CarDropdown === false) {
      setCarDropdown(true);
    } else {
      setCarDropdown(false);
    }
  };

  const [HomeTab, setHomeTab] = useState(false);
  const handleSetHomeTab = (e) => {
    if (HomeTab === false) {
      setHomeTab(true);
    } else {
      setHomeTab(false);
    }
  };

  const [profileClick, setprofileClick] = useState(false);
  const handleProfileClick = () => setprofileClick(!profileClick);

  //=================================================================================================
  const [cars, setCars] = useState([]);

  let token = localStorage.getItem('ctoken');
  let auth = `Token ${token}`;

  useEffect(() => {
    axios
      .get('http://127.0.0.1:8000/carowner/carlist/', {
        headers: { 'Content-Type': 'application/json', Authorization: auth },
      })
      .then((res) => {
        //console.log(res.data.results);
        setCars(res.data.results);
        //console.log(cars);
      })
      .catch((e) => {
        console.log('error occured in fetch');
      });
  }, []);

  //=====================================================================================================

  return (
    <div className="Container" style={{ zIndex: '5' }}>
      <Button clicked={click} onClick={() => handleClick()}></Button>
      <div className="SidebarContainer">
        {/* <img src={logo} alt="logo" /> */}
        {/* src="https://picsum.photos/200" */}
        <img className="Logo img-fluid w-100 rounded" alt="Profile" />

        <SlickBar
          // className="d-flex justify-content-center flex-column"
          clicked={click}
          className="d-flex flex-column align-items-center justify-content-center py-5"
        >
          <Item
            exact
            activeClassName="active"
            to="/UserPannel"
            className="mb-3"
          >
            <img src={Home} alt="Home" className="itemimages" />
            {click ? <Text clicked={handleSetHomeTab}>خانه</Text> : null}
          </Item>

          <Item
            // className="d-flex justify-content-center align-items-center"
            // activeClassName="active d-flex justify-content-center align-items-center"
            to="/UserPannel"
            className="mx-auto mb-3 w-100"
          >
            <img
              src={car}
              alt="Car"
              className="img-fluid"
              style={{ fill: 'red' }}
            />
            {click ? (
              <div
                // className="justify-content-center align-items-center d-flex"
                style={{ paddingRight: '65px' }}
              >
                <button
                  onClick={handleCarDropDown}
                  style={{ zIndex: '500', color: 'white' }}
                >
                  <div className="mx-auto">
                    ماشین
                    <RiIcons.RiArrowDownSFill style={{ marginRight: '15px' }} />
                  </div>
                </button>
                {CarDropdown ? (
                  <div className="d-flex flex-column justify-content-center">
                    <tbody>
                      {cars.map(function (car) {
                        return (
                          <Item to="/EditCar">
                            <button
                              className="div text-light"
                              key={car.id}
                              onClick={() => {
                                localStorage.setItem('carId', car.id);
                                localStorage.setItem('carName', car.carName);
                                localStorage.setItem('carColor', car.color);
                                localStorage.setItem('carPelak', car.pelak);
                              }}
                              style={{ paddingTop: '15px' }}
                            >
                              {car.carName}
                            </button>
                          </Item>
                        );
                      })}
                    </tbody>

                    <Item
                      // exact
                      // activeClassName="active"
                      to="/RegisterCar"
                    >
                      <button
                        className="addBtn"
                        style={{
                          paddingTop: '15px',
                          color: 'white',
                        }}
                        onClick={(e) => {
                          history.push('/RegisterCar');
                        }}
                      >
                        اضافه کردن
                      </button>
                    </Item>
                  </div>
                ) : null}
              </div>
            ) : null}

            {/* {SidebarData.map((item, index) => {
              return <SubMenu item={item} key={index} />;
            })} */}
          </Item>
          <Item
            onClick={() => setClick(false)}
            exact
            activeClassName="active"
            to="/EditInfo"
          >
            <img src={setting} alt="Home" />
            {click ? <Text clicked={handleSetHomeTab}>پروفایل</Text> : null}
          </Item>
        </SlickBar>

        <button className="Logout">
          <img src={PowerOff} alt="logout" />
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
