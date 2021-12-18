import React from 'react';

export function nationalCodeValidation(input) {
  if (input.length !== 10) return false;
  let a =
    parseInt(input[0]) * 10 +
    parseInt(input[1]) * 9 +
    parseInt(input[2]) * 8 +
    parseInt(input[3]) * 7 +
    parseInt(input[4]) * 6 +
    parseInt(input[5]) * 5 +
    parseInt(input[6]) * 4 +
    parseInt(input[7]) * 3 +
    parseInt(input[8]) * 2;
  let b = parseInt(input[9]);
  let c = a % 11;

  if (c >= 2 && b === 11 - c) return true;
  else if (c < 2 && b === c) return true;
  else return false;
}

export function passwordValidation(input) {
  let passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,15}$/;
  let passRegex = new RegExp(passwordPattern, 'g');
  if (passRegex.test(input) === true) return true;
  else return false;
}

export function phoneNumberValidation(input) {
  let numPattern =
    /^09(1[0-9]|3[1-9]|2[1-9]|0[0-9]|9[0-9])-?[0-9]{3}-?[0-9]{4}$/;
  let numRegex = new RegExp(numPattern, 'g');
  if (numRegex.test(input) === true) return true;
  else return false;
}
export function passResetValidation(firstInput, secondInput) {
  if (firstInput !== secondInput) return false;
  else if (passwordValidation(firstInput) === false) return false;
  else if (passwordValidation(secondInput) === false) return false;
  else return true;
}
export function validateEmail(email) {
  const re =
    /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
  return re.test(String(email).toLowerCase());
}
