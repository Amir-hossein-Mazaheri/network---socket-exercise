import axiosInstance from "./axiosInstance";

export type TFileItem = {
  name: string;
  path: string;
  type: "FILE" | "DIR";
};

async function getList(prefix = "") {
  const res = await axiosInstance.get(`/list?prefix=${prefix}`);

  return res.data as unknown as TFileItem[];
}

export default getList;
