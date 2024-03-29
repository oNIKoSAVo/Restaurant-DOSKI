import { getCSRFtoken } from "./utils";
import qs from "qs";

export async function request(method, path, data) {
  return await fetch(path, {
    method: method,
    headers: {
      "X-CSRFToken": getCSRFtoken(),
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: qs.stringify({ ...data }),
  })
    .then((response) => {
      return response.json();
    })
    .then((data) => {
      return data;
    });
}

export function feedbackRequest(data) {
  return request("POST", "/feedback", data);
}

export function franchiseRequest(data) {
  return request("POST", "/franchise", data);
}

export function reservationRequest(data) {
  return request("POST", "/reservation", data);
}

export function careerRequest(data) {
  return request("POST", "/career", data);
}

export function signUp(data){
  return request("POST", "/signup", data);
}

export function signIn(data){
  return request("POST", "/signin", data);
}
