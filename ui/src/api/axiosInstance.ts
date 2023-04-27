import axios from "axios";

const axiosInstance = axios.create({
  // its just here to make axios not append the page url to the request url
  // it will be changed by an interceptor
  baseURL: "http://localhost:5500",
});

axiosInstance.interceptors.request.use((config) => {
  config.baseURL = localStorage.getItem("node") ?? "";

  return config;
});

export default axiosInstance;
