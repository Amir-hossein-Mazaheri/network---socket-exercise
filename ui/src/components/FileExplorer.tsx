import { useState } from "react";
import { useQuery } from "@tanstack/react-query";

import getList from "../api/getList";
import FileItem from "./FileItem";
import getPath from "../api/getPath";

const FileExplorer = () => {
  const [prefix, setPrefix] = useState("");

  // previous paths acts like a stack which holds all paths that user has visited
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

    // its just a stack pop in react way :)
    setPreviousPaths((paths) => {
      const copyPaths = [...paths];

      copyPaths.pop();

      return copyPaths;
    });

    lastPath && setPrefix(lastPath);
  };

  return (
    <div className="px-12 py-8 bg-gray-800 text-white min-h-screen w-screen">
      <div className="mb-12">
        <h1 className="font-bold text-3xl">File Explorer</h1>
      </div>

      {isLoading ? (
        <p className="font-bold text-lg text-red-500">Loading Please Wait...</p>
      ) : (
        <div className="grid lg:grid-cols-3 md:grid-cols-2 grid-cols-1 gap-6">
          {/* just simulate native os go back directory but it just call cd into last previous paths item and pop it*/}
          {!!previousPaths.length && (
            <FileItem name=".." type="DIR" path=".." onClick={handleGoBack} />
          )}
          {!!error ? (
            <p>Something went wrong</p>
          ) : (
            data?.map((item) => (
              <FileItem key={item.path} {...item} onClick={handleChangePath} />
            ))
          )}
        </div>
      )}
    </div>
  );
};

export default FileExplorer;
