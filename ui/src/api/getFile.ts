import axiosInstance from "./axiosInstance";

async function getFile(path: string) {
  return await axiosInstance.get(`/file?path=${path}`);
}

export default getFile;
