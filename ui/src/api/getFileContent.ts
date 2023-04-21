import axiosInstance from "./axiosInstance";

async function getFileContent(path: string) {
  return await axiosInstance.get(`/file?path=${path}`);
}

export default getFileContent;
