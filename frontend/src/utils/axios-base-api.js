import axios from "axios";

export const instance = axios.create({
  baseURL: process.env.REACT_APP_API,
});

export default {
  get: (url, params) =>
    instance({
      method: "GET",
      url,
      params,
    }),
  post: (url, data) =>
    instance({
      method: "POST",
      url,
      data,
    }),
  delete: (url, params) =>
    instance({
      method: "DELETE",
      url,
      params,
    }),
};