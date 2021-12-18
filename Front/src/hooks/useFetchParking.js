import React, { useEffect } from 'react';
import axios from 'axios';
import { useState } from 'react';

export default function useFetchParking(page) {
  const [parkings, setParkings] = useState([]);
  const [count, setCount] = useState(1);
  const [data, setData] = useState({});
  const [hasMore, setHasMore] = useState(true);

  let token = localStorage.getItem('ctoken');
  let auth = `Token ${token}`;

  useEffect(() => {
    // fetch(link, {
    //   mode: 'cors',
    //   credentials: 'omit',
    //   headers: {
    //     Authorization: auth,
    //     'Access-Control-Allow-Origin': '*',
    //     // 'Access-Control-Request-Method:': 'GET',
    //   },
    //   method: 'GET',

    // })
    //   .then((res) => {
    //     // console.log(res);
    //     if (res.ok) {
    //       return res.json();
    //     }
    //     throw res;
    //   })
    //   .then((d) => {
    //     // console.log('everything was ok!');
    //     // console.log(d.results);
    //     // console.log(d.count);

    //     setParkings((prevState) => [...prevState, ...d.results]);
    //     //here we add to array while keeping the previous results
    //   })
    //   .catch(console.log('error occured in fetch'));
    axios
      .get('http://127.0.0.1:8000/carowner/parkinglist', {
        headers: { 'Content-Type': 'application/json', Authorization: auth },
        params: { page: page },
      })
      .then((res) => {
        console.log(res.data);
        setParkings((prevState) => [...prevState, ...res.data.results]);
        setCount(res.data.count);
        if (res.data.next === null) setHasMore(false);
      })
      .catch((e) => {
        console.log('error occured in fetch');
      });
  }, [page]);

  return [parkings, hasMore];
}
