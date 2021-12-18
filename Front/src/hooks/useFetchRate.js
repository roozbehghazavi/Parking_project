import React, { useEffect } from "react";
import axios from "axios";
import { useState } from "react";

export default function useFetchParking(id) {
  const [rate, setRate] = useState(null);

  let token = localStorage.getItem("ctoken");
  let auth = `Token ${token}`;

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/carowner/israted/", {
        headers: { Authorization: auth },
        params: { id: id },
      })
      .then((response) => {
        console.log("response israted: ", response);
        setRate(response.data.isRated);
        console.log("rate:", rate);
      })
      .catch((e) => {
        console.log("error:", e);
      });

    // fetch(`http://127.0.0.1:8000/carowner/israted/?id=${id}`, {
    //   method: "GET",
    //   headers: {
    //     Authorization: auth,
    //   },
    // })
    //   .then((response) => {
    //     if (response.ok) {
    //       return response.json();
    //     }
    //   })
    //   .then((data) => {
    //     console.log("response israted : ", data.isRated);
    //     setRate(data.isRated);
    //     console.log("rate:", rate);
    //   })
    //   .catch((e) => {
    //     console.log("error:", e);
    //   });
  }, [id]);

  return [rate];
}
