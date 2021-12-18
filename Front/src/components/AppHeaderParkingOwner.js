import * as React from "react";
import { useState, useEffect } from "react";
import { useHistory, useLocation } from "react-router-dom";
import axios from "axios";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import PowerSettingsNewRoundedIcon from "@mui/icons-material/PowerSettingsNewRounded";

import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";

import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemIcon from "@mui/material/ListItemIcon";

import { SwipeableDrawer } from "@mui/material";
import { Avatar } from "@mui/material";
import defpro from "./../images/defaultProPic.png";
import HomeIcon from "@mui/icons-material/Home";
import "./../css/headAndSide.css";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";
import DirectionsCarIcon from "@mui/icons-material/DirectionsCar";
import Collapse from "@mui/material/Collapse";
import KeyIcon from "@mui/icons-material/Key";
import AddIcon from "@mui/icons-material/Add";
import PersonIcon from "@mui/icons-material/Person";
import { GiHomeGarage } from "react-icons/gi";
import LocalParkingIcon from "@mui/icons-material/LocalParking";

const drawerWidth = 240;
const homeString = "خانه";

const AppHeaderParkingOwner = (props) => {
  const histo = useHistory();
  const [profilePhoto, setProfilePhoto] = useState(defpro);
  const [email, setEmail] = useState("");
  const [parkings, setParkings] = useState([]);
  const [parkingStyle, setParkingStyle] = useState(false);

  const [open, setOpen] = useState(false);

  const [isHome, setIsHome] = useState(true);
  const [isParkings, setIsParkings] = useState(false);
  const [isProfile, setIsProfile] = useState(false);

  let location = useLocation();

  const handleCarOpen = () => {
    setOpen(!open);
  };

  let token = localStorage.getItem("ptoken");
  let auth = `Token ${token}`;

  useEffect(() => {
    if (location.pathname == "/Home") {
      setIsHome(true);
      setIsParkings(false);
      setIsProfile(false);
    } else if (location.pathname == "/Panel") {
      setIsHome(false);
      setIsParkings(true);
      setIsProfile(false);
    } else if (location.pathname == "/EditInfo") {
      setIsHome(false);
      setIsParkings(false);
      setIsProfile(true);
    }
    // data fetch///
    // User Info
    axios
      .get("http://127.0.0.1:8000/users/rest-auth/user/", {
        headers: { "Content-Type": "application/json", Authorization: auth },
      })
      .then((res) => {
        if (res.data.profilePhoto != null)
          setProfilePhoto(res.data.profilePhoto);

        setEmail(res.data.email);
      });

    ///////////
    axios
      .get("http://127.0.0.1:8000/parkingowner/parkinglist", {
        headers: { "Content-Type": "application/json", Authorization: auth },
      })
      .then((res) => {
        //console.log(res.data.results);
        setParkings(res.data.results);
        //console.log(cars);
      })
      .catch((e) => {
        console.log("error occured in fetch");
      });
  }, [location]);

  const { window } = props;
  const [mobileOpen, setMobileOpen] = useState(false);
  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const drawer = (
    <div className="h-100 border-left-0">
      <div className="headergradient border-left-0" style={{ height: "65px" }}>
        <Avatar
          src={profilePhoto}
          className="mx-auto"
          sx={{ width: 40, height: 40, marginBottom: "7px" }}
        />
        <Typography
          fontSize={14}
          style={{
            display: "flex",
            justifyContent: "center",
            color: "white",
          }}
        >
          {email}
        </Typography>
      </div>
      <Divider />
      <List className={`${isHome ? "activetab" : ""}`}>
        <ListItem
          button
          onClick={() => {
            histo.push("/HomeParkingOwner");
          }}
          style={{ display: "flex", justifyContent: "flex-start" }}
        >
          {/* <ListItemText primary={homeString} /> */}

          <ListItemIcon>
            <HomeIcon />
          </ListItemIcon>
          {/* <h5>خانه</h5> */}
          <Typography>خانه</Typography>
        </ListItem>
      </List>
      <Divider />
      <List className={`${isParkings ? "activetab" : ""}`}>
        <ListItem button onClick={handleCarOpen}>
          <ListItemIcon>
            <LocalParkingIcon />
          </ListItemIcon>
          <Typography className="ms-2">پارکینگ های من</Typography>
          {open ? (
            <ExpandLess style={{ color: "black" }} />
          ) : (
            <ExpandMore style={{ color: "black" }} />
          )}
        </ListItem>
        <Collapse
          in={open}
          timeout="auto"
          unmountOnExit
          className={`${isParkings ? "activetab" : ""}`}
        >
          <List component="div" disablePadding>
            {parkings.map(function (parking) {
              return (
                <ListItem
                  className={`${
                    parking.parkingName == localStorage.getItem("pName") &&
                    isParkings
                      ? "activenestedtab"
                      : ""
                  }`}
                  button
                  key={parking.id}
                  onClick={() => {
                    localStorage.setItem("pID", parking.id);
                    localStorage.setItem("pAddress", parking.location);
                    localStorage.setItem("pName", parking.parkingName);
                    localStorage.setItem(
                      "pPhoneNum",
                      parking.parkingPhoneNumber
                    );
                    localStorage.setItem("pCapacity", parking.capacity);
                    localStorage.setItem("pImage", parking.parkingPicture);
                    localStorage.setItem("pCheckbox", parking.isPrivate);
                    localStorage.setItem("pricePerHour", parking.pricePerHour);
                    histo.push("/Panel");
                  }}
                >
                  <ListItemIcon>
                    <GiHomeGarage />
                  </ListItemIcon>
                  <Typography>{parking.parkingName}</Typography>
                </ListItem>
              );
            })}
            <ListItem
              button
              onClick={() => {
                histo.push("/RegisterParking");
              }}
            >
              <ListItemIcon>
                <AddIcon />
              </ListItemIcon>
              <Typography>اضافه کردن</Typography>
            </ListItem>
          </List>
        </Collapse>
      </List>
      {/* <Divider />
      <List>
        <ListItem
          className={`${isProfile ? 'activetab' : ''}`}
          button
          onClick={() => {
            histo.push('/EditInfo');
          }}
        >
          <ListItemIcon>
            <PersonIcon />
          </ListItemIcon>
          <Typography>پروفایل</Typography>
        </ListItem>
      </List> */}
    </div>
  );

  const container =
    window !== undefined ? () => window().document.body : undefined;
  return (
    <Box sx={{ display: "flex" }}>
      <AppBar
        position="fixed"
        style={{
          // background:
          //   'linear-gradient(-45deg,#9970ceac,#bf8ffd92,#84a1f9ab,#e7eaf9c7)',
          backgroundColor: "#706bec",
        }}
        className="headergradient"
      >
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={handleDrawerToggle}
          >
            <MenuIcon />
          </IconButton>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            !PARKESH KON
            <Typography variant="subtitle1">
              a project by fortuna team
            </Typography>
          </Typography>
          <IconButton size="large" edge="end" color="inherit">
            <PowerSettingsNewRoundedIcon
              onClick={() => {
                axios
                  .post("http://127.0.0.1:8000/users/rest-auth/logout/", {
                    headers: { authorization: auth },
                  })
                  .then((response) => {
                    console.log("logged out!");
                    histo.push("/");
                  });
              }}
            />
          </IconButton>
        </Toolbar>
      </AppBar>
      <Box
        component="div"
        alignItems="end"
        sx={{
          width: { sm: drawerWidth },
          flexShrink: { sm: 0 },
        }}
        aria-label="mailbox folders"
        borderLeft={0}
        borderColor="red"
      >
        {/* The implementation can be swapped with js to avoid SEO duplication of links. */}
        <SwipeableDrawer
          anchor={"right"}
          SlideProps={{ direction: "left" }}
          container={container}
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          borderLeft={0}
          borderColor="red"
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: {
              xs: "flex",
              sm: "flex",
              md: "none",
              alignContent: "flex-start",
            },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </SwipeableDrawer>
        <Drawer
          anchor={"right"}
          container={container}
          variant="permanent"
          sx={{
            display: { xs: "none", sm: "none", md: "flex" },
            "& .MuiDrawer-paper": {
              boxSizing: "border-box",
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>
    </Box>
  );
};

export default AppHeaderParkingOwner;
