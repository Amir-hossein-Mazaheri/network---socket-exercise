import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import getList from "../api/getList";
import FileItem from "./FileItem";
import getPath from "../api/getPath";

const FileExplorer = () => {
  const [prefix, setPrefix] = useState("");
  const [previousPaths, setPreviousPaths] = useState<string[]>([]);

  const { data, isLoading, error } = useQuery(["list", prefix], () =>
    getList(prefix)
  );

  const { data: startPath } = useQuery(["path"], getPath);

  const handleChangePath = (path: string) => {
    setPreviousPaths((paths) => [
      ...paths,
      !!prefix ? prefix : startPath ?? "",
    ]);
    setPrefix(path);
  };

  const handleGoBack = () => {
    const lastPath = previousPaths.at(-1);

    console.log("last path: ", lastPath);

    setPreviousPaths((paths) => {
      const copyPaths = [...paths];

      copyPaths.pop();

      return copyPaths;
    });

    lastPath && setPrefix(lastPath);
  };

  console.log("prefix: ", prefix);
  console.log("previous paths: ", previousPaths);

  return (
    <div className="px-12 py-8 bg-gray-800 text-white h-screen w-screen">
      <div className="mb-12">
        <h1 className="font-bold text-3xl">File Explorer</h1>
      </div>

      <div className="grid grid-cols-3 gap-6">
        {!!previousPaths.length && (
          <FileItem name=".." type="DIR" path=".." setPrefix={handleGoBack} />
        )}
        {data?.map((item) => (
          <FileItem key={item.path} {...item} setPrefix={handleChangePath} />
        ))}
      </div>
    </div>
  );
};

export default FileExplorer;
