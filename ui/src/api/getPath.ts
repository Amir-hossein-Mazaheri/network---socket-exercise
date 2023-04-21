import axiosInstance from "./axiosInstance";

async function getPath() {
  const res = await axiosInstance.get("/path");

  return res.data.path as string;
}

export default getPath;
